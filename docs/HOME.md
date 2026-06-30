# Forge OS Wiki

Welcome to **Forge OS v1.0** — documentation for the Python virtual operating system.

---

## Quick links

| Link | Description |
|------|-------------|
| [Documentation](Docs) | Full command reference, setup, troubleshooting |
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
- **User management** and local login (salted password hashes)
- **Package manager** — `forgepkg`

---

## Quick start

```cmd
git clone https://github.com/axk42-op/ForgeOS.git
cd ForgeOS
uv venv
uv pip install -r requirements.txt
uv pip install -e .
python boot.py
```

First launch: create an account. Later runs: sign in.

Debug in one window: `python boot.py --session`

---

## In the shell

| Command | What it does |
|---------|----------------|
| `help` | List all commands |
| `docs` | Open wiki docs in your browser |
| `source` | Open the GitHub repository |
| `disclaimer` | Legal notice + local storage disclosure |
| `forgefetch` | System info |
| `about` | About Forge OS |

---

## Disclaimer

Forge OS is a virtual OS for education and development — not a real operating system. Network and process commands are largely simulated. Account credentials are stored **locally** on your machine only. Run `disclaimer` in the shell for the full notice.

---

## Next steps

→ Read the full **[Documentation](Docs)** for commands, auth, and troubleshooting.

→ Star the repo: [github.com/axk42-op/ForgeOS](https://github.com/axk42-op/ForgeOS)
