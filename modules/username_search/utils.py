import shutil
from pathlib import Path
from datetime import datetime
import logging
import json

# === PATH SETUP ===
ROOT_DIR = Path(__file__).parents[2]
MAIGRET_REPORTS_DIR = ROOT_DIR / "tools/maigret/reports"
OUTPUT_DIR = ROOT_DIR / "data/outputs"

# === LOGGING SETUP ===
LOG_PATH = ROOT_DIR / "logs/username_search.log"
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# === MOVE MAIGRET REPORT TO OUTPUT DIR ===
def move_maigret_output(username):
    try:
        json_reports = sorted(
            MAIGRET_REPORTS_DIR.glob(f"{username}*.json"),
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )
        if not json_reports:
            logging.warning(f"No Maigret output JSON found for {username}")
            return None

        latest_file = json_reports[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_file = OUTPUT_DIR / f"maigret_{username}_{timestamp}.json"

        shutil.move(str(latest_file), str(dest_file))
        logging.info(f"Moved Maigret report to {dest_file}")
        return dest_file
    except Exception as e:
        logging.exception(f"Error moving Maigret output file for {username}: {e}")
        return None


# === FILTER FALSE POSITIVES ===
def filter_false_positives(found_on_list):
    filtered = []
    for entry in found_on_list:
        url = entry.get("url", "")
        site = entry.get("site", "").lower()

        if not url or len(url.strip()) < 8:
            continue
        if any(
            term in url.lower()
            for term in ["404", "notfound", "error", "login", "signup", "register"]
        ):
            continue
        if site in ["example.com", "localhost"]:
            continue
        if url.endswith("/") and url.count("/") <= 3:
            continue

        filtered.append(entry)

    return filtered


# === CLEANUP ROGUE TXT FILES IN ROOT DIR ===
def purge_rogue_txt_files(exceptions=None):
    """
    Deletes all .txt files in the root directory except those explicitly whitelisted.
    """
    root_dir = Path(__file__).parents[2]
    exceptions = set(exceptions or [])

    for txt_file in root_dir.glob("*.txt"):
        if txt_file.name not in exceptions:
            try:
                txt_file.unlink()
                logging.info(f"Deleted rogue .txt file: {txt_file}")
            except Exception as e:
                logging.error(f"Failed to delete {txt_file}: {e}")
        else:
            logging.info(f"Skipped whitelisted .txt file: {txt_file}")


# === PARSE AND SAVE NORMALIZED OUTPUT ===
def parse_username_output(result_dict):
    method = result_dict.get("method")
    file_path = str(Path(result_dict.get("file", "")))
    if not Path(file_path).exists():
        logging.error(f"Output file does not exist: {file_path}")
        return None

    username = Path(file_path).stem.split("_")[1]
    normalized = {"username": username, "method": method, "found_on": []}

    try:
        if method == "maigret":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for site, info in data.get("sites", {}).items():
                    if info.get("status") == "claimed":
                        normalized["found_on"].append(
                            {
                                "site": site,
                                "url": info.get("url_user"),
                                "category": info.get("category"),
                                "tags": info.get("tags", []),
                            }
                        )

        elif method == "sherlock":
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "http" in line:
                        url = line.strip()
                        normalized["found_on"].append(
                            {
                                "site": url.split("//")[1].split("/")[0],
                                "url": url,
                                "category": "unknown",
                                "tags": [],
                            }
                        )

        else:
            logging.warning(f"Unknown method for parsing: {method}")
            return None

        # Apply false positive filtering
        original_count = len(normalized["found_on"])
        normalized["found_on"] = filter_false_positives(normalized["found_on"])
        filtered_count = len(normalized["found_on"])
        logging.info(
            f"Filtered {original_count - filtered_count} false positives (kept {filtered_count})"
        )

        # Save normalized version
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        norm_path = str(OUTPUT_DIR / f"normalized_username_{username}_{timestamp}.json")
        with open(norm_path, "w") as f:
            json.dump(normalized, f, indent=4)

        logging.info(f"Normalized data saved to {norm_path}")
        return norm_path

    except Exception as e:
        logging.exception(f"Error parsing and normalizing username data: {e}")
        return None
