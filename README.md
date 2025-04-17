# 🕵️ AUTON-OSINT

[![CI](https://github.com/Into-The-Grey/Auton-OSINT/actions/workflows/ci.yml/badge.svg)](https://github.com/Into-The-Grey/Auton-OSINT/actions/workflows/ci.yml)
[![Markdown Lint](https://github.com/Into-The-Grey/Auton-OSINT/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/Into-The-Grey/Auton-OSINT/actions/workflows/markdown-lint.yml)
[![Project Board](https://img.shields.io/badge/Project-Board-blue?logo=github)](https://github.com/users/Into-The-Grey/projects/10)

**Auton-OSINT** is a free, lightweight, and modular open-source intelligence (OSINT) framework for Linux. Designed for cybersecurity professionals, researchers, and enthusiasts, it provides deep reconnaissance using public sources, with optional Tor-based dark web scanning, no paid APIs, and a robust correlation/visualization engine.

---

## 🚀 Features

- 📦 Modular design — add/disable modules via config
- 🔍 Input types: Email, phone, username, domain, IP, real name, onion URLs
- 🌐 Tor/Darkweb support for anonymous or deep scans
- 📊 Graph-based correlation & relationship visualization
- 🔐 Security-first: secure mode, config validation, rate limiting
- 🧠 Headless or interactive CLI with optional HTML summary export
- 🧪 No paid APIs — 100% open source intelligence

### Features (Plain Text)

- Modular design — add/disable modules via config
- Input types: Email, phone, username, domain, IP, real name, onion URLs
- Tor/Darkweb support for anonymous or deep scans
- **Username Search** (via [Maigret](https://github.com/soxoj/maigret) for detailed profiling, with [Sherlock](https://github.com/sherlock-project/sherlock) as a fallback for username availability checks)
- Security-first: secure mode, config validation, rate limiting
- Headless or interactive CLI with optional HTML summary export
- No paid APIs — 100% open source intelligence

---

## ✅ Supported Modules

- **Email Verification** (MX, syntax, breach checks)
- **Username Search** (via Maigret, Sherlock fallback)
- **Phone Lookup** (NumVerify, PhoneInfoga)
- **Domain/IP Lookup** (DNS, IPWhois, passive tools)
- **Real Name Discovery** (Social media pattern-matching)
- **.onion Scan** (Tor-enabled module scanner)

---

## 🛠️ Quick Start

```bash
git clone https://github.com/Into-The-Grey/Auton-OSINT.git
cd Auton-OSINT
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 main.py --help
```

Example:

```bash
python3 main.py "johnsmith1995" --headless --output-summary json
# Replace "johnsmith1995" with the username, email, or other input type you want to investigate.
```

---

## ⚙️ Configuration

Each module has its own YAML config in:

``` yaml
config/modules_config/*.yaml
```

| Setting         | Description                     |
|----------------|---------------------------------|
| `enabled`       | Toggle module on/off            |
| `rate_limit`    | Optional cooldown between calls |
| `output_format` | Choose JSON, CSV, etc.          |
| `use_tor`       | Respect global or module TOR    |

Global config file: `config/main_config.yaml`

---

## 📁 Output Files

| Path                        | Description                              |
|-----------------------------|------------------------------------------|
| `data/outputs/`             | Individual module results                |
| `data/correlated_results.json` | Normalized & cross-linked entity data |
| `data/visualizations/`      | Graphs from `networkx`/`matplotlib`      |
| `logs/`                     | Logs per run & per module                |
| `.last_run.json`            | Cache of latest successful CLI run       |

---

## 🔒 Security & Requirements

- Python 3.12+
- Tor (system daemon or embedded client)
- Git
- Ubuntu or Debian-based Linux (recommended)

### Installation Instructions

1. **Python 3.12+**: Install the latest version of Python from [python.org](https://www.python.org/downloads/) or use your package manager:

   ```bash
   sudo apt update && sudo apt install -y python3 python3-venv python3-pip
   ```

2. **Tor**: Install Tor using the following commands:

   ```bash
   sudo apt update && sudo apt install -y tor
   sudo systemctl start tor
   sudo systemctl enable tor
   ```

3. **Git**: Install Git with:

   ```bash
   sudo apt update && sudo apt install -y git
   ```

4. **Ubuntu/Debian-based Linux**: Ensure your system is up-to-date:

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

## 📦 Development & Automation

- 📋 GitHub Project: [Auton-OSINT Dev Flow](https://github.com/users/Into-The-Grey/projects/10)
- ✅ [CI Workflow](.github/workflows/ci.yml)
- 📄 Auto Markdown Linting & Doc Hygiene
- 🔄 Weekly dependency checks via Dependabot

---

## 📸 Demo Preview

> Comming soon!

---

## ❤️ Credits

Built with 💻 by **[REDACTED]** and contributors.  
Inspired by tools like SpiderFoot — reimagined with speed and simplicity.

---

## 📄 License

**MIT License** — see [LICENSE](LICENSE) for full details.

---
