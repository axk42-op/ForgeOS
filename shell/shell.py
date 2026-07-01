"""Forge Shell — main REPL loop."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from colorama import init as colorama_init
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
from rich.console import Console

from shell.completion import CompletionEngine
from shell.config import ShellConfig
from shell.dispatcher import CommandDispatcher, DispatchResult
from shell.errors import ShellError
from shell.history import SessionHistory
from shell.logger import ShellLogger
from shell.parser import CommandParser
from shell.prompt import PromptRenderer
from shell.registry import CommandRegistry
from shell.session import ShellSession
from shell.ui.screen import ScreenManager

from desktop.icon import apply_window_icon


class ForgeShell:
    """Interactive shell for Forge OS.

    Responsibilities: display prompt, read input, parse, dispatch, print result.
    """

    def __init__(
        self,
        kernel: Any,
        filesystem: Any,
        users: Any,
        packages: Any,
        config: ShellConfig | None = None,
        console: Console | None = None,
        *,
        gui_mode: bool = False,
    ) -> None:
        colorama_init(autoreset=True)

        self._gui_mode = gui_mode
        self._read_line_callback: Callable[[str], str] | None = None
        self._gui_clear_callback: Callable[[], None] | None = None

        self._console = console or Console(force_terminal=True, legacy_windows=False)
        self._screen = ScreenManager(console=self._console)
        self._config = config or ShellConfig()
        self._session = ShellSession.create(config=self._config, users=users)
        self._parser = CommandParser()
        self._logger = ShellLogger(console=self._console)

        self._registry = CommandRegistry()
        self._registry.discover()

        self._context = {
            "kernel": kernel,
            "filesystem": filesystem,
            "users": users,
            "packages": packages,
            "console": self._console,
            "logger": self._logger,
            "registry": self._registry,
            "gui_mode": gui_mode,
        }

        self._dispatcher = CommandDispatcher(self._registry, self._context, self._parser)
        self._context["dispatcher"] = self._dispatcher
        self._context["parser"] = self._parser
        self._prompt = PromptRenderer(self._session, self._config)
        self._completion = CompletionEngine(self._registry)
        self._desktop = None
        if not gui_mode:
            from desktop.chrome import DesktopChrome

            self._desktop = DesktopChrome(self._console, self._session, self._config)
        self._input_session: PromptSession | None = None
        self._use_fallback_input = False

    @property
    def session(self) -> ShellSession:
        return self._session

    @property
    def registry(self) -> CommandRegistry:
        return self._registry

    def attach_gui_console(self, console: Console) -> None:
        """Route shell output to a GUI-hosted Rich console."""
        self._console = console
        self._screen = ScreenManager(console=console)
        self._logger = ShellLogger(console=console)
        self._context["console"] = console

    def set_gui_mode(self, enabled: bool) -> None:
        self._gui_mode = enabled
        self._context["gui_mode"] = enabled

    def set_gui_clear(self, callback: Callable[[], None]) -> None:
        self._gui_clear_callback = callback

    def start(self) -> None:
        """Start the interactive shell loop in the system terminal."""
        if self._gui_mode:
            raise RuntimeError("Use start_gui() when running inside the desktop terminal window.")

        apply_window_icon()
        self._init_input()

        while self._session.running:
            try:
                if self._desktop:
                    self._desktop.show_taskbar()
                user_input = self._read_input()
                self._handle_input(user_input)
            except KeyboardInterrupt:
                self._console.print()
                continue
            except EOFError:
                self._console.print()
                break
            except ShellError as error:
                self._session.last_exit_code = error.exit_code
                self._console.print(error.message, style="bold red")
            except Exception as error:
                self._session.last_exit_code = 1
                self._console.print(f"shell: {error}", style="bold red")

    def start_gui(self, read_line: Callable[[str], str]) -> None:
        """Start the shell loop inside a Forge OS terminal window."""
        self._read_line_callback = read_line
        self._context["gui_read_line"] = read_line
        self._use_fallback_input = True

        while self._session.running:
            try:
                prompt = self._prompt.render_plain()
                user_input = read_line(prompt)
                self._handle_input(user_input)
            except KeyboardInterrupt:
                self._console.print()
                continue
            except EOFError:
                self._console.print()
                break
            except ShellError as error:
                self._session.last_exit_code = error.exit_code
                self._console.print(error.message, style="bold red")
            except Exception as error:
                self._session.last_exit_code = 1
                self._console.print(f"shell: {error}", style="bold red")

    def _handle_input(self, user_input: str) -> None:
        if not user_input.strip():
            return

        if self._use_fallback_input:
            self._session.history.add(user_input)
        parse_result = self._parser.parse(user_input)
        dispatch_result = self._dispatcher.dispatch(parse_result, self._session)
        self._render_result(dispatch_result)

        if dispatch_result.should_exit:
            self._session.stop()

    def _init_input(self) -> None:
        if self._input_session is not None or self._use_fallback_input:
            return

        try:
            completer = None
            if self._config.enable_completion:
                completer = WordCompleter(
                    self._registry.names(),
                    ignore_case=True,
                    sentence=True,
                )
            self._input_session = PromptSession(
                history=SessionHistory(self._session.history),
                enable_history_search=True,
                completer=completer,
            )
        except NoConsoleScreenBufferError:
            self._use_fallback_input = True

    def _read_input(self) -> str:
        if self._read_line_callback is not None:
            return self._read_line_callback(self._prompt.render_plain())

        prompt_text = self._prompt.render_plain()
        if self._use_fallback_input or self._input_session is None:
            return input(prompt_text)
        return self._input_session.prompt(prompt_text)

    def _render_result(self, result: DispatchResult) -> None:
        if result.clear_screen:
            if self._gui_clear_callback:
                self._gui_clear_callback()
            else:
                self._screen.clear()

        if result.renderable is not None:
            self._console.print(result.renderable)
            if self._gui_mode:
                self._console.print()
        elif result.output:
            self._console.print(result.output)
            if self._gui_mode and not result.output.endswith("\n"):
                self._console.print()
