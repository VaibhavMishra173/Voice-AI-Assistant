from api.services.memory import SessionMemory

def test_session_memory():
    memory = SessionMemory(max_turns=3)
    memory.add_turn("What is Fort Wise?", "An AI company.")
    memory.add_turn("What does it do?", "It builds educational AI tools.")
    context = memory.get_formatted_context()
    assert "What is Fort Wise?" in context
    assert "It builds educational AI tools." in context
    assert isinstance(context, str)
