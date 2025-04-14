import json
import logging
import socket
from pathlib import Path
from datetime import datetime

from .utils import (
    query_dns_records,
    query_whois,
    query_reverse_dns,
    query_ip_geolocation,
    query_asn,
    query_blacklists,
    sanitize_output,
)

# === PATHS & LOGGING ===
ROOT = Path(__file__).parents[2]
LOG_PATH = ROOT / "logs/domain_ip_lookup.log"
OUTPUT_DIR = ROOT / "data/outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def is_ip(target: str) -> bool:
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        return False


def domain_ip_lookup(target: str) -> str:
    logging.info(f"Running domain/IP lookup on: {target}")
    result = {"target": target, "type": "ip" if is_ip(target) else "domain"}

    if is_ip(target):
        result["reverse_dns"] = query_reverse_dns(target) or ""
        geolocation = query_ip_geolocation(target)
        result["ip_geolocation"] = json.dumps(geolocation) if geolocation is not None else ""
        asn_info = query_asn(target)
        result["asn_info"] = json.dumps(asn_info) if asn_info is not None else ""
        blacklists = query_blacklists(target)
        result["blacklists"] = json.dumps(blacklists) if blacklists is not None else ""
    else:
        try:
            resolved_ip = socket.gethostbyname(target)
            result["resolved_ip"] = resolved_ip
        except Exception as e:
            result["resolved_ip"] = f"Failed to resolve: {e}"

        result["dns_records"] = json.dumps(query_dns_records(
            target, ["A", "AAAA", "MX", "NS", "TXT", "SOA"]
        ))
        whois = query_whois(target)
        result["whois"] = json.dumps(whois) if whois is not None else ""

    # Final output
    result = sanitize_output(result)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = "".join(c if c.isalnum() else "_" for c in target)
    out_path = OUTPUT_DIR / f"domain_ip_lookup_{safe_target}_{timestamp}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=4)

    logging.info(f"Domain/IP lookup complete. Results saved to {out_path}")
    return str(out_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: python3 -m modules.domain_ip_lookup.domain_ip_lookup <domain_or_ip>"
        )
        sys.exit(1)

    target = sys.argv[1]
    output_file = domain_ip_lookup(target)
    print(f"Results saved to: {output_file}")
