# Forge OS Documentation

> **Version 1.0** · [Repository](https://github.com/axk42-op/ForgeOS) · [Wiki Home](Home)

---

## Table of contents

1. [About Forge OS](#about-forge-os)
2. [Getting started](#getting-started)
3. [Authentication & Supabase](#authentication--supabase)
4. [Shell prompt](#shell-prompt)
5. [Command reference](#command-reference)
6. [forgepkg subcommands](#forgepkg-subcommands)
7. [Supabase setup](#supabase-setup)
8. [Project structure](#project-structure)
9. [Disclaimer](#disclaimer)
10. [Troubleshooting](#troubleshooting)

---

## About Forge OS

Forge OS is a Python-based virtual operating system for learning, experimentation, and development. It is **not** a real kernel or hardware OS. It runs as a Python application and provides:

- Custom boot sequence and **ForgeOS** terminal window
- Login / account system backed by **[Supabase](https://supabase.com)** (PostgreSQL) for cloud storage
- Local credential fallback when Supabase is not configured on a machine
- **Forge Shell** with 65+ commands
- Virtual in-memory filesystem (VFS)
- User management
- Package manager (`forgepkg`)
- Rich terminal UI

| | |
|---|---|
| **Author** | ayaan global |
| **License** | MIT |
| **Repository** | https://github.com/axk42-op/ForgeOS |
| **Documentation** | https://github.com/axk42-op/ForgeOS/wiki/Docs |
| **Database** | [Supabase](https://supabase.com) — `forge_users` table (usernames + salted password hashes) |

In the shell, run `docs` to open this wiki in your browser, or `source` to open the GitHub repository.

---

## Getting started

### Install from GitHub (any device)

Requires **Python 3.10+** and [uv](https://github.com/astral-sh/uv).

**Windows:**

```cmd
git clone https://github.com/axk42-op/ForgeOS.git
cd ForgeOS
uv venv
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

**Linux / macOS:**

```bash
git clone https://github.com/axk42-op/ForgeOS.git
cd ForgeOS
uv venv
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

### Already cloned — Windows local path

```cmd
cd /d D:\ForgeOS\Forge
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

### Launch

```cmd
cd /d D:\ForgeOS\Forge && .\.venv\Scripts\python.exe boot.py
```

Opens a new **ForgeOS** terminal window, then login.

### Run in the current terminal (debug)

```cmd
cd /d D:\ForgeOS\Forge && .\.venv\Scripts\python.exe boot.py --session
```

### Host CLI (after `uv pip install -e .`)

```cmd
forgeos login
forgeos start
forgeos version
```

---

## Authentication & Supabase

Forge OS uses **Supabase** as its cloud database for account storage.

| What | Details |
|------|---------|
| **First run** | Create a username and password |
| **Later runs** | Login prompt (3 attempts) |
| **Password storage** | Salted SHA-256 hashes only — **never plain text** |
| **Cloud database** | Supabase PostgreSQL — table `forge_users` |
| **Local fallback** | `%LOCALAPPDATA%\ForgeOS\ForgeOS\credentials.json` when `.env` is not set |
| **Change password** | `passwd` |
| **Sign out** | `logout` |

### How storage is chosen

1. If `FORGEOS_SUPABASE_URL` and `FORGEOS_SUPABASE_KEY` are set in `.env` → accounts are stored in **Supabase**.
2. If not configured → accounts are stored **locally** on that machine until Supabase is set up.

Run `disclaimer` in the shell for the full legal and data-storage notice.

---

## Shell prompt

```
user@localhost:/home/user $
```

---

## Command reference

### System

| Command | Syntax | Description |
|---------|--------|-------------|
| help | `help [COMMAND]` | List commands or show help for one command |
| about | `about` | About Forge OS |
| version | `version` | Show version |
| clear | `clear` | Clear screen |
| cls | `cls` | Clear screen (alias) |
| exit | `exit` | Exit shell |
| license | `license` | Show MIT license from `/etc/LICENSE` |
| copyright | `copyright` | Copyright notice |
| credits | `credits` | Project credits |
| authors | `authors` | Project authors |
| disclaimer | `disclaimer` | Legal notice + Supabase data-storage disclosure |
| docs | `docs` | Open GitHub Wiki docs in browser |
| source | `source` | Open GitHub repository in browser |
| uname | `uname [-a]` | System info |
| df | `df` | Disk usage (virtual) |
| free | `free` | Memory usage |
| ps | `ps` | List processes (virtual) |
| kill | `kill PID` | Kill process (virtual) |
| users | `users` | List Forge OS users |
| reboot | `reboot` | Reboot Forge OS |
| shutdown | `shutdown` | Shut down Forge OS |

### User

| Command | Syntax | Description |
|---------|--------|-------------|
| whoami | `whoami` | Current user |
| who | `who` | Logged-in users |
| id | `id [USER]` | User/group identity |
| groups | `groups [USER]` | Group membership |
| passwd | `passwd` | Change password (syncs to Supabase when configured) |
| logout | `logout` | Log out and exit |
| hostname | `hostname` | System hostname |
| date | `date` | Current date |
| time | `time` | Current time |
| uptime | `uptime` | System uptime |
| env | `env` | Environment variables |

### Filesystem

| Command | Syntax | Description |
|---------|--------|-------------|
| ls | `ls [PATH]` | List directory |
| cd | `cd [PATH]` | Change directory |
| pwd | `pwd` | Print working directory |
| cat | `cat FILE...` | Print file contents |
| mkdir | `mkdir [-p] DIR...` | Create directories |
| touch | `touch FILE...` | Create empty files |
| cp | `cp SOURCE DEST` | Copy files |
| mv | `mv SOURCE DEST` | Move/rename files |
| rm | `rm [-r] PATH...` | Remove files/dirs |
| find | `find [PATH] [PATTERN]` | Search files |
| tree | `tree [PATH]` | Directory tree |
| head | `head [-n NUM] FILE` | First lines of file |
| tail | `tail [-n NUM] FILE` | Last lines of file |
| grep | `grep PATTERN FILE...` | Search in files |
| wc | `wc [FILE...]` | Line/word/byte counts |
| sort | `sort [FILE]` | Sort lines |

### Network (mostly simulated)

| Command | Syntax | Description |
|---------|--------|-------------|
| echo | `echo [TEXT...]` | Print text |
| ping | `ping HOST` | Ping host (simulated) |
| curl | `curl URL` | HTTP request (simulated) |
| wget | `wget URL` | Download (simulated) |
| netstat | `netstat` | Network connections (virtual) |
| alias | `alias [NAME[=VALUE]]` | Manage aliases |
| history | `history` | Command history |
| which | `which COMMAND` | Locate command |
| where | `where COMMAND` | Locate command (alias) |
| man | `man COMMAND` | Manual for a command |

### Developer

| Command | Syntax | Description |
|---------|--------|-------------|
| forgepkg | `forgepkg [list\|info\|install]` | Package manager |
| python | `python [ARGS...]` | Python (placeholder) |
| node | `node [ARGS...]` | Node.js (placeholder) |
| npm | `npm [ARGS...]` | npm (placeholder) |
| git | `git [ARGS...]` | Git (placeholder) |

### Apps

| Command | Syntax | Description |
|---------|--------|-------------|
| forgefetch | `forgefetch` | System info (neofetch-style) |
| logo | `logo` | Forge OS ASCII logo |
| fortune | `fortune` | Random fortune |
| calc | `calc EXPRESSION` | Math calculator |

---

## forgepkg subcommands

- `forgepkg list` — list installed packages
- `forgepkg info` — package manager info
- `forgepkg install NAME` — install a package

---

## Supabase setup

Forge OS uses **[Supabase](https://supabase.com)** to store user accounts in the cloud. Passwords are never stored in plain text — only salted SHA-256 hashes.

### Steps

1. Create a [Supabase](https://supabase.com) project.
2. In the **SQL Editor**, run `supabase/schema.sql` (creates the `forge_users` table).
3. Copy `.env.example` → `.env` in the Forge project folder.
4. Set:
   - `FORGEOS_SUPABASE_URL` — Project Settings → API → Project URL
   - `FORGEOS_SUPABASE_KEY` — API key (service role recommended for CLI writes)
5. Restart Forge OS — register or sign in; accounts appear in Supabase **Table Editor → forge_users**.

### `forge_users` table

| Column | Description |
|--------|-------------|
| `id` | UUID primary key |
| `username` | Unique login name |
| `password_hash` | SHA-256 hash of `salt:password` |
| `salt` | Random hex per account |
| `created_at` | Account creation timestamp |

**Security:** Never commit `.env` to Git. It is listed in `.gitignore`.

---

## Project structure

```text
Forge/
├── boot.py              # Boot entry point
├── cli.py               # forgeos CLI
├── launcher.py          # ForgeOS window launcher
├── auth/                # Login, crypto, local + Supabase stores
├── supabase/
│   └── schema.sql       # Run once in Supabase SQL Editor
├── .env.example         # Supabase URL + key template
├── kernel/
├── shell/
│   ├── commands/        # Auto-discovered shell commands
│   └── ui/
├── filesystem/          # Virtual filesystem (VFS)
├── users/
├── packages/
└── pyproject.toml
```

---

## Disclaimer

Forge OS is a **virtual** operating system — not a real kernel or hardware OS. Commands, network tools, and processes are simulated for learning and development.

### Database (Supabase)

Forge OS uses **Supabase** (PostgreSQL) for account storage. Usernames and salted password hashes are stored in the `forge_users` table. Plain-text passwords are **never** saved.

- When Supabase is configured (`.env` present) → cloud storage is **active**.
- When not configured → credentials are stored **locally** until `.env` is set up.

By creating an account, you acknowledge that your username and hashed credentials may be stored in the Forge OS Supabase database.

### No warranty

Forge OS is provided **"as is"** without warranty of any kind. Use at your own risk. Network tools, processes, and many developer commands are simulated or placeholders — not for production security use.

Run `disclaimer` in the shell for the live notice.

---

## Troubleshooting

### `The system cannot find the path specified` (Windows)

Do **not** paste the folder and python path as one string. Use:

```cmd
cd /d D:\ForgeOS\Forge && .\.venv\Scripts\python.exe boot.py
```

Or two lines:

```cmd
cd /d D:\ForgeOS\Forge
.\.venv\Scripts\python.exe boot.py
```

### Test in one window

```cmd
cd /d D:\ForgeOS\Forge && .\.venv\Scripts\python.exe boot.py --session
```

### Supabase connection errors

- Confirm `supabase/schema.sql` was run in the SQL Editor.
- Check `.env` has correct `FORGEOS_SUPABASE_URL` and `FORGEOS_SUPABASE_KEY`.
- Never commit `.env` to GitHub.

---

*Forge OS — developed by **ayaan global**. [MIT License](https://github.com/axk42-op/ForgeOS/blob/main/LICENSE)*
