"""Forge Shell — main REPL loop."""

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
    ) -> None:
        colorama_init(autoreset=True)

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
        }

        self._dispatcher = CommandDispatcher(self._registry, self._context, self._parser)
        self._prompt = PromptRenderer(self._session, self._config)
        self._completion = CompletionEngine(self._registry)
        self._input_session: PromptSession | None = None
        self._use_fallback_input = False

    @property
    def session(self) -> ShellSession:
        return self._session

    @property
    def registry(self) -> CommandRegistry:
        return self._registry

    def start(self) -> None:
        """Start the interactive shell loop."""
        self._init_input()

        while self._session.running:
            try:
                user_input = self._read_input()
                if not user_input.strip():
                    continue

                if self._use_fallback_input:
                    self._session.history.add(user_input)
                parse_result = self._parser.parse(user_input)
                dispatch_result = self._dispatcher.dispatch(parse_result, self._session)
                self._render_result(dispatch_result)

                if dispatch_result.should_exit:
                    self._session.stop()

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
        prompt_text = self._prompt.render_plain()
        if self._use_fallback_input or self._input_session is None:
            return input(prompt_text)
        return self._input_session.prompt(prompt_text)

    def _render_result(self, result: DispatchResult) -> None:
        if result.clear_screen:
            self._screen.clear()

        if result.renderable is not None:
            self._console.print(result.renderable)
        elif result.output:
            self._console.print(result.output)
