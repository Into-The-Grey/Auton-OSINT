#!/usr/bin/env python3

import sys
import time
import argparse
import hashlib
import getpass
from pathlib import Path
from datetime import datetime
from scripts.input_parser import main as run_parser
from scripts.correlation_engine import correlate_data
from scripts.visualization import visualize_correlations
import json
import traceback

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LAST_RUN_PATH = Path("data/.last_run.json")

CONFIG_DIR = Path("config/modules_config")
CONFIG_HASH_FILE = CONFIG_DIR / ".config_hash.checksum"


def compute_config_checksum():
    hasher = hashlib.sha256()
    for file in CONFIG_DIR.glob("*.yaml"):
        with open(file, "rb") as f:
            hasher.update(f.read())
    return hasher.hexdigest()


def validate_config_checksum():
    if not CONFIG_HASH_FILE.exists():
        return True  # No validation baseline
    current = compute_config_checksum()
    with open(CONFIG_HASH_FILE, "r") as f:
        expected = f.read().strip()
    return current == expected


def save_last_run(data):
    with open(LAST_RUN_PATH, "w") as f:

        json.dump(data, f, indent=4)


def main():
    parser = argparse.ArgumentParser(description="🧠 Auton-OSINT Suite Launcher")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run without visualization (headless mode).",
    )
    parser.add_argument(
        "--skip-correlation", action="store_true", help="Skip correlation and graphing."
    )
    parser.add_argument(
        "--output-summary",
        choices=["json", "csv", "md"],
        help="Generate summary in specified format.",
    )
    parser.add_argument(
        "--batch-input", type=Path, help="Run batch inputs from a file."
    )
    parser.add_argument(
        "--no-tor", action="store_true", help="Disable TOR for this session."
    )
    parser.add_argument(
        "--silent", action="store_true", help="Suppress all output except errors."
    )
    parser.add_argument(
        "--visualize-only",
        action="store_true",
        help="Only visualize previous correlation output.",
    )
    parser.add_argument(
        "--secure", action="store_true", help="Require password to run."
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable verbose stacktrace output."
    )
    parser.add_argument("--module-test", help="Run a specific module with mock data.")
    parser.add_argument(
        "--timing", action="store_true", help="Show elapsed time per phase."
    )
    parser.add_argument(
        "--validate-config", action="store_true", help="Run config checksum check."
    )

    args = parser.parse_args()
    start_time = time.time()

    if args.validate_config:
        if not validate_config_checksum():
            print("❌ Config checksum mismatch. Configs may have been tampered with.")
            sys.exit(1)

    if args.secure:
        pw = getpass.getpass("🔒 Enter execution password: ")
        if pw.strip() != "letmein":  # Replace this with a secure method
            print("❌ Incorrect password.")
            sys.exit(1)

    if args.visualize_only:
        if not args.silent:
            print("📈 Visualization-only mode enabled.")
        visualize_correlations()
        return

    if not args.silent:
        print("\n🔍 Auton-OSINT Suite Initialized")
        print("================================")
        print("Modules loaded:")
        print(" • Input parser")
        print(" • Correlation engine")
        print(" • Graph visualizer\n")

    try:
        if args.module_test:
            # You'd implement this per module if needed
            print(f"🧪 Module test for: {args.module_test} (not implemented)")
            return

        if args.batch_input:
            print(
                f"📂 Batch input mode: {args.batch_input} (not implemented)"
            )  # Add support later
            return

        run_parser(override_flags=args)

        if not args.skip_correlation:
            if not args.silent:
                print("📎 Starting correlation engine...")
            correlate_data()

            if not args.headless:
                if not args.silent:
                    print("📈 Launching visualization...")
                visualize_correlations()

        if args.output_summary:
            print(f"📝 Summary output ({args.output_summary}) not implemented yet.")

        save_last_run({"timestamp": datetime.now().isoformat()})

        if not args.silent:
            print("\n✅ All processes completed successfully.")

    except Exception as e:
        if args.debug:

            traceback.print_exc()
        else:
            print(f"❌ Error occurred: {e}")
        sys.exit(1)

    if args.timing:
        elapsed = time.time() - start_time
        print(f"⏱️ Total time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()
