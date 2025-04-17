# Phase 3: Core Module Development

This document serves as a GitHub PR draft covering the file/folder structure, code stubs, configuration templates, unit test outlines, logging examples, and documentation updates required for Phase 3 of the Auton‑OSINT project.

---

## 📁 Project Structure (Phase 3)

``` plaintext
Auton-OSINT/
├── modules/
│   ├── input_parser.py
│   ├── domain_ip_lookup.py
│   ├── email_verification.py
│   ├── username_search.py
│   └── __init__.py
├── tests/
│   ├── test_input_parser.py
│   ├── test_domain_ip_lookup.py
│   ├── test_email_verification.py
│   └── test_username_search.py
├── config/
│   └── modules_config/
│       └── email_verification_config.yaml
├── logs/
│   ├── main_system.log
│   ├── domain_module.log
│   ├── email_module.log
│   └── username_module.log
└── README.md  (update Phase 2 instructions)
```  

---

### 1. Module: Input Parsing & Dynamic Recognition

**File:** `modules/input_parser.py`

```python
import argparse
import logging
from typing import List, Dict

logger = logging.getLogger('input_parser')

class InputParser:
    """
    Parses raw CLI/web inputs and dispatches to OSINT modules.

    Usage:
        parser = InputParser()
        results = parser.parse(['--email', 'foo@bar.com', '--username', 'Alice'])
    """
    def __init__(self):
        self._setup_argparse()

    def _setup_argparse(self) -> None:
        self.arg_parser = argparse.ArgumentParser(prog='auton-osint')
        self.arg_parser.add_argument('--email', nargs='+', help='Email address(es)')
        self.arg_parser.add_argument('--username', nargs='+', help='Username(s)')
        self.arg_parser.add_argument('--domain', nargs='+', help='Domain(s)')
        self.arg_parser.add_argument('--ip', nargs='+', help='IP address(es)')
        # Add more types as needed

    def parse(self, args: List[str]) -> Dict[str, List[str]]:
        parsed = vars(self.arg_parser.parse_args(args))
        output: Dict[str, List[str]] = {}
        for key, values in parsed.items():
            if values:
                normalized = [v.strip() for v in values if v]
                output[key] = normalized
                logger.info(f"Parsed {key}: {normalized}")
        return output
```

**Logging Setup:**

```python
import logging
logging.basicConfig(
    filename='logs/main_system.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s]: %(message)s'
)
```

---

### 2. Module: Domain & IP Lookup

**File:** `modules/domain_ip_lookup.py`

```python
import time
import logging
from datetime import datetime
import whois
import requests

logger = logging.getLogger('domain_ip_lookup')

class DomainIPLookup:
    """
    Provides WHOIS, DNS records, geolocation, and port data.
    """

    RETRY_DELAYS = [1, 2, 5]

    def lookup_domain(self, domain: str) -> dict:
        for delay in self.RETRY_DELAYS:
            try:
                w = whois.whois(domain)
                # DNSRecon or similar for records
                records = {}  # placeholder
                data = {
                    'module': 'domain',
                    'input': domain,
                    'timestamp': datetime.utcnow().isoformat(),
                    'data': {
                        'whois': w.text,
                        'records': records
                    }
                }
                logger.info(f"Domain lookup success: {domain}")
                return data
            except Exception as e:
                logger.warning(f"WHOIS failed for {domain}, retrying in {delay}s...")
                time.sleep(delay)
        logger.error(f"Domain lookup failed: {domain}")
        return {}

    def lookup_ip(self, ip: str) -> dict:
        url = f'http://ip-api.com/json/{ip}'
        resp = requests.get(url)
        geo = resp.json()
        # Shodan InternetDB API for ports (free)
        shodan_url = f'https://api.shodan.io/internetdb/{ip}'
        shodan_resp = requests.get(shodan_url)
        ports = shodan_resp.json().get('ports', [])
        data = {
            'module': 'ip',
            'input': ip,
            'timestamp': datetime.utcnow().isoformat(),
            'data': {
                'geolocation': geo,
                'open_ports': ports
            }
        }
        logger.info(f"IP lookup success: {ip}")
        return data
```

**Logging Setup:**

```python
logging.getLogger('domain_ip_lookup').setLevel(logging.INFO)
# write to logs/domain_module.log via handlers
```

---

### 3. Module: Email & Username OSINT

#### a) Email Verification Module

**File:** `modules/email_verification.py`

```python
import yaml
import logging
from typing import Dict
import requests

logger = logging.getLogger('email_verification')

class EmailVerifier:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        self.api_key = cfg.get('emailrep_api_key')

    def verify_email(self, email: str) -> Dict:
        # EmailRep.io
        headers = {'Key': self.api_key}
        rep = requests.get(f'https://emailrep.io/{email}', headers=headers).json()
        # holehe local
        # e.g., subprocess.run([...])
        sites = []  # placeholder
        result = {
            'module': 'email',
            'input': email,
            'timestamp': datetime.utcnow().isoformat(),
            'data': {
                'reputation': rep,
                'associated_sites': sites
            }
        }
        logger.info(f"Verified email: {email}")
        return result
```

