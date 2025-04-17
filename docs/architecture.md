# 🏗️ Auton-OSINT Architecture Overview

This document outlines the internal flow of the Auton-OSINT framework — from data ingestion to module execution, correlation, and visualization.

---

## 🔁 System Flow Diagram (Conceptual)

``` mermaid
[ CLI Input / Batch File ]
         │
         ▼
[ input_parser.py ] ──► detects input type (email, phone, etc.)
         │
         ▼
[ Dynamic Module Dispatcher ]
         │
         ├─► [ email_verification ]
         ├─► [ username_search ]
         ├─► [ domain_ip_lookup ]
         └─► [ ...other modules ]
         ▼
[ Normalized JSON Output ] (in /data/outputs/)
         ▼
[ correlation_engine.py ]
         ▼
[ correlated_results.json ]
         ▼
[ visualization.py ]
         ▼
[ PNG Graph in /data/visualizations/ ]
```

---

## 📦 Key Components

### `main.py`

- Central CLI interface
- Routes arguments to the parser or visualization
- Controls secure mode, headless, tor toggles, batch vs single input

### `input_parser.py`

- Inspects CLI input or file line-by-line
- Classifies input: email, domain, IP, username, name, phone
- Sends task to dispatcher

### `modules/`

- Each folder is an isolated scanning module
- Shared structure: `main.py`, `utils.py`, `config.yaml`
- Results written to `/data/outputs/`

### `config/`

- `main_config.yaml`: Global flags and CLI overrides
- `modules_config/*.yaml`: Per-module settings and flags

### `correlation_engine.py`

- Scans `/data/outputs/`
- Extracts shared fields (emails, phones, domains, usernames)
- Builds relationships and writes `correlated_results.json`

### `visualization.py`

- Uses `networkx` and `matplotlib`
- Renders entity graph with node types and connections
- Saves to `/data/visualizations/`

---

## 🔄 CLI Options → Runtime Behavior

| CLI Flag               | Affects                     |
|------------------------|-----------------------------|
| `--headless`           | Skips visualization         |
| `--skip-correlation`   | Bypasses engine             |
| `--output-summary`     | Writes formatted report     |
| `--no-tor`             | Disables Tor across modules |
| `--secure`             | Prompts password lock       |

---

## 🔐 Security Layers

- Password lock mode for sensitive ops
- Tor routing per-module with config control
- YAML integrity validated via checksum in secure mode
- Logs and session caches are auto-cleared in secure runs (planned)

---

## 🛠️ Design Philosophy

- Modular by default: drop-in new modules
- CLI-first but GUI/web-ready
- No cloud dependencies or paywalls
- Docs, configs, and tests all versioned

---

For expanding modules or data flow: see [dev_guide.md](dev_guide.md)
