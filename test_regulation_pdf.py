
import requests
import fitz

PDF_URL = (
    "https://www.cert-in.org.in/PDF/"
    "CERT-In_Directions_70B_28.04.2022.pdf"
)

response = requests.get(PDF_URL, timeout=30)
response.raise_for_status()

document = fitz.open(stream=response.content, filetype="pdf")
text = "\n".join(page.get_text() for page in document)

print("Document pages:", len(document))
print("\n--- Relevant reporting requirements ---")

keywords = ["within 6 hours", "Data Breaches", "report cyber incidents"]

for keyword in keywords:
    position = text.lower().find(keyword.lower())

    if position >= 0:
        print(f"\nKeyword: {keyword}")
        print(text[max(0, position - 250):position + 700])
