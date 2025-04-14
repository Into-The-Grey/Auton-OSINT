import subprocess
import logging
import json
import yaml
from pathlib import Path
from datetime import datetime
import time
from .utils import move_maigret_output, parse_username_output, purge_rogue_txt_files

# === CONFIG & LOGGING ===
CONFIG_PATH = (
    Path(__file__).parents[2] / "config/modules_config/username_search_config.yaml"
)
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)["username_search"]

LOG_PATH = Path(__file__).parents[2] / "logs/username_search.log"
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

OUTPUT_DIR = Path(__file__).parents[2] / "data/outputs"
MAIGRET_DIR = Path(__file__).parents[2] / "tools/maigret"
MAIGRET_REPORTS_DIR = MAIGRET_DIR / "reports"


# === TOR CONTROL ===
def start_tor():
    try:
        logging.info("Starting Tor service...")
        subprocess.run(["systemctl", "start", "tor"], check=True)
        time.sleep(3)
    except Exception as e:
        logging.exception("Failed to start Tor")


def stop_tor():
    try:
        logging.info("Stopping Tor service...")
        subprocess.run(["systemctl", "stop", "tor"], check=True)
    except Exception as e:
        logging.exception("Failed to stop Tor")


def restart_tor():
    try:
        logging.info("Restarting Tor service...")
        subprocess.run(["systemctl", "restart", "tor"], check=True)
        time.sleep(3)
    except Exception as e:
        logging.exception("Failed to restart Tor")


# === MAIGRET RUN ===
def run_maigret(username):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"maigret_{username}_{timestamp}.json"

    cmd = [
        "python3",
        "-m",
        "tools.maigret.maigret.maigret",
        username,
        "--top-sites",
        "750",
        "--json",
        "simple",  # Ensures JSON only
        "--folderoutput",
        str(output_path),  # This becomes the output directory
        "--no-color",  # Optional: make it cleaner for logs
        "--no-progressbar",  # Optional: cleaner subprocess
    ]

    if config.get("use_tor", False):
        cmd += ["--tor"]

    if config.get("permute", False):
        cmd += ["--permute"]

    try:
        logging.info(f"Running Maigret for {username}")
        subprocess.run(cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Maigret failed: {e}")
        return None


# === SHERLOCK RUN ===
def run_sherlock(username):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"sherlock_{username}_{timestamp}.txt"

    try:
        logging.info(f"Running Sherlock for {username}")
        with open(output_file, "w") as f:
            subprocess.run(
                ["sherlock", username], stdout=f, stderr=subprocess.STDOUT, check=True
            )
        return output_file
    except subprocess.CalledProcessError as e:
        logging.error(f"Sherlock failed: {e}")
        return None


# === MAIN ===
def search_username(username):
    logging.info(f"Starting username search for {username}")

    try:
        if config.get("use_tor", False):
            start_tor()

        maigret_success = run_maigret(username)

    finally:
        if config.get("use_tor", False):
            stop_tor()

    if maigret_success:
        moved_file = move_maigret_output(username)
        if moved_file:
            result = {"method": "maigret", "file": str(moved_file)}
            parse_username_output(result)
            logging.info(f"Maigret success for {username}, file moved to {moved_file}")
            logging.info(f"Search completed for {username}")
            return result
        else:
            logging.warning("Maigret output not found or failed to move.")

    logging.warning("Maigret failed fatally. Falling back to Sherlock...")

    sherlock_result = run_sherlock(username)
    if sherlock_result and sherlock_result.exists():
        result = {"method": "sherlock", "file": str(sherlock_result)}
        parse_username_output(result)
        logging.info(f"Sherlock success for {username}")
        logging.info(f"Search completed for {username}")
        return result
    else:
        logging.error("Both Maigret and Sherlock failed.")
        return {"error": "Both tools failed"}


purge_rogue_txt_files(
    exceptions=["README.txt", "important_notes.txt", "requirements.txt"]
)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 -m modules.username_search.username_search <username>")
        sys.exit(1)

    username = sys.argv[1]
    result = search_username(username)
    print(json.dumps(result, indent=4))

    file_path = result.get("file")
    if file_path:
        parsed = parse_username_output(result)
    else:
        parsed = {"error": "No file path provided"}
    purge_rogue_txt_files(
        exceptions=["README.txt", "important_notes.txt", "requirements.txt"]
    )

    print(json.dumps(parsed, indent=4))
