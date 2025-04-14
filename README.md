# 🕵️ AUTON-OSINT

**Auton-OSINT** is a free, lightweight, and modular open-source intelligence (OSINT) framework built for Linux. It provides deep reconnaissance using public sources, with optional Tor-based dark web scanning, no paid APIs, and robust correlation/visualization tools.

---

## 🚀 Features

- 📦 Modular design: Add/disable any module via config.
- 🔍 Input types: Email, phone, username, domain, IP, real name, onion URLs.
- 🌐 Tor/Darkweb support: Toggle integration for deeper investigations.
- 📊 Graph-based correlation engine.
- 🔐 Security: Rate limiting, secure mode, logging with config hash validation.
- 🧠 Visualize: Export interactive HTML dashboards or run CLI-only.
- 🧪 No paid APIs. Ever.

---

## 🧪 Supported Modules

- **Email Verification**
- **Username Search** (Maigret, Sherlock fallback)
- **Phone Lookup**
- **Domain/IP Lookup**
- **Real Name Discovery** (Social Media / Public Profiles)
- **Darkweb .onion Scan** (Tor Integration)

---

## 🛠️ Quick Start

```bash
git clone https://github.com/Into_The_Grey/auton-osint.git
cd auton-osint
python3 main.py --help
```

Example:

```bash
python3 main.py "johnsmith1995" --headless --output-summary
```

---

## 🔧 Configurable Settings

Stored in `config/modules_config/*.yaml`.

Each module has:

- Enable/disable toggle
- Optional rate limiting
- Source customization
- Output format (`json`, `csv`)

---

## 📁 Output Files

| File                        | Description                             |
|-----------------------------|-----------------------------------------|
| `data/outputs/`             | Raw and parsed module output            |
| `correlated_results.json`   | Unified correlation data                |
| `graphs/`                   | Visual network graphs (if enabled)      |
| `.last_run.json`            | Cached latest session                   |
| `logs/`                     | Daily logs for review/auditing          |

---

## ⚙️ Requirements

- Python 3.12+
- Tor (for .onion scans)
- Git
- Linux (Debian/Ubuntu recommended)

---

## 📌 Notes

- CLI-first design. Web interface is optional (planned).
- No paid APIs used anywhere in the tool.
- Safe defaults, but adjustable compliance levels available.

---

## ❤️ Credits

Built with love by [Mr. Acord] and contributors. Inspired by SpiderFoot, simplified for real-world speed and focus.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---
