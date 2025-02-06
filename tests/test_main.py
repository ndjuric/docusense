import time
import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

# FastAPI test client instantiation
client = TestClient(app)

# this waits for elasticsearch indexer before it runs tests
@pytest.fixture(autouse=True)
def wait_for_indexing():
    time.sleep(1)

def test_create_and_get_document():
    # DOCUMENT CREATION
    text = "This is a long text for testing."
    response = client.post("/documents", data={"text": text})
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert "document_id" in data, "Missing document_id in response"
    doc_id = data["document_id"]

    # DOCUMENT RETRIEVAL
    response_get = client.get(f"/documents/{doc_id}")
    assert response_get.status_code == 200, f"Response: {response_get.text}"
    data_get = response_get.json()
    assert data_get["document_id"] == doc_id, "Document ID does not match"
    assert data_get["text"] == text, "Document text does not match"

def test_get_document_not_found():
    # DOCUMENT RETRIEVAL WITH NON-EXISTENT ID
    random_id = str(uuid.uuid4())
    response = client.get(f"/documents/{random_id}")
    assert response.status_code == 404, f"Expected 404 for non-existent document, got {response.status_code}"

def test_search_documents():
    # CREATING TWO DOCS
    text1 = " the quick brown fox "
    text2 = " jumps over the lazy dog "
    client.post("/documents", data={"text": text1})
    client.post("/documents", data={"text": text2})

    # SEARCH FOR 'fox' - EXPECT AT LEAST ONE RESULT
    response = client.get("/search", params={"query": "fox", "k": 10})
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()

    # SEE IF 'results' KEY EXISTS IN data - SEE IF IT IS A LIST - SEE IF IT IS NOT EMPTY
    assert "results" in data, "Missing 'results' in response"
    results = data["results"]
    assert isinstance(results, list), "'results' should be a list"
    assert len(results) > 0, "Expected at least one result but got an empty list"

    # SEE IF AT LEAST ONE DOC CONTAINS 'fox' KEYWORD
    assert any("fox" in doc["text"] for doc in results), "No document in results contains 'fox'"

def test_search_with_llm_generation():
    # DOCUMENT CREATION FOLLOWED BY SEARCH WITH generate_answer FLAG
    text = "LLM generation test text."
    client.post("/documents", data={"text": text})
    response = client.get("/search", params={"query": "LLM generation", "generate_answer": "true"})
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()

    # SEE IF RESPONSE CONTAINS THE GENERATED ANSWER ALONG WITH THE SOURCE DOCUMENTS
    assert "answer" in data, "Missing 'answer' in response"
    assert "source_documents" in data, "Missing 'source_documents' in response"
    # MAKE SURE THAT THE SIMULATED ANSWER INCLUDES TEXT OF THE QUERY
    assert "LLM generation" in data["answer"], "Simulated answer does not include the query text"
