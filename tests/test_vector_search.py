from api.services import vector_search

import pytest
from api.services import vector_search

def test_query_faiss():
    query = "What is Fort Wise?"
    results = vector_search.query_faiss(query)
    assert len(results) > 0, "Expected search results, but got none."


def test_faiss_search_returns_results():
    query = "What is Fort Wise AI?"
    results = vector_search.query_faiss(query)
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(r, str) for r in results)
