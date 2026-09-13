import os

import requests

from dotenv import load_dotenv

from langchain_core.documents import Document


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# Configuration
# ==========================================

COLLEGE_API_URL = os.getenv(
    "COLLEGE_API_URL",
    "http://localhost:8000"
)


API_ENDPOINTS = {

    "college":
        "/api/college",

    "departments":
        "/api/departments",

    "announcements":
        "/api/announcements",

    "placements":
        "/api/placements",

    "regulations":
        "/api/regulations",

    "exams":
        "/api/exams",

    "faculty":
        "/api/faculty",

    "academic_calendar":
        "/api/academic-calendar",
}


# ==========================================
# Fetch API Data
# ==========================================

def fetch_api_data(endpoint):
    """
    Fetch data from the dummy college API.

    Args:
        endpoint: API endpoint path.

    Returns:
        JSON response.
    """

    url = (
        f"{COLLEGE_API_URL}"
        f"{endpoint}"
    )


    response = requests.get(
        url,
        timeout=10
    )


    response.raise_for_status()


    return response.json()


# ==========================================
# Convert API Data to Documents
# ==========================================

def convert_to_documents(
    data,
    category
):
    """
    Convert API records into LangChain
    Document objects.
    """

    documents = []


    # --------------------------------------
    # Normalize Records
    # --------------------------------------

    if isinstance(
        data,
        dict
    ):

        records = [data]

    elif isinstance(
        data,
        list
    ):

        records = data

    else:

        return documents


    # --------------------------------------
    # Convert Each Record
    # --------------------------------------

    for record in records:

        content_parts = []


        for key, value in record.items():

            if value is not None:

                formatted_key = (
                    key
                    .replace(
                        "_",
                        " "
                    )
                    .title()
                )


                content_parts.append(
                    f"{formatted_key}: "
                    f"{value}"
                )


        content = "\n".join(
            content_parts
        )


        # ----------------------------------
        # Metadata
        # ----------------------------------

        document = Document(

            page_content=content,

            metadata={

                "source":
                    "dummy_college_api",

                "category":
                    category,

                "document_name":
                    f"{category}.json",

                "title":
                    record.get(
                        "title",
                        record.get(
                            "name",
                            category
                            .replace(
                                "_",
                                " "
                            )
                            .title()
                        )
                    ),

                "department":
                    record.get(
                        "department",
                        "General"
                    ),

                "date":
                    record.get(
                        "date",
                        ""
                    ),
            }
        )


        documents.append(
            document
        )


    return documents


# ==========================================
# Load All API Documents
# ==========================================

def load_api_documents():
    """
    Load documents from all dummy college
    API endpoints.

    This module is independent from the
    main PDF RAG pipeline.
    """

    documents = []


    for category, endpoint in (
        API_ENDPOINTS.items()
    ):

        try:

            data = fetch_api_data(
                endpoint
            )


            api_documents = (
                convert_to_documents(
                    data,
                    category
                )
            )


            documents.extend(
                api_documents
            )


            print(
                f"Loaded "
                f"{len(api_documents)} "
                f"documents from "
                f"{category}"
            )


        except requests.RequestException as error:

            print(
                f"Failed to load "
                f"{category}: "
                f"{error}"
            )


    return documents


# ==========================================
# Run Directly
# ==========================================

if __name__ == "__main__":

    documents = load_api_documents()


    print(
        f"\nTotal API documents loaded: "
        f"{len(documents)}"
    )


    for document in documents[:5]:

        print("\n--------------------")

        print(
            document.page_content
        )

        print(
            document.metadata
        )