# Forge OS Documentation

> **Version 1.0** · [Repository](https://github.com/axk42-op/ForgeOS) · [Wiki Home](Home)

---

## Table of contents

1. [About](#about-forge-os)
2. [Getting started](#getting-started)
3. [Authentication](#authentication)
4. [Command reference](#command-reference)
5. [Disclaimer](#disclaimer)
6. [Troubleshooting](#troubleshooting)

---

## About Forge OS

Forge OS is a Python virtual operating system with its own shell, VFS, package manager, and login system. It is **not** a real kernel.

| | |
|---|---|
| **Author** | ayaan global |
| **License** | MIT |
| **Repository** | https://github.com/axk42-op/ForgeOS |

---

## Getting started

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

---

## Authentication

- **First run:** create username + password
- **Later runs:** login prompt
- **Storage:** local machine only (Windows: `%LOCALAPPDATA%\ForgeOS\ForgeOS\credentials.json`)
- **Passwords:** salted SHA-256 hashes — never plain text
- **Commands:** `passwd` (change password), `logout` (sign out)

---

## Command reference

Run `help` in the shell for the full list. Categories:

| Category | Examples |
|----------|----------|
| **System** | `help`, `about`, `version`, `docs`, `source`, `disclaimer`, `clear`, `exit` |
| **User** | `whoami`, `passwd`, `logout`, `hostname`, `date`, `uptime` |
| **Filesystem** | `ls`, `cd`, `pwd`, `cat`, `mkdir`, `cp`, `mv`, `rm`, `tree`, `grep` |
| **Network** | `echo`, `ping`, `curl`, `history`, `alias`, `man` |
| **Developer** | `forgepkg`, `python`, `git`, `npm`, `node` |
| **Apps** | `forgefetch`, `logo`, `fortune`, `calc` |

### forgepkg

- `forgepkg list` — installed packages
- `forgepkg info` — manager info
- `forgepkg install NAME` — install a package

---

## Disclaimer

Forge OS is a **virtual** OS for learning and development. Commands and network tools are simulated.

**Account storage:** credentials are stored **locally** on your machine only. Usernames and salted password hashes are saved — plain-text passwords are never stored.

Forge OS is provided **"as is"** without warranty. Run `disclaimer` in the shell for the live notice.

---

## Troubleshooting

**Path not found (Windows):** use two steps or `&&`:

```cmd
cd /d D:\ForgeOS\Forge && .\.venv\Scripts\python.exe boot.py
```

**Single-window testing:**

```cmd
python boot.py --session
```

---

*Forge OS — developed by **ayaan global***
