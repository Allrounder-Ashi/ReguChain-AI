
import os

from dotenv import load_dotenv
from tinyfish import TinyFish

load_dotenv()

api_key = os.getenv("TINYFISH_API_KEY")

if not api_key:
    raise RuntimeError(
        "TINYFISH_API_KEY is missing. Check your .env file."
    )

client = TinyFish(api_key=api_key)


def search_regulations(query: str) -> list[dict]:
    """Search the web for regulatory information."""
    response = client.search.query(query=query)

    results = []

    for item in response.results:
        results.append({
            "title": getattr(item, "title", ""),
            "url": getattr(item, "url", ""),
            "snippet": getattr(item, "snippet", ""),
        })

    return results
