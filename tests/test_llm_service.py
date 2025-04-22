from app.services.llm_service import generate_answer

def test_llm():
    answer = generate_answer("What is Fort Wise AI?", ["Fort Wise AI is a defense system."])
    assert "Fort Wise" in answer

