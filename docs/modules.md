# 🧩 OSINT Modules Overview

This document outlines the structure, function, and configuration of each module available in **Auton-OSINT**.

---

## 🔍 Input → Output Chain

Each module follows this pattern:

1. **Input** — Passed from the input parser
2. **Execution** — Executes tools/APIs or scrapers
3. **Normalization** — Output is parsed into unified JSON
4. **Storage** — Data saved under `/data/outputs/`
5. **(Optional)** Correlation & visualization

All modules are enabled/disabled via their own YAML files in `config/modules_config/`.

---

## 📦 Available Modules

### 1. `email_verification`

- **Input**: `email@example.com`
- **Tools Used**: HIBP API, MX record checkers
- **Output**: JSON w/ syntax validity, domain health, breach exposure
- **Config**:

  ```yaml
  enabled: true
  use_tor: false
  output_format: json
  rate_limit: 2
  ```

---

### 2. `username_search`

- **Input**: `@username`
- **Tools Used**: Maigret (primary), Sherlock (fallback)
- **Features**: Optional Tor routing
- **Output**: Detected platforms, timestamps, metadata
- **Config**:

  ```yaml
  enabled: true
  use_tor: true
  timeout: 60
  sites_limit: 300
  ```

---

### 3. `phone_lookup`

- **Input**: `+15551234567`
- **Tools Used**: NumVerify, PhoneInfoga, regex filters
- **Output**: Country, carrier, line type, region
- **Config**:

  ```yaml
  enabled: true
  cache_hits_only: true
  validate_country: US
  ```

---

### 4. `domain_ip_lookup`

- **Input**: `example.com` or `8.8.8.8`
- **Tools Used**: DNS, whois, IPWhois, reputation APIs
- **Output**: Registry info, nameservers, ASN, geoIP
- **Config**:

  ```yaml
  enabled: true
  output_format: json
  include_dnssec: false
  ```

---

### 5. `social_media_discovery`

- **Input**: `"John Smith"`, name or alias
- **Tools Used**: Pattern-based scrapers (from YAML)
- **Output**: Found profile URLs, hit metadata
- **Config**:

  ```yaml
  enabled: true
  platforms:
    - linkedin
    - facebook
    - twitter
  require_match: true
  use_tor: true
  ```

---

### 6. `tor_darkweb_integration`

- **Input**: `.onion URLs` or modules flagged to use Tor
- **Function**: Controls the Tor routing, port binding, and client start/stop
- **Config**:

  ```yaml
  enabled: true
  control_port: 9051
  socks_port: 9050
  use_existing_instance: false
  ```

---

## ⚙️ Module Best Practices

- Each module has a `main.py` file and optionally a `utils.py`
- Logs should be saved to `/logs/{module}/`
- Output files go to `/data/outputs/`
- Avoid hardcoding: configs live in YAML
- Respect CLI flags passed by `main.py`

---

Need to create a new module? See [dev_guide.md](dev_guide.md)