**Config Template:** `config/modules_config/email_verification_config.yaml`

```yaml
# Email Verification Module Configuration
tools:
  emailrep_api_key: 'YOUR_EMAILREP_API_KEY'
  holehe_path: '/usr/local/bin/holehe'
```  

**Logging Setup:**

```python
logging.getLogger('email_verification').addHandler(
    logging.FileHandler('logs/email_module.log')
)
```

#### b) Username Search Module

**File:** `modules/username_search.py`

```python
import logging
import subprocess
from datetime import datetime

logger = logging.getLogger('username_search')

class UsernameSearcher:
    def __init__(self, use_tor: bool = False):
        self.use_tor = use_tor

    def search_username(self, username: str) -> dict:
        cmd = ['sherlock', username, '--output', 'json']
        if self.use_tor:
            cmd.insert(0, 'torsocks')
        proc = subprocess.run(cmd, capture_output=True, text=True)
        data = proc.stdout  # parse JSON
        result = {
            'module': 'username',
            'input': username,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data
        }
        logger.info(f"Username search completed: {username}")
        return result
```

**Logging Setup:**

```python
logging.getLogger('username_search').addHandler(
    logging.FileHandler('logs/username_module.log')
)
```

---

### 4. Unit Test Outlines (`pytest`)

#### tests/test_input_parser.py

```python
import pytest
from modules.input_parser import InputParser

def test_parse_single_email():
    p = InputParser()
    res = p.parse(['--email', 'foo@bar.com'])
    assert res['email'] == ['foo@bar.com']

def test_parse_multiple():
    p = InputParser()
    res = p.parse(['--email', 'a@b.com', 'c@d.com', '--ip', '1.2.3.4'])
    assert 'ip' in res and 'email' in res

def test_invalid_ip_format(caplog):
    p = InputParser()
    # assume we add validation to error on invalid IP
    res = p.parse(['--ip', 'not_an_ip'])
    assert 'ip' not in res
    assert 'ERROR' in caplog.text
```

#### tests/test_domain_ip_lookup.py

```python
import pytest
from modules.domain_ip_lookup import DomainIPLookup

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
    def json(self):
        return self._json

@pytest.fixture(autouse=True)
def patch_requests(monkeypatch):
    monkeypatch.setattr('modules.domain_ip_lookup.requests.get', lambda url: DummyResponse({'status': 'success'}))


def test_lookup_ip_success(monkeypatch):
    d = DomainIPLookup()
    result = d.lookup_ip('8.8.8.8')
    assert result['module'] == 'ip'
    assert 'geolocation' in result['data']
```

#### tests/test_email_verification.py

```python
import pytest
from modules.email_verification import EmailVerifier

def test_verify_email(monkeypatch, tmp_path):
    cfg = tmp_path / 'cfg.yaml'
    cfg.write_text("emailrep_api_key: 'KEY'\nholehe_path: '/bin/holehe'\n")
    ev = EmailVerifier(str(cfg))
    monkeypatch.setattr('modules.email_verification.requests.get', lambda url, headers={}: type('R', (), {'json': lambda s: {'reputation': 'ok'}})())
    res = ev.verify_email('test@example.com')
    assert res['module'] == 'email'
```

#### tests/test_username_search.py

```python
import pytest
from modules.username_search import UsernameSearcher

class DummyProc:
    stdout = '{"found": []}'

@pytest.fixture(autouse=True)
def patch_subprocess(monkeypatch):
    monkeypatch.setattr('modules.username_search.subprocess.run', lambda *args, **kwargs: DummyProc())


def test_search_username():
    us = UsernameSearcher()
    res = us.search_username('user123')
    assert res['module'] == 'username'
    assert 'found' in res['data']
```

---

### 5. Documentation Updates

- **Phase 1 Architecture Doc:**
  - Add `timestamp` field to JSON schema.
  - Include `module` and `input` keys in normalized output.

- **Phase 2 `modules.md` / README:**
  - List new stubs under "Phase 3 Core Modules":
    - InputParser usage and flags
    - Domain/IP lookup instructions (needs API keys for Shodan)
    - Email / Username modules dependencies
  - Instructions to run `pytest tests/` for module tests.

---

### 6. Next Steps (Phase 4)

1. **Central Database Ingestion:**
   - Feed module outputs into the SQLite cache; implement `DatabaseManager.insert(record)`.

2. **Correlation Engine Integration:**
   - Enable grouping of related records across modules.

3. **Recursive & Chained Searches:**
   - Trigger new searches based on intermediate findings (e.g., domain found in email sites).

4. **Web Interface Hooks:**
   - Expose REST endpoints for each module through `webapp.py`.

5. **Configuration & Scheduling:**
   - Allow background tasks and timed re-scans via cron or APScheduler.

---
