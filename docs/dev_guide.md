# 🧪 Developer Guide: Extending Auton-OSINT

This guide walks you through the process of adding new modules, debugging existing ones, and working with CLI arguments during development.

---

## ⚙️ Module Creation Checklist

1. **Create a new folder in `modules/`**

   ```bash
   mkdir modules/new_module_name
   ```

2. **Add required files**:
   - `main.py` — core logic
   - `utils.py` — optional helpers
   - `config/modules_config/new_module_name.yaml`
   - Add an entry to your `README.md` or `modules.md`

3. **Structure**:

   ``` bash
   modules/
     └── new_module_name/
         ├── main.py
         ├── utils.py (optional)
         └── __init__.py
   ```

4. **Expected Output Format**:
   Every module should output to `/data/outputs/` with this JSON format:

   ```json
   {
     "type": "username",
     "value": "johnsmith",
     "source": "maigret",
     "timestamp": "2025-04-16T18:42:00Z",
     "metadata": {...}
   }
   ```

---

## 🧪 Testing & Debugging Modules

- **Run a single module manually:**

  ```bash
  python3 modules/username_search/main.py "target_username"
  ```

- **Enable debug output:**
  Use the CLI flag `--debug`

- **Module Logging:**
  Write logs to `logs/<module_name>.log` using the shared logger

---

## 🧵 Adding CLI Arguments

If your module needs new CLI flags:

1. Modify `main.py`'s `argparse` section
2. Add logic in `main()` to dispatch or pass to submodules
3. Document them in the README or usage screen

Example:

```python
parser.add_argument('--depth', type=int, default=1, help='Depth of search')
```

---

## 🗃️ Configuration Tips

- All modules must read from their YAML config via `PyYAML`
- Avoid hardcoded URLs, timeouts, or thresholds
- Allow overrides from CLI

Example config usage:

```python
import yaml
with open('config/modules_config/username_search.yaml') as f:
    config = yaml.safe_load(f)
```

---

## 🧼 Optional Enhancements

- Add retry logic using `tenacity`
- Use `requests-cache` to throttle APIs
- Store credentials in `.env` (never in source)
- Include docstring headers for functions and classes

---

For module config structure, see [config_reference.md](config_reference.md)
