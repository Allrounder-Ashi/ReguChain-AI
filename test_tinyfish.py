
from app.regulatory_research import search_regulations

results = search_regulations(
    "site:cert-in.org.in CERT-In Directions 2022 "
    "six hours cyber security incident reporting deadline"
)

for result in results:
    print("\nTitle:", result["title"])
    print("URL:", result["url"])
    print("Summary:", result["snippet"])

