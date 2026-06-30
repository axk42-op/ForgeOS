# Forge OS Wiki

Welcome to **Forge OS v1.0** — documentation for the Python virtual operating system.

---

## Quick links

| Link | Description |
|------|-------------|
| [Documentation](Docs) | Full command reference, setup, Supabase, troubleshooting |
| [GitHub Repository](https://github.com/axk42-op/ForgeOS) | Source code, issues, contributions |
| [License (MIT)](https://github.com/axk42-op/ForgeOS/blob/main/LICENSE) | Open-source license |

---

## What is Forge OS?

Forge OS is a Python-based **virtual operating system** for learning, experimentation, and development. It is not a real kernel — it runs as a Python app with its own shell, virtual filesystem, package manager, and 65+ commands.

Built by **ayaan global**. Open source under the **MIT License**.

---

## Features

- **ForgeOS** terminal window with boot sequence and Rich UI
- **Forge Shell** — 65+ auto-discovered commands
- **Virtual filesystem** (in-memory VFS)
- **User management** and login system
- **Package manager** — `forgepkg`
- **Supabase** cloud accounts — usernames and salted password hashes stored in PostgreSQL (`forge_users` table); local fallback when not configured

---

## Quick start (Windows)

```cmd
git clone https://github.com/axk42-op/ForgeOS.git
cd ForgeOS
uv venv
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

First launch: create an account. Later runs: sign in.

Debug in one window:

```cmd
python boot.py --session
```

## Install on other devices

See **[Documentation → Getting started](Docs#getting-started)** for Windows, Linux, and macOS install steps from GitHub.

---

## In the shell

| Command | What it does |
|---------|----------------|
| `help` | List all commands |
| `docs` | Open this wiki (Docs page) in your browser |
| `source` | Open the GitHub repository |
| `disclaimer` | Legal notice + Supabase data-storage disclosure |
| `forgefetch` | System info |
| `about` | About Forge OS |

---

## Supabase

Forge OS uses **[Supabase](https://supabase.com)** for cloud account storage. Passwords are stored as **salted SHA-256 hashes only** — never plain text.

Setup steps, `.env` configuration, and the `forge_users` schema are in the **[Documentation](Docs)** page.

---

## Disclaimer

Forge OS is a virtual OS for education and development — not a real operating system. Network and process commands are largely simulated. Account data may be stored in Supabase when configured. See **[Documentation → Disclaimer](Docs#disclaimer)** or run `disclaimer` in the shell.

---

## Next steps

→ Read the full **[Documentation](Docs)** for commands, auth, Supabase setup, and troubleshooting.

→ Star the repo: [github.com/axk42-op/ForgeOS](https://github.com/axk42-op/ForgeOS)
