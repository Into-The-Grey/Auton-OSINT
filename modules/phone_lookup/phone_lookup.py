import subprocess
import yaml
import logging
import os
import json
from pathlib import Path
from datetime import datetime
from .utils import parse_phoneinfoga_output

def mask_phone_number(phone_number):
    if len(phone_number) > 4:
        return phone_number[:2] + '*' * (len(phone_number) - 4) + phone_number[-2:]
    return phone_number
# Load configuration
CONFIG_PATH = (
    Path(__file__).parents[2] / "config/modules_config/phone_lookup_config.yaml"
)
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)["phoneinfoga"]

# Setup Logging
log_file = Path(__file__).parents[2] / "logs/phone_lookup.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Outputs directory
OUTPUT_DIR = Path(__file__).parents[2] / "data/outputs"


def phone_lookup(phone_number):
    command = [
        config["executable_path"],
        "scan",
        "-n",
        phone_number,
    ]

    try:
        masked_phone_number = mask_phone_number(phone_number)
        logging.info(f"Initiating phone lookup for: {masked_phone_number}")
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=config["timeout"]
        )

        if result.returncode != 0:
            logging.error(f"Command error: {result.stderr.strip()}")
            return None

        output = result.stdout.strip()
        structured_data = parse_phoneinfoga_output(output)

        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
        filename = OUTPUT_DIR / f"phone_lookup_{safe_number}_{timestamp}.json"

        # Write to JSON file
        with open(filename, "w") as json_file:
            json.dump(structured_data, json_file, indent=4)

        logging.info(
            f"Phone lookup and parsing successful, results saved in {filename}"
        )
        return structured_data

    except subprocess.TimeoutExpired:
        logging.error("Timeout expired during phone lookup.")
        return None
    except Exception as e:
        logging.exception(f"Unexpected error during phone lookup: {e}")
        return None


if __name__ == "__main__":
    sample_number = "+11234567890"
    result = phone_lookup(sample_number)
    print(json.dumps(result, indent=4) if result else "Lookup failed.")
