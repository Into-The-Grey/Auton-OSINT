import json
import re
from pathlib import Path
from collections import defaultdict

OUTPUT_DIR = Path(__file__).parents[1] / "data/outputs"
CORRELATED_OUTPUT = Path(__file__).parents[1] / "data/correlated_results.json"
STATE_FILE = Path(__file__).parents[1] / "data/.corr_state.json"


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
    # Gather entries
    if target_file:
        entries = []
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

    # Sort for deterministic order
    entries.sort(key=lambda e: e["filename"])

    # Load or initialize state
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as sf:
            state = json.load(sf)
        last_processed = state.get("last")
        phone_map = defaultdict(list, state.get("phone_map", {}))
        breach_map = defaultdict(
            set, {k: set(v) for k, v in state.get("breach_map", {}).items()}
        )
        username_map = defaultdict(
            set, {k: set(v) for k, v in state.get("username_map", {}).items()}
        )
        domain_map = defaultdict(
            set, {k: set(v) for k, v in state.get("domain_map", {}).items()}
        )
        ip_map = defaultdict(
            set, {k: set(v) for k, v in state.get("ip_map", {}).items()}
        )
        darkweb_keywords = defaultdict(
            set, {k: set(v) for k, v in state.get("darkweb_keywords", {}).items()}
        )
        darkweb_sites = defaultdict(
            set, {k: set(v) for k, v in state.get("darkweb_sites", {}).items()}
        )
        print(f"Resuming correlation from: {last_processed}")
    else:
        last_processed = None
        phone_map = defaultdict(list)
        breach_map = defaultdict(set)
        username_map = defaultdict(set)
        domain_map = defaultdict(set)
        ip_map = defaultdict(set)
        darkweb_keywords = defaultdict(set)
        darkweb_sites = defaultdict(set)
        print(f"Loaded {len(entries)} data entries for correlation.")

    # Process each entry
    for entry in entries:
        fname = entry["filename"]
        if last_processed and fname <= last_processed:
            continue  # Skip already‑processed

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

        # Darkweb correlation (NEW integration)
        if data.get("source") == "darkweb":
            keyword = data.get("keyword")
            if keyword:
                darkweb_keywords[keyword].add(fname)

            for result_set in ["darksearch", "torbot"]:
                results = data.get(result_set, [])
                if isinstance(results, list):
                    for result in results:
                        link = result.get("link")
                        if link:
                            darkweb_sites[link].add(fname)

        # Checkpoint state after each file
        last_processed = fname
        with open(STATE_FILE, "w") as sf:
            json.dump(
                {
                    "last": last_processed,
                    "phone_map": dict(phone_map),
                    "breach_map": {k: list(v) for k, v in breach_map.items()},
                    "username_map": {k: list(v) for k, v in username_map.items()},
                    "domain_map": {k: list(v) for k, v in domain_map.items()},
                    "ip_map": {k: list(v) for k, v in ip_map.items()},
                    "darkweb_keywords": {
                        k: list(v) for k, v in darkweb_keywords.items()
                    },
                    "darkweb_sites": {k: list(v) for k, v in darkweb_sites.items()},
                },
                sf,
                indent=2,
            )

    # Filter only truly correlated results
    correlated_phones = {k: v for k, v in phone_map.items() if len(v) > 1}
    correlated_breaches = {k: list(v) for k, v in breach_map.items() if len(v) > 1}
    correlated_usernames = {k: list(v) for k, v in username_map.items() if len(v) > 1}
    correlated_domains = {k: list(v) for k, v in domain_map.items() if len(v) > 1}
    correlated_ips = {k: list(v) for k, v in ip_map.items() if len(v) > 1}
    correlated_darkweb_keywords = {
        k: list(v) for k, v in darkweb_keywords.items() if len(v) > 1
    }
    correlated_darkweb_sites = {
        k: list(v) for k, v in darkweb_sites.items() if len(v) > 1
    }

    result = {
        "phones": correlated_phones,
        "breaches": correlated_breaches,
        "usernames": correlated_usernames,
        "domains": correlated_domains,
        "ips": correlated_ips,
        "darkweb_keywords": correlated_darkweb_keywords,
        "darkweb_sites": correlated_darkweb_sites,
    }

    # Write final correlated output
    with open(CORRELATED_OUTPUT, "w") as f:
        json.dump(result, f, indent=4)
    print(f"Correlations written to {CORRELATED_OUTPUT}")
    print(json.dumps(result, indent=4))

    # Clean up state for fresh next run
    try:
        STATE_FILE.unlink()
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    correlate_data()
