# Auton-OSINT Phase 2: Initial Setup & Environment Configuration

## 1. Environment Setup

### Ubuntu Development Environment Setup

```bash
# Update package index and upgrade installed packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, and Git
sudo apt install -y python3 python3-pip python3-venv git

# Verify installations
python3 --version
pip3 --version
git --version

# Create and activate Python virtual environment
mkdir -p ~/Auton-OSINT
cd ~/Auton-OSINT
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install essential Python libraries
pip install argparse rich requests PyYAML sqlalchemy sqlite3
```

## 2. Proposed Directory Structure

``` plaintext
/home/ncacord/Auton-OSINT/
├── venv/
├── config/
│   └── config.yaml
├── modules/
│   ├── username/
│   │   ├── config.yaml
│   │   ├── username_lookup.py
│   │   └── logs/
│   ├── email/
│   │   ├── config.yaml
│   │   ├── email_lookup.py
│   │   └── logs/
│   └── ... (additional modules)
├── utils/
│   ├── db.py
│   └── parser.py
├── logs/
│   └── auton_osint.log
├── data/
│   └── auton_osint.db
├── main.py
├── requirements.txt
└── README.md
```

## 3. Version Control & CI/CD Setup

### Git Initialization

```bash
git init
echo "venv/" > .gitignore
echo "logs/" >> .gitignore
echo "data/" >> .gitignore
git add .
git commit -m "Initial commit – Auton-OSINT project setup"
```

### Branching Strategy

- **Main branch**: Production-ready code
- **Development branch**: Integrating new features and modules
- **Feature branches**: Individual features/modules

### CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/ci.yml`

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Linter
        run: |
          pip install flake8
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Pre-commit Hooks and Standards

- Use `flake8` for linting:

```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pycqa/flake8
    rev: stable
    hooks:
      - id: flake8
```

## 4. Basic CLI Framework

### CLI Implementation (`main.py`)

```python
import argparse
import logging
from rich.logging import RichHandler
import yaml

# Logging setup
logging.basicConfig(
    level="INFO",
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[RichHandler(), logging.FileHandler('logs/auton_osint.log')]
)
logger = logging.getLogger("Auton-OSINT")

def load_config(path='config/config.yaml'):
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def main():
    parser = argparse.ArgumentParser(description="Auton-OSINT CLI")
    parser.add_argument('-gui', '--gui', action='store_true', help='Run with GUI interface')
    parser.add_argument('-web', '--web', metavar='host:port', help='Run web interface on specified host and port')
    parser.add_argument('-i', '--input', required=True, help='Input data for OSINT modules')
    args = parser.parse_args()

    config = load_config()

    if args.gui:
        logger.info("Launching GUI mode...")
        # Placeholder for future GUI implementation

    elif args.web:
        host, port = args.web.split(':')
        logger.info(f"Launching Web UI at {host}:{port}")
        # Placeholder for future web UI implementation

    else:
        logger.info(f"Processing input: {args.input}")
        # Dynamic input parsing and module execution placeholder

if __name__ == '__main__':
    main()
```

## 5. Recommendations & Modifications to Phase 1

- **Dependencies Addition**: Explicitly include `rich`, `sqlalchemy`, and `sqlite3` in documentation.
- **Directory Structure Adjustment**: Clearly defined per-module logs folders to improve modularity.
- **Logging Configuration**: Standardized logging setup using Rich.

## Integration & Support for Future Phases

This setup facilitates:

- **Modularity**: Easy addition and management of modules.
- **Robust Logging**: Comprehensive logging for debugging and maintenance.
- **Automation**: GitHub Actions for automated testing and linting, improving stability and reliability.
- **Flexibility**: CLI framework scalable for GUI and web interfaces.
- **Continuous Development**: Clear roadmap and structure for contributors and future module integration.
