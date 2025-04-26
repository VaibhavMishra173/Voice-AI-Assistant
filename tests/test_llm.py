from api.services import llm

import pytest
from api.services import llm

def test_generate_answer():
    question = "What does Fort Wise do?"
    context = ["Fort Wise is a platform that helps teams make better decisions with AI."]
    answer = llm.generate_answer(question, context)
    assert "platform" in answer, f"Expected the word 'platform' in the answer, but got {answer}"


def test_llm_response():
    sample_context = [
        "Fort Wise AI is a company specializing in AI-powered education and training systems.",
        "It uses cutting-edge language models to deliver personalized learning experiences."
    ]
    question = "What does Fort Wise AI do?"
    response = llm.generate_answer(question, sample_context)
    assert isinstance(response, str)
    assert len(response) > 0
