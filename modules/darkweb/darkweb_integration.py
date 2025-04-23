import requests
import yaml
import logging
from datetime import datetime
from pathlib import Path

# Load Configurations
CONFIG_PATH = "config/modules_config/darkweb_config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Logging setup
LOG_PATH = Path(__file__).parents[1] / "logs/darkweb_module.log"
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def search_darksearch(keyword: str, limit: int = config["query_limit"]) -> dict:
    """
    Searches DarkSearch.io API for the provided keyword.
    Returns structured JSON results.
    """
    api_url = "https://darksearch.io/api/search"
    params = {
        "query": keyword,
        "page": 1,
    }
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(
            api_url, params=params, headers=headers, timeout=config["timeout"]
        )
        response.raise_for_status()
        results = response.json().get("data", [])[:limit]
        logging.info(f"DarkSearch successful for keyword: '{keyword}'")
        return {"keyword": keyword, "results": results}
    except requests.RequestException as e:
        logging.error(f"Error querying DarkSearch for keyword '{keyword}': {e}")
        return {"keyword": keyword, "results": [], "error": str(e)}


def torbot_crawl(keyword: str) -> dict:
    """
    Placeholder for TorBot crawling integration.
    Returns structured JSON results.
    """
    logging.info(f"Initiating TorBot crawl for keyword: '{keyword}'")
    # Placeholder implementation
    # Integrate actual TorBot crawling logic here
    results = []  # Placeholder empty results
    logging.info(f"TorBot crawl completed for keyword: '{keyword}'")
    return {"keyword": keyword, "results": results}


def darkweb_lookup(keyword: str) -> dict:
    """
    Aggregates results from DarkSearch and TorBot.
    Returns unified correlation schema JSON.
    """
    logging.info(f"Starting dark web lookup for keyword: '{keyword}'")

    darksearch_results = search_darksearch(keyword)
    torbot_results = torbot_crawl(keyword)

    combined_results = {
        "keyword": keyword,
        "darksearch": darksearch_results["results"],
        "torbot": torbot_results["results"],
        "timestamp": datetime.utcnow().isoformat(),
    }

    logging.info(f"Completed dark web lookup for keyword: '{keyword}'")
    return combined_results


if __name__ == "__main__":
    test_keyword = "test"
    results = darkweb_lookup(test_keyword)
    print(f"Results for '{test_keyword}':\n", results)
