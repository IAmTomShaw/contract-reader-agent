from astrapy import DataAPIClient
from typing import List, Dict, Any
import os
from src.embeddings import generate_embedding
from dotenv import load_dotenv

load_dotenv()

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION", "snippets")
ASTRA_DB_NAMESPACE = os.getenv("ASTRA_DB_NAMESPACE")

# Initialize AstraDB client and collection
client = DataAPIClient()

database = client.get_database(api_endpoint=ASTRA_DB_API_ENDPOINT, token=ASTRA_DB_APPLICATION_TOKEN)
collection = database.get_collection(ASTRA_DB_COLLECTION)

def vector_search(query: str, vector_field: str = "$vector", text_field: str = "original", limit: int = 4) -> List[Dict[str, Any]]:
    """
    Perform a vector search in the specified AstraDB collection.
    Args:
        query: Query text to search for
        vector_field: Field containing the vector embeddings
        text_field: Field containing the original text
        limit: Maximum number of results to return
    Returns:
        List of matching documents with similarity scores
    """
    query_vector = generate_embedding(query)

    results = collection.find(
        sort={"$vector": query_vector},
        limit=limit,
    )

    formatted_results = []

    for result in results:

        formatted_results.append({
            "original": result.get(text_field, ''),
            "modified": result.get('modified', ''),
            "ignored": result.get('ignored', False)
        })

    return formatted_results


def find_all_snippets() -> List[Dict[str, Any]]:
    """
    Find all snippets in the AstraDB collection.
    Returns:
        List of all snippets in the collection
    """
    results = collection.find()
    return [{
        "original": result.get("original", ''),
        "modified": result.get("modified", ''),
        "ignored": result.get("ignored", False)
    } for result in results]


def insert_snippet(original_snippet: str, modified_snippet: str = None, ignore: bool = False) -> Dict[str, Any]:
    """
    Insert a new snippet into the AstraDB collection.
    """
    doc = {
        "original": original_snippet,
        "$vector": generate_embedding(original_snippet),
        "modified": modified_snippet,
        "ignored": ignore
    }
    result = collection.insert_one(doc)
    return {"inserted_id": result.inserted_id}

