#!/usr/bin/env python3
import argparse
import re
import logging
from typing import Optional

from modules.phone_lookup.phone_lookup import phone_lookup
from modules.email_verification.email_verification import verify_email
from modules.username_search.username_search import search_username
from modules.social_media_discovery.social_media_discovery import social_discovery
from modules.domain_ip_lookup.domain_ip_lookup import domain_ip_lookup
from scripts.correlation_engine import correlate_data
from scripts.visualization import visualize_correlations

logger = logging.getLogger("input_parser")

# ————————————————————————————————————————
# Centralize your patterns here
PATTERNS = {
    "phone": re.compile(r"^\+?\d[\d\s\-\(\)\.]+$"),
    "email": re.compile(r"^[^@]+@[^@]+\.[^@]+$"),
    "ip": re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$"),
    "domain": re.compile(r"^[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}$"),
    "username": re.compile(r"^@?[A-Za-z0-9_.\-]{3,}$"),
}

def detect_input_type(item: str) -> Optional[str]:
    """
    Returns one of PATTERNS keys or None.
    """
    for t, rx in PATTERNS.items():
        if rx.fullmatch(item):
            return t
    return None

def split_items(field: str) -> list:
    """
    Split comma-separated strings and strip whitespace.
    """
    return [x.strip() for x in field.split(",") if x.strip()]


def main(override_flags=None):
    """
    If override_flags is a Namespace, skip argparse;
    otherwise, parse CLI exactly as before.
    """
    if override_flags:
        args = override_flags
    else:
        parser = argparse.ArgumentParser(
            description="Auton-OSINT Parser – Smart Input Handler",
            epilog="""\
📌 Syntax Guide (no flags needed):
  +1234567890         → Phone number
  user@example.com    → Email address
  @someuser           → Username
  someuser            → Username (generic)
  8.8.8.8             → IP address
  example.com         → Domain name

⚙️ Advanced Options:
  -p / --phone        → Force phone lookup
  -e / --email        → Force email check
  -u / --username     → Force username search
  --user-id           → Optional numeric ID
  --discriminator     → Optional tag/discriminator
  --target            → Force domain or IP lookup
""",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "input", nargs="?", help="Quick input (phone/email/username/domain/IP)"
        )
        parser.add_argument("-p", "--phone", help="Phone number to lookup")
        parser.add_argument("-e", "--email", help="Email address to verify")
        parser.add_argument(
            "-u", "--username", help="Username to scan across platforms"
        )
        parser.add_argument("--user-id", help="Optional platform-specific ID")
        parser.add_argument(
            "--discriminator", help="Optional tag (e.g. Discord#1234 → 1234)"
        )
        parser.add_argument("--target", help="Force domain or IP lookup")

        args = parser.parse_args()

    # — Build a dict of lists for each category
    buckets = {t: [] for t in PATTERNS}

    # 1) Flagged inputs (allow comma‑lists)
    if getattr(args, "phone", None):
        buckets["phone"].extend(split_items(args.phone))
    if getattr(args, "email", None):
        buckets["email"].extend(split_items(args.email))
    if getattr(args, "username", None):
        buckets["username"].extend(split_items(args.username))
    if getattr(args, "target", None):
        for item in split_items(args.target):
            cat = detect_input_type(item)
            if cat in ("domain", "ip"):
                buckets[cat].append(item)
            else:
                logger.error(f"Ignoring invalid target: {item}")

    # 2) Bare “input” (also comma‑lists)
    if getattr(args, "input", None):
        for item in split_items(args.input):
            cat = detect_input_type(item)
            if cat in ("phone", "email", "username"):
                buckets[cat].append(item.lstrip("@") if cat == "username" else item)
            elif cat in ("domain", "ip"):
                # domain/ip both feed into domain_ip_lookup
                buckets[cat].append(item)
            else:
                logger.error(f"Could not classify input: {item}")

    # If nothing to do, bail early
    if not any(buckets.values()):
        print("⚠️ No valid inputs detected. Use `--help`.")
        return

    # ————————————————————————————————————————
    # Dispatch to each module
    # PHONE
    for num in buckets["phone"]:
        logger.info(f"Dispatch phone_lookup → {num}")
        print(f"📞 Phone lookup: {num}")
        phone_lookup(num)
        print("✅ Done.\n")

    # EMAIL
    for addr in buckets["email"]:
        logger.info(f"Dispatch verify_email → {addr}")
        print(f"📧 Email verify: {addr}")
        verify_email(addr)
        print("✅ Done.\n")

    # USERNAME + SOCIAL + CORRELATE & VIS
    for usr in buckets["username"]:
        logger.info(f"Dispatch search_username → {usr}")
        print(f"🔎 Username search: {usr}")
        search_username(usr)
        print("✅ Done.")

        print(f"🌐 Social discovery: {usr}")
        social_discovery(
            usr,
            user_id=getattr(args, "user_id", None),
            discriminator=getattr(args, "discriminator", None),
        )
        print("✅ Done.\n")

        print("📊 Correlating & visualizing…")
        correlate_data()
        visualize_correlations()
        print("✅ All processing complete.\n")

    # DOMAIN & IP (same module)
    for host in buckets["domain"] + buckets["ip"]:
        logger.info(f"Dispatch domain_ip_lookup → {host}")
        print(f"🌍 Domain/IP lookup: {host}")
        domain_ip_lookup(host)
        print("✅ Done.\n")
