import re


def parse_phoneinfoga_output(raw_output: str) -> dict:
    result = {}
    current_section = None
    url_pattern = re.compile(r"URL:\s+(https?://[^\s]+)")

    lines = raw_output.splitlines()

    for line in lines:
        line = line.strip()

        if line.startswith("Results for "):
            current_section = line.replace("Results for ", "").strip()
            result[current_section] = []
            continue

        url_match = url_pattern.search(line)
        if url_match and current_section:
            url = url_match.group(1)
            result[current_section].append(url)

        # Extracting number formatting at the end
        if ":" in line and any(
            keyword in line
            for keyword in ["Raw local", "Local", "E164", "International"]
        ):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()

    return result

def format_phone_number(number: str) -> str:
    """
    Formats phone number into E.164 standard if necessary.
    Placeholder for future validation or formatting.
    """
    return number.strip().replace(" ", "")
