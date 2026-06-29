# Forge OS

> A Python-powered virtual operating system for developers.

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?style=for-the-badge\&logo=python)
![Status](https://img.shields.io/badge/Status-Development-orange?style=for-the-badge)
![License](https://img.shields.io/github/license/axk42-op/ForgeOS?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-00C853?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Alpha-orange?style=for-the-badge)

---

## What is Forge OS?

Forge OS is an open-source virtual operating system built entirely in Python.

Unlike a traditional operating system, Forge OS runs as a Python application while providing its own operating system environment. It is designed for learning, experimentation, software development, and testing operating system concepts without interacting directly with computer hardware.

The project focuses on creating a developer-first environment featuring its own shell, virtual filesystem, package manager, user management, applications, and desktop environment.

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

# Features

## Current

* Custom boot sequence
* Forge Shell
* Kernel manager
* Virtual filesystem
* User management
* Package manager
* Boot banner
* Modular architecture

---

## Planned

### Shell

* Command history
* Auto-completion
* Aliases
* Environment variables
* Pipes
* Redirection

### Filesystem

* Virtual directories
* File permissions
* Symbolic links
* Mount points

### Package Manager

* forgepkg install
* forgepkg remove
* forgepkg update
* Package repositories
* Dependency resolution

### Applications

* Terminal
* File Manager
* Settings
* Calculator
* Text Editor

### Developer Tools

* Git integration
* Python support
* Node.js support
* npm support
* Package SDK

### Desktop

* Window manager
* Taskbar
* Notifications
* Themes
* Widgets

---

# Planned Applications

* vi
* Vim
* Neovim
* Vimge
* Forge (editor)
* Forgium (browser)

---

# Project Structure

```text
Forge/
│
├── boot.py
├── kernel/
├── shell/
├── filesystem/
├── users/
├── packages/
├── config/
├── system/
└── assets/
```

---

# Goals

* Learn operating system architecture
* Build a modular shell
* Design a virtual filesystem
* Create a package ecosystem
* Develop a desktop environment
* Build developer-focused applications
* Experiment with software architecture

---

# Technologies

* Python 3.14+
* Rich
* Prompt Toolkit
* uv
* TOML

---

# Running Forge OS

```bash
uv run boot.py
```

or

```bash
python boot.py
```

---

# Development Status

Forge OS is currently under active development.

The project is evolving rapidly, and many features are experimental.

---

# Contributing

Contributions, ideas, bug reports, and feature requests are welcome.

If you'd like to help improve Forge OS, feel free to open an issue or submit a pull request.

---

# License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.

---

# Disclaimer

Forge OS is **not** a real operating system or kernel.

It is a Python-powered virtual operating system designed for education, experimentation, software architecture, and software development. Forge OS runs as a standard Python application while providing its own virtual operating system environment.

---

## Roadmap

* [x] Boot System
* [x] Kernel Manager
* [x] Forge Shell
* [ ] Virtual Filesystem
* [ ] User Management
* [ ] Package Manager (`forgepkg`)
* [ ] Process Manager
* [ ] Application Framework
* [ ] Desktop Environment
* [ ] Forge Editor
* [ ] Vimge
* [ ] Forgium Browser
* [ ] Plugin SDK

---

## Author

Developed by **ayaan global**.

Forge OS is an open-source project created to explore operating system concepts, software architecture, shell development, virtual filesystems, and developer tooling through a modular Python-based virtual operating system.


## Author

**ayaan global**

Building Forge OS as an open-source platform for learning software architecture, shell development, virtual filesystems, package management, and developer tooling.
