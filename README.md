# Forge OS

> A Python-powered virtual operating system for developers.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-00C853?style=for-the-badge)

---

## What is Forge OS?

Forge OS is an open-source virtual operating system built entirely in Python.

Unlike a traditional operating system, Forge OS runs as a Python application while providing its own operating system environment. It is designed for learning, experimentation, software development, and testing operating system concepts without interacting directly with computer hardware.

The project focuses on creating a developer-first environment featuring its own shell, virtual filesystem, package manager, user management, applications, and (planned) desktop environment.

---

## Vision

Forge OS aims to become a complete virtual development platform where users can:

* Write code
* Build applications
* Test software
* Manage projects
* Install packages
* Explore operating system concepts
* Learn software architecture

---

## Features

### v1.0

* **Forge Shell** — 65+ auto-discovered commands (`help`, `docs`, `source`, `disclaimer`, and more)
* **Login system** — first-run registration, returning-user login, `passwd`, `logout`
* **Supabase auth** — cloud account storage in `forge_users` (salted SHA-256 hashes; local fallback)
* **ForgeOS terminal window** — dedicated boot window on Windows
* **Virtual filesystem** — in-memory VFS with user home directories
* **Package manager** — `forgepkg list`, `info`, `install`
* **Rich UI** — boot banner, animated startup, colored shell output
* **CLI** — `forgeos login`, `forgeos start`, `forgeos version`
* **Wiki docs** — `docs` and `source` commands link to GitHub wiki and repo

### Current

* Custom boot sequence with ForgeOS terminal window
* Local login / first-run account setup
* Forge Shell (64+ commands)
* Kernel manager
* Virtual filesystem (in-memory VFS)
* User management
* Package manager (`forgepkg`)
* Boot banner and Rich UI
* Modular command architecture with auto-discovery
* Command history, aliases, pipes (basic)
* Auth stored locally via `platformdirs`, or in **Supabase** when configured (salted SHA-256 hashes — never plain text)

### Planned

#### Shell

* Full pipe/redirection support
* Syntax highlighting in the REPL
* Rich prompt themes

#### Filesystem

* File permissions
* Symbolic links
* Mount points
* Persistence across sessions

#### Package Manager

* `forgepkg remove` / `forgepkg update`
* Package repositories
* Dependency resolution

#### Applications

* Terminal (enhanced)
* File Manager
* Settings
* Text Editor

#### Developer Tools

* Git integration (real)
* Python / Node.js / npm wrappers (real)
* Package SDK

#### Desktop

* Window manager
* Taskbar
* Notifications
* Themes
* Widgets

---

## Planned Applications

* vi / Vim / Neovim
* Vimge
* Forge (editor)
* Forgium (browser)

---

## Project Structure

```text
Forge/
├── boot.py              # Boot entry point
├── cli.py               # forgeos CLI (login, version)
├── launcher.py          # ForgeOS window launcher
├── auth/                # Login, crypto, local + Supabase credential stores
│   └── supabase_store.py
├── docs/
│   ├── HOME.md          # GitHub Wiki home (copy to wiki)
│   └── WIKI.md          # GitHub Wiki docs (copy to wiki)
├── supabase/
│   └── schema.sql       # Run once in Supabase SQL Editor
├── .env.example         # Copy to .env for Supabase credentials
├── kernel/
├── shell/
│   ├── commands/        # Auto-discovered shell commands
│   └── ui/              # Rich UI components
├── filesystem/
├── users/
├── packages/
├── pyproject.toml       # PyPI packaging (planned)
└── requirements.txt
```

---

## Quick start

```cmd
cd Forge
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

On first launch, Forge OS opens a **ForgeOS** terminal window and prompts you to create an account. On later runs, use `forgeos login` or `python boot.py`.

---

## Supabase (cloud accounts)

By default, credentials are stored locally on your machine. To save usernames and **hashed** passwords to Supabase instead:

1. Create a [Supabase](https://supabase.com) project.
2. In the SQL Editor, run `supabase/schema.sql` to create the `forge_users` table.
3. Copy `.env.example` → `.env` and set:
   - `FORGEOS_SUPABASE_URL` — Project Settings → API → Project URL
   - `FORGEOS_SUPABASE_KEY` — **service role** key (keeps writes working from the CLI; never commit this file)
4. Restart Forge OS and register or sign in — accounts are stored in `forge_users`.

| Column          | Description                          |
|-----------------|--------------------------------------|
| `username`      | Unique login name                    |
| `password_hash` | SHA-256 hash of `salt:password`      |
| `salt`          | Random hex per account               |

Without a `.env` file, Forge OS falls back to local storage automatically.

---

## Install from GitHub (other devices)

Clone the repo and run Forge OS on any machine with **Python 3.10+** and [uv](https://github.com/astral-sh/uv) (recommended).

### Windows

```cmd
git clone https://github.com/axk42-op/ForgeOS.git
cd ForgeOS
uv venv
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

### Linux / macOS

```bash
git clone https://github.com/axk42-op/ForgeOS.git
cd ForgeOS
uv venv
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

### Optional: Supabase on a new device

```bash
cp .env.example .env
# Edit .env with your Supabase URL and key
# Run supabase/schema.sql once in Supabase SQL Editor
python boot.py
```

### Wiki & links

* **Documentation:** https://github.com/axk42-op/ForgeOS/wiki/Docs
* **Repository:** https://github.com/axk42-op/ForgeOS
* In the shell: `docs` · `source` · `disclaimer`