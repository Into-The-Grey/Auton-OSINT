# modules/social_media_discovery/social_media_discovery.py

import json
import logging
import requests
from pathlib import Path
from typing import Optional
from datetime import datetime
from .utils import (
    generate_platform_urls,
    get_enabled_platforms,
    validate_url,
    sanitize_result,
    load_tor_config,
    save_normalized_social_discovery,  # NEW
)

# === CONFIG & LOGGING ===
CONFIG_PATH = (
    Path(__file__).parents[2]
    / "config/modules_config/social_media_discovery_config.yaml"
)
TOR_CONFIG = load_tor_config()
LOG_PATH = Path(__file__).parents[2] / "logs/social_media_discovery.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

OUTPUT_DIR = Path(__file__).parents[2] / "data/outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def social_discovery(
    username: str, user_id: Optional[str] = None, discriminator: Optional[str] = None
):
    logging.info(f"Starting social media discovery for {username}")
    platforms = get_enabled_platforms()
    urls_to_check = generate_platform_urls(platforms, username, user_id, discriminator)

    session = requests.Session()
    if TOR_CONFIG.get("enabled", False):
        session.proxies = {
            "http": TOR_CONFIG.get("tor_proxy_url", "socks5h://127.0.0.1:9050"),
            "https": TOR_CONFIG.get("tor_proxy_url", "socks5h://127.0.0.1:9050"),
        }

    discovered = []

    for entry in urls_to_check:
        platform = entry["site"]
        url = entry["url"]

        try:
            logging.info(f"Checking {platform}: {url}")
            if validate_url(url, session=session):
                discovered.append({"site": platform, "url": url})
        except Exception as e:
            logging.warning(f"Error checking {platform} at {url}: {e}")

    result = sanitize_result(username, discovered)

    # Output filename sanitization
    safe_username = "".join(c if c.isalnum() else "_" for c in username)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = OUTPUT_DIR / f"social_discovery_{safe_username}_{timestamp}.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=4)

    logging.info(f"Discovery results saved to {out_path}")

    # Save normalized version for correlation engine
    norm_path = save_normalized_social_discovery(username, discovered)
    logging.info(f"Normalized data saved to {norm_path}")

    return out_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python3 -m modules.social_media_discovery.social_media_discovery <username> [user_id] [discriminator]"
        )
        sys.exit(1)

    username = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else None
    discriminator = sys.argv[3] if len(sys.argv) > 3 else None

    result = social_discovery(username, user_id, discriminator)
    print(f"Results saved to: {result}")
