# modules/tor_darkweb_integration/tor_darkweb_integration.py

import logging
from pathlib import Path
from datetime import datetime
from .utils import (
    is_tor_enabled,
    start_tor,
    stop_tor,
    restart_tor,
    test_known_onions,
)

LOG_PATH = Path(__file__).parents[2] / "logs/tor_darkweb.log"
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_tor_darkweb_check():
    logging.info("==== Starting Tor Dark Web Integration Check ====")

    if not is_tor_enabled():
        logging.warning("Tor integration is disabled in the config.")
        return {"status": "disabled", "failed_sites": []}

    # Start Tor service
    start_tor()

    # Test known onion URLs
    failures = test_known_onions()

    # Stop Tor
    stop_tor()

    if failures:
        logging.warning(f"Failed to access {len(failures)} onion sites.")
        for site in failures:
            logging.warning(f"❌ {site}")
    else:
        logging.info("✅ All test onion URLs are accessible over Tor.")

    result = {
        "status": "success" if not failures else "partial_failure",
        "failed_sites": failures,
        "timestamp": datetime.now().isoformat(),
    }

    return result


if __name__ == "__main__":
    result = run_tor_darkweb_check()
    print("=== Tor Dark Web Check ===")
    print(f"Status: {result['status']}")
    if result["failed_sites"]:
        print("Failed sites:")
        for site in result["failed_sites"]:
            print(f" - {site}")
