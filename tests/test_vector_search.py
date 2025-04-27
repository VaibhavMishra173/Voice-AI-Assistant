from api.services import vector_search

import pytest
from api.services import vector_search

def test_query_faiss():
    query = "What is Fort Wise?"
    results = vector_search.query_faiss(query)
    assert len(results) > 0, "Expected search results, but got none."
