import json
import socket
import requests
import whois
import dns.resolver
from pathlib import Path
from typing import List, Optional
import yaml
import logging

# === PATH SETUP ===
ROOT = Path(__file__).parents[2]
CONFIG_PATH = ROOT / "config/modules_config/domain_ip_lookup_config.yaml"
LOG_PATH = ROOT / "logs/domain_ip_lookup.log"

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# === LOAD CONFIG ===
with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)["domain_ip_lookup"]

HEADERS = {
    "User-Agent": CONFIG.get("headers", {}).get(
        "user_agent", "Mozilla/5.0 (Auton-OSINT)"
    )
}


# === DNS LOOKUPS ===
def query_dns_records(domain: str, types: List[str]) -> dict:
    results = {}
    resolver = dns.resolver.Resolver()
    for record_type in types:
        try:
            answers = resolver.resolve(domain, record_type)
            results[record_type] = [r.to_text() for r in answers]
        except Exception as e:
            results[record_type] = f"Failed: {str(e)}"
    return results


# === WHOIS LOOKUP ===
def query_whois(domain: str) -> Optional[dict]:
    try:
        w = whois.whois(domain)
        return {k: v for k, v in w.items() if v}  # prune nulls
    except Exception as e:
        logging.warning(f"WHOIS failed for {domain}: {e}")
        return None


# === REVERSE DNS ===
def query_reverse_dns(ip: str) -> Optional[str]:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception as e:
        logging.warning(f"Reverse DNS failed for {ip}: {e}")
        return None


# === GEOLOCATION LOOKUP ===
def query_ip_geolocation(ip: str) -> Optional[dict]:
    endpoint = CONFIG["features"]["ip_geolocation"]["endpoint"].format(ip=ip)
    try:
        resp = requests.get(endpoint, headers=HEADERS, timeout=10)
        return resp.json() if resp.status_code == 200 else None
    except Exception as e:
        logging.warning(f"Geolocation failed for {ip}: {e}")
        return None


# === ASN LOOKUP ===
def query_asn(ip: str) -> Optional[dict]:
    endpoint = CONFIG["features"]["asn_lookup"]["endpoint"].format(ip=ip)
    try:
        resp = requests.get(endpoint, headers=HEADERS, timeout=10)
        return resp.json() if resp.status_code == 200 else None
    except Exception as e:
        logging.warning(f"ASN lookup failed for {ip}: {e}")
        return None


# === BLACKLIST CHECK (ABUSEIPDB stub) ===
def query_blacklists(ip: str) -> Optional[dict]:
    abuse_entry = next(
        (
            p
            for p in CONFIG["features"]["blacklist_check"]["providers"]
            if p["name"] == "AbuseIPDB" and p["enabled"]
        ),
        None,
    )
    if not abuse_entry:
        return None  # Skipped

    endpoint = abuse_entry["endpoint"]
    headers = {"Accept": "application/json"}
    headers[abuse_entry["headers"]["Key-Header"]] = "YOUR_API_KEY"  # replace as needed

    try:
        resp = requests.get(
            endpoint,
            headers=headers,
            params={"ipAddress": ip, "maxAgeInDays": 90},
            timeout=10,
        )
        return resp.json() if resp.status_code == 200 else None
    except Exception as e:
        logging.warning(f"Blacklist check failed for {ip}: {e}")
        return None


# === CLEAN OUTPUT ===
def sanitize_output(data: dict) -> dict:
    return {k: v for k, v in data.items() if v and v != "Failed: []"}
