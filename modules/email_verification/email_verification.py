import requests
import subprocess
import logging
import yaml
import json
import re
from pathlib import Path
from datetime import datetime

# Config setup
CONFIG_PATH = (
    Path(__file__).parents[2] / "config/modules_config/email_verification_config.yaml"
)
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)["email_verification"]

# Logging setup
log_file = Path(__file__).parents[2] / "logs/email_verification.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# Output directory
OUTPUT_DIR = Path(__file__).parents[2] / "data/outputs"

# ANSI color code removal (for h8mail output)
ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")


def check_xposed(email):
    try:
        url = f"https://api.xposedornot.com/v1/check-email/{email}"
        resp = requests.get(url, timeout=config["xposed_timeout"])
        if resp.status_code == 200:
            data = resp.json()
            breaches = data.get("breaches", [])

            # Fix double-wrapped list if necessary
            if (
                isinstance(breaches, list)
                and len(breaches) == 1
                and isinstance(breaches[0], list)
            ):
                breaches = breaches[0]

            logger.info(f"XposedOrNot found {len(breaches)} breach(es) for {email}")
            return {"xposed_breaches": breaches}
        else:
            logger.warning(
                f"XposedOrNot returned status {resp.status_code} for {email}"
            )
            return {"xposed_error": f"Status {resp.status_code}"}
    except Exception as e:
        logger.exception(f"XposedOrNot exception: {e}")
        return {"xposed_exception": str(e)}


def check_h8mail(email):
    try:
        cmd = ["h8mail", "-t", email]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=config["h8mail_timeout"]
        )
        logger.info(f"h8mail scan completed for {email}")
        clean_output = ansi_escape.sub("", result.stdout)
        return {"h8mail_output": clean_output}
    except Exception as e:
        logger.exception(f"h8mail exception: {e}")
        return {"h8mail_exception": str(e)}


def verify_email(email):
    logger.info(f"Verifying email: {email}")
    results = {}

    # First: Check via XposedOrNot
    xposed_results = check_xposed(email)
    results.update(xposed_results)

    # If breached, follow up with h8mail
    if "xposed_breaches" in xposed_results and xposed_results["xposed_breaches"]:
        h8mail_results = check_h8mail(email)
        results.update(h8mail_results)
    else:
        logger.info(f"No breaches found in XposedOrNot, skipping h8mail for {email}")

    # Save results
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_email = email.replace("@", "_at_").replace(".", "_")
        filename = OUTPUT_DIR / f"email_verification_{safe_email}_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(results, f, indent=4)

        logger.info(f"Email verification results saved to {filename}")
    except Exception as e:
        logger.exception(f"Failed to save results for {email}: {e}")

    return results


if __name__ == "__main__":
    test_email = "test@example.com"
    print(json.dumps(verify_email(test_email), indent=4))
