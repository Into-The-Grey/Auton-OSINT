# modules/tor_darkweb_integration/utils.py

import yaml
import subprocess
import requests
import logging
from pathlib import Path
from typing import List

ROOT_DIR = Path(__file__).parents[2]
CONFIG_PATH = ROOT_DIR / "config/modules_config/tor_darkweb_config.yaml"
LOG_PATH = ROOT_DIR / "logs/tor_darkweb.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# === Load Config ===
def load_tor_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f).get("tor_darkweb", {})


TOR_CONFIG = load_tor_config()


# === Systemctl Controls ===
def start_tor():
    try:
        logging.info("Starting Tor...")
        subprocess.run(
            ["systemctl", "start", TOR_CONFIG["systemctl_service"]], check=True
        )
    except Exception as e:
        logging.error(f"Failed to start Tor: {e}")


def stop_tor():
    try:
        logging.info("Stopping Tor...")
        subprocess.run(
            ["systemctl", "stop", TOR_CONFIG["systemctl_service"]], check=True
        )
    except Exception as e:
        logging.error(f"Failed to stop Tor: {e}")


def restart_tor():
    try:
        logging.info("Restarting Tor...")
        subprocess.run(
            ["systemctl", "restart", TOR_CONFIG["systemctl_service"]], check=True
        )
    except Exception as e:
        logging.error(f"Failed to restart Tor: {e}")


# === Status Check ===
def is_tor_enabled():
    return TOR_CONFIG.get("is_enabled", False)


def get_proxy_session():
    proxy = TOR_CONFIG.get("proxy_url", "socks5h://127.0.0.1:9050")
    s = requests.Session()
    s.proxies = {"http": proxy, "https": proxy}
    s.verify = TOR_CONFIG.get("verify_https", True)
    return s


def test_onion_access(onion_url: str) -> bool:
    try:
        timeout = TOR_CONFIG.get("timeout", 10)
        session = get_proxy_session()
        resp = session.get(onion_url, timeout=timeout)
        return resp.status_code == 200
    except Exception as e:
        logging.warning(f"Failed to reach {onion_url} over Tor: {e}")
        return False


def test_known_onions() -> List[str]:
    failures = []
    test_urls = TOR_CONFIG.get("test_onions", [])
    for url in test_urls:
        if not test_onion_access(url):
            failures.append(url)
    return failures
