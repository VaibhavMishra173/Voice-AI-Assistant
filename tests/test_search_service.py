from app.services.search_service import search_knowledge_base

def test_search():
    chunks = search_knowledge_base("surveillance")
    assert isinstance(chunks, list)
    assert len(chunks) > 0

