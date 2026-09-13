import os

import requests
from dotenv import load_dotenv
from langchain_core.documents import Document


load_dotenv()

COLLEGE_API_URL = os.getenv(
    "COLLEGE_API_URL",
    "http://localhost:8000"
)


API_ENDPOINTS = {
    "college": "/api/college",
    "departments": "/api/departments",
    "announcements": "/api/announcements",
    "placements": "/api/placements",
    "regulations": "/api/regulations",
    "exams": "/api/exams",
    "faculty": "/api/faculty",
    "academic_calendar": "/api/academic-calendar",
}


def fetch_api_data(endpoint):
    url = f"{COLLEGE_API_URL}{endpoint}"

    response = requests.get(
        url,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def convert_to_documents(data, category):
    documents = []

    if isinstance(data, dict):
        records = [data]

    elif isinstance(data, list):
        records = data

    else:
        return documents

    for record in records:

        content_parts = []

        for key, value in record.items():

            if value is not None:
                content_parts.append(
                    f"{key.replace('_', ' ').title()}: {value}"
                )

        content = "\n".join(content_parts)

        document = Document(
            page_content=content,
            metadata={
                "source": "dummy_college_api",
                "category": category,
                "document_name": f"{category}.json",
                "title": record.get(
                    "title",
                    record.get(
                        "name",
                        category.replace("_", " ").title()
                    )
                ),
                "department": record.get(
                    "department",
                    "General"
                ),
                "date": record.get(
                    "date",
                    ""
                ),
            }
        )

        documents.append(document)

    return documents


def load_api_documents():
    documents = []

    for category, endpoint in API_ENDPOINTS.items():

        try:

            data = fetch_api_data(endpoint)

            api_documents = convert_to_documents(
                data,
                category
            )

            documents.extend(api_documents)

            print(
                f"Loaded {len(api_documents)} "
                f"documents from {category}"
            )

        except requests.RequestException as error:

            print(
                f"Failed to load {category}: {error}"
            )

    return documents