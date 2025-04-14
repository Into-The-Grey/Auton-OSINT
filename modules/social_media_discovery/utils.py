import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional
import requests
import json

# === SETUP ===
ROOT_DIR = Path(__file__).parents[2]
CONFIG_PATH = ROOT_DIR / "config/modules_config/social_media_discovery_config.yaml"
TOR_CONFIG_PATH = ROOT_DIR / "config/modules_config/tor_darkweb_config.yaml"
LOG_PATH = ROOT_DIR / "logs/social_media_discovery.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# === LOAD CONFIGS ===
def load_social_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)["social_media_discovery"]


def load_tor_config():
    with open(TOR_CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


CONFIG = load_social_config()
TOR_CONFIG = load_tor_config()


# === PLATFORM HELPERS ===
def get_enabled_platforms(config_path=None):
    """Return a list of enabled platforms and their full settings."""
    config = load_social_config()
    return {
        name: info
        for name, info in config.get("platforms", {}).items()
        if info.get("is_enabled", False)
    }


def generate_platform_urls(
    platforms: dict,
    username: str,
    user_id: Optional[str] = None,
    discriminator: Optional[str] = None,
):
    urls = []
    for site, info in platforms.items():
        url = None
        if "url_pattern" in info:
            url = info["url_pattern"].format(username=username)
        elif "url_pattern_username" in info:
            url = info["url_pattern_username"].format(username=username)
        elif "url_pattern_userid" in info and user_id:
            url = info["url_pattern_userid"].format(user_id=user_id)

        if url and "{discriminator}" in url and discriminator:
            url = url.replace("{discriminator}", discriminator)

        if url:
            urls.append({"site": site, "url": url})
    return urls


def check_tor():
    """Returns True if TOR is globally enabled via config."""
    tor = load_tor_config()
    return tor.get("enabled", False)


def validate_url(url: str, session=None, timeout=10) -> bool:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    session = session or requests.Session()

    try:
        resp = session.get(url, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return False
        page = resp.text.lower()
        if any(
            x in page
            for x in ["not found", "404", "doesn’t exist", "page not available"]
        ):
            return False
        return True
    except Exception as e:
        logging.warning(f"Request to {url} failed: {e}")
        return False


def sanitize_result(username, platform_results):
    return {
        "username": username,
        "discovered": platform_results,
        "timestamp": datetime.now().isoformat(),
    }

def save_normalized_social_discovery(username: str, discovered: list) -> Path:

    OUTPUT_DIR = Path(__file__).parents[2] / "data/outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"normalized_social_{username}_{timestamp}.json"
    output_path = OUTPUT_DIR / filename

    normalized = {
        "username": username,
        "found_on": discovered,
        "method": "social_media_discovery",
        "timestamp": datetime.now().isoformat(),
    }

    with open(output_path, "w") as f:
        json.dump(normalized, f, indent=4)

    return output_path
