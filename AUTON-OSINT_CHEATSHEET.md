# 🧠 AUTON-OSINT Cheat Sheet

> One-page quick reference for using the Auton-OSINT CLI tool.

---

## 🛠️ Run Modes

| Flag                  | Description                                                             |
|-----------------------|-------------------------------------------------------------------------|
| `--headless`          | Skip visualizations (for CLI/headless use).                             |
| `--skip-correlation`  | Skip the correlation engine, just run lookups.                          |
| `--output-summary`    | Output a summary (Markdown/JSON/CSV) after scans.                       |
| `--batch-input`       | Run a file of inputs (phones, emails, etc.) in batch mode.              |
| `--no-tor`            | Disable Tor integration for faster scans.                               |
| `--silent`            | Suppress most CLI messages except errors.                              |
| `--visualize-only`    | Only run the visualizer on the latest results.                          |

---

## 🔍 Input Routing

| Input Format         | Routed Module            |
|----------------------|--------------------------|
| `email@example.com`  | Email Verification        |
| `@username`          | Username Search           |
| `John Doe`           | Social Media Discovery    |
| `8.8.8.8`            | Domain/IP Lookup          |
| `example.com`        | Domain/IP Lookup          |
| `123-456-7890`       | Phone Lookup              |
| `.onion URL`         | Tor/Darkweb Integration   |

---

## 🔒 Security & Logging

| Feature               | Description                                                       |
|-----------------------|-------------------------------------------------------------------|
| `--secure`            | Activates CLI password prompt + rate limiting                    |
| Log Files             | Stored in `/logs/` by default                                    |
| `.last_run.json`      | Cached summary of the last full OSINT session                    |
| Config Checksum       | Ensures configs haven’t been tampered with (auto verified)       |

---

## 📈 Post-Run Options

- Generate HTML Dashboard Report
- Correlation Summary Stored in `correlated_results.json`
- Graph stored in `/graphs/` directory

---

## 🧪 Debug / Dev Flags

| Flag             | Description                           |
|------------------|---------------------------------------|
| `--debug`        | Verbose output + tracebacks.          |
| `--module-test`  | Runs module tests only.               |
| `--timing`       | Show module execution time.           |

---
