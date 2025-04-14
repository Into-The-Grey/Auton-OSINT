import argparse
import re
from modules.phone_lookup.phone_lookup import phone_lookup
from modules.email_verification.email_verification import verify_email
from modules.username_search.username_search import search_username
from modules.social_media_discovery.social_media_discovery import social_discovery
from modules.domain_ip_lookup.domain_ip_lookup import domain_ip_lookup
from scripts.correlation_engine import correlate_data
from scripts.visualization import visualize_correlations


def detect_input_type(raw_input):
    if re.fullmatch(r"\+?\d[\d\s\-().]+", raw_input):  # phone
        return "phone"
    elif re.fullmatch(r"[^@]+@[^@]+\.[^@]+", raw_input):  # email
        return "email"
    elif re.fullmatch(r"^(?:(?:[0-9]{1,3}\.){3}[0-9]{1,3})$", raw_input):  # IP
        return "ip"
    elif re.fullmatch(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", raw_input):  # domain
        return "domain"
    elif re.fullmatch(r"@[a-zA-Z0-9_]+", raw_input):  # @username
        return "username"
    elif re.fullmatch(r"[a-zA-Z0-9_.-]{3,}", raw_input):  # fallback username
        return "username"
    return None


def main(override_flags=None):
    if override_flags:
        args = override_flags
    else:
        parser = argparse.ArgumentParser(
            description="Auton-OSINT Parser – Smart Input Handler",
            epilog="""\
📌 Syntax Guide (no flags needed):
  +1234567890         → Phone number
  user@example.com    → Email address
  @someuser           → Username (Twitter/Discord-style)
  someuser            → Username (generic)
  8.8.8.8             → IP address
  example.com         → Domain name

⚙️ Advanced Options:
  -p / --phone        → Force phone lookup
  -e / --email        → Force email check
  -u / --username     → Force username search
  --user-id           → Provide numeric platform ID (e.g. Facebook, Yelp)
  --discriminator     → Optional tag/discriminator (e.g. Discord#1234 → 1234)
  --target            → Force domain or IP lookup
""",
            formatter_class=argparse.RawTextHelpFormatter,
        )

        parser.add_argument(
            "input", nargs="?", help="Quick input (phone/email/username/domain/IP)"
        )
        parser.add_argument(
            "-p", "--phone", help="Phone number to lookup (e.g. +15551234567)"
        )
        parser.add_argument(
            "-e", "--email", help="Email address to verify (e.g. test@domain.com)"
        )
        parser.add_argument(
            "-u", "--username", help="Username to scan across platforms (e.g. johndoe)"
        )
        parser.add_argument(
            "--user-id", help="Optional user ID (used by Facebook, Vimeo, etc.)"
        )
        parser.add_argument(
            "--discriminator", help="Optional tag (e.g. Discord#1234 → 1234)"
        )
        parser.add_argument(
            "--target", help="Domain or IP address (e.g. example.com or 8.8.8.8)"
        )

        args = parser.parse_args()

    # === Dynamic Input ===
    if args.input:
        detected = detect_input_type(args.input)
        if detected == "phone":
            args.phone = args.input
        elif detected == "email":
            args.email = args.input
        elif detected == "username":
            args.username = args.input
        elif detected in ["domain", "ip"]:
            args.target = args.input

    # === Phone Lookup ===
    if args.phone:
        print(f"📞 Phone lookup for: {args.phone}")
        result = phone_lookup(args.phone)
        print("✅ Lookup complete." if result else "❌ Lookup failed.")

    # === Email Verification ===
    if args.email:
        print(f"📧 Email verification: {args.email}")
        result = verify_email(args.email)
        print("✅ Verification complete." if result else "❌ Verification failed.")

    # === Username + Social Media ===
    if args.username:
        print(f"🔎 Username search for: {args.username}")
        result = search_username(args.username)
        print("✅ Username search complete.")

        print(f"🌐 Running social media discovery for: {args.username}")
        social_discovery(
            args.username, user_id=args.user_id, discriminator=args.discriminator
        )
        print("✅ Social discovery complete.")

        print("📊 Running correlation & visualization...")
        correlate_data()
        visualize_correlations()
        print("✅ All processing complete.")

    # === Domain/IP Lookup ===
    if args.target:
        print(f"🌍 Domain/IP analysis for: {args.target}")
        result = domain_ip_lookup(args.target)
        print(f"✅ Lookup complete. Results saved to {result}")

    # === No Input ===
    if not any([args.phone, args.email, args.username, args.target]):
        print("⚠️ No input detected. Use `--help` for usage examples.")


if __name__ == "__main__":
    main()
