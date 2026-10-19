
import requests
import pymupdf

PDF_URL = (
    "https://www.cert-in.org.in/PDF/"
    "CERT-In_Directions_70B_28.04.2022.pdf"
)


def extract_reporting_rule():
    response = requests.get(PDF_URL, timeout=30)
    response.raise_for_status()

    document = pymupdf.open(
        stream=response.content,
        filetype="pdf"
    )

    text = "\n".join(
        page.get_text() for page in document
    )

    keyword = "within 6 hours"
    position = text.lower().find(keyword)

    if position == -1:
        return {
            "found": False,
            "source": PDF_URL
        }

    relevant_text = text[
        max(0, position - 250):position + 900
    ]

    return {
        "found": True,
        "regulator": "CERT-In",
        "requirement": "Report specified cyber incidents",
        "deadline": "Within 6 hours",
        "trigger": (
            "When the incident is noticed "
            "or brought to the entity's notice"
        ),
        "source": PDF_URL,
        "extracted_text": relevant_text
    }


if __name__ == "__main__":
    rule = extract_reporting_rule()

    for key, value in rule.items():
        print(f"{key}: {value}")
