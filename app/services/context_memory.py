context_history = []

def get_conversation_context():
    return context_history[-5:]  # Keep limited context

def update_context(query, answer):
    context_history.append({"role": "user", "content": query})
    context_history.append({"role": "assistant", "content": answer})

