# ⚙️ Configuration Reference

This document outlines all major configuration options for both global and per-module YAML files used in Auton-OSINT.

---

## 🗃️ Global Configuration

File: `config/main_config.yaml`

| Key                  | Type    | Description                                        |
|----------------------|---------|----------------------------------------------------|
| `tor_enabled`        | bool    | Enables/disables Tor across all modules            |
| `log_level`          | string  | Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`       |
| `secure_mode`        | bool    | Enables password lock, secure CLI mode             |
| `default_output_fmt` | string  | Default output format if not set per-module        |
| `run_batch_parallel` | bool    | If true, batch inputs are processed concurrently    |

Example:

```yaml
tor_enabled: true
log_level: INFO
secure_mode: false
default_output_fmt: json
run_batch_parallel: true
```

---

## 🧩 Module Configuration Files

Located in: `config/modules_config/*.yaml`

Each module’s config defines its runtime behavior.

### Common Keys

| Key              | Type    | Description                                      |
|------------------|---------|--------------------------------------------------|
| `enabled`        | bool    | Enables or disables the module                   |
| `use_tor`        | bool    | Forces Tor proxy for this module                 |
| `output_format`  | string  | Output format: `json`, `csv`, etc.               |
| `rate_limit`     | int     | Delay (in seconds) between requests              |
| `sources`        | list    | Optional list of data sources or tools to use    |

Example:

```yaml
enabled: true
use_tor: true
output_format: json
rate_limit: 2
sources:
  - maigret
  - sherlock
```

---

### Special Module Keys

Some modules support additional flags.

#### `username_search.yaml`

```yaml
sites_limit: 300
timeout: 60
fallback_enabled: true
```

#### `email_verification.yaml`

```yaml
hibp_enabled: true
validate_mx: true
skip_temp_domains: true
```

#### `phone_lookup.yaml`

```yaml
validate_country: "US"
cache_hits_only: true
```  

---

## 🧪 Tips for Managing Configs

- Keep all `*.yaml` configs under version control
- Use meaningful defaults
- Avoid API keys in YAML (use `.env` instead)
- Use `pyyaml` for loading:

  ```python
  with open("config/modules_config/phone_lookup.yaml") as f:
      config = yaml.safe_load(f)
  ```

---

For developer integration instructions, see [dev_guide.md](dev_guide.md).
