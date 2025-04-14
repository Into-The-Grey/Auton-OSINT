import json
import re
from pathlib import Path
from collections import defaultdict

OUTPUT_DIR = Path(__file__).parents[1] / "data/outputs"
CORRELATED_OUTPUT = Path(__file__).parents[1] / "data/correlated_results.json"


def load_all_outputs():
    all_data = []
    for file in OUTPUT_DIR.glob("*.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                all_data.append({"filename": file.name, "data": data})
        except Exception as e:
            print(f"Error loading {file.name}: {e}")
    return all_data


def correlate_data(target_file=None):
    entries = []

    if target_file:
        target_path = Path(target_file)
        if target_path.exists():
            with open(target_path, "r") as f:
                data = json.load(f)
                entries.append({"filename": target_path.name, "data": data})
        else:
            print(f"Specified file does not exist: {target_file}")
            return
    else:
        entries = load_all_outputs()

    print(f"Loaded {len(entries)} data entries for correlation.")

    phone_map = defaultdict(list)
    breach_map = defaultdict(set)
    username_map = defaultdict(set)
    domain_map = defaultdict(set)
    ip_map = defaultdict(set)

    for entry in entries:
        fname = entry["filename"]
        data = entry["data"]

        # Phone number matching
        for key in ["E164", "Local", "International", "Raw local"]:
            if key in data:
                norm = re.sub(r"[^\d+]", "", data[key])
                if norm:
                    phone_map[norm].append(fname)

        # Breach name matching
        breaches = data.get("xposed_breaches", [])
        if isinstance(breaches, list):
            for breach in breaches:
                if isinstance(breach, str):
                    breach_map[breach].add(fname)

        # Username site matching
        if "found_on" in data and isinstance(data["found_on"], list):
            for item in data["found_on"]:
                site = item.get("site")
                if site:
                    username_map[site].add(fname)

        # Domain correlation
        domain = data.get("domain")
        if domain:
            domain_map[domain].add(fname)

        # IP correlation
        ip = data.get("ip")
        if ip:
            ip_map[ip].add(fname)

    # Only keep correlated (multi-source) matches
    correlated_phones = {k: v for k, v in phone_map.items() if len(v) > 1}
    correlated_breaches = {k: list(v) for k, v in breach_map.items() if len(v) > 1}
    correlated_usernames = {k: list(v) for k, v in username_map.items() if len(v) > 1}
    correlated_domains = {k: list(v) for k, v in domain_map.items() if len(v) > 1}
    correlated_ips = {k: list(v) for k, v in ip_map.items() if len(v) > 1}

    result = {
        "phones": correlated_phones,
        "breaches": correlated_breaches,
        "usernames": correlated_usernames,
        "domains": correlated_domains,
        "ips": correlated_ips,
    }

    with open(CORRELATED_OUTPUT, "w") as f:
        json.dump(result, f, indent=4)

    print(f"Correlations written to {CORRELATED_OUTPUT}")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    correlate_data()
