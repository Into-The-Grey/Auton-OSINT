# 🧭 **Auton‑OSINT Phase 1 Roadmap: Foundation & Core Architecture**

## 🎯 **Phase Objective**

Establish the foundational structure for a modular, extensible OSINT toolchain that:

- Accepts various input types
- Uses powerful but free tools (Maigret, Sherlock, etc.)
- Normalizes results
- Correlates and visualizes data
- Prepares for both CLI and future GUI usage

---

### 🧱 **1. Input Type Mapping**

Define what kinds of inputs Auton-OSINT should accept:

| Input Type     | Description                           | Primary Module(s)          |
|----------------|---------------------------------------|-----------------------------|
| `username`     | Handles online usernames              | `username_search`          |
| `email`        | Validity + breach checking            | `email_verification`       |
| `phone`        | Phone info and carrier lookup         | `phone_lookup`             |
| `real name`    | Maps to social discovery              | `social_media_discovery`   |
| `domain/IP`    | Passive DNS and IP info               | `domain_ip_lookup`         |
| `address`      | (Planned) reverse lookup              | _TBD_                       |

---

### 🧩 **2. Module Design Pattern**

Each module was to follow this structure:

``` plaintext
modules/
├── email_verification/
│   ├── email_verification.py
│   ├── utils.py
│   └── __init__.py
├── username_search/
│   └── ...
```

- Each module reads input → runs a tool → normalizes output → saves to `data/outputs/`
- Configs live under `config/modules_config/*.yaml`
- Output is always in normalized JSON

---

### ⚙️ **3. Configuration System**

Centralized YAML config for:

- Each module’s settings (enabled, tool-specific toggles, URLs)
- Tor integration (global toggle, proxy address, service name)
- Compliance level (for legal/safety controls)

---

### 🕸️ **4. Tool Integration**

We scoped these tools as first-class integrations:

| Tool        | Use Case                        | Notes                                |
|-------------|----------------------------------|--------------------------------------|
| **Maigret** | Username OSINT                   | Primary, fallback to Sherlock        |
| **Sherlock**| Backup username scanner          | Only if Maigret fails                |
| **PhoneInfoga** | Phone lookups               | Optional integration                 |
| **HIBP API**| Breach lookups by email          | Optional if public API limits exist |
| **IPWhois / DNSPython** | Domain/IP lookups | Lightweight, no auth needed          |

---

### 🔄 **5. Data Normalization**

Output from each module is parsed and standardized into a common format like:

```json
{
  "input_type": "username",
  "username": "johndoe",
  "found_on": [
    {
      "site": "github.com",
      "url": "https://github.com/johndoe"
    }
  ]
}
```

---

### 🧠 **6. Correlation Engine**

- Scans `/data/outputs/*.json`
- Links related data (same phone/email on multiple services, reused usernames)
- Builds internal maps:
  - Username → services
  - Email → breaches
  - IP → domains
- Outputs to `correlated_results.json`

---

### 📊 **7. Graph Visualization**

- Uses `networkx` + `matplotlib`
- Draws nodes for entities (phones, usernames, domains, files)
- Colored by type
- Outputs static PNG to `/data/visualizations/`

---

### 🚀 **8. CLI Entry Point**

Initial CLI via `parser.py`, with:

- Dynamic input detection
- Optional explicit flags
- Tooltips for all arguments
- Batch input stub

---

### 🔒 **9. Compliance & Logging System**

- Toggleable **compliance level** (0–10) in config
- Logs for each run written to `/logs/`
- Tor support configurable per module or globally
- Logging of actions for traceability

---

### 📂 **10. Directory Structure**

``` plaintext
Auton-OSINT/
├── main.py
├── scripts/
│   ├── input_parser.py
│   ├── correlation_engine.py
│   └── visualization.py
├── modules/
├── config/
│   └── modules_config/
├── data/
│   ├── outputs/
│   ├── visualizations/
│   └── correlated_results.json
├── logs/
```

---
