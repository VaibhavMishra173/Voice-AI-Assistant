import openai
from core.config import Config
from api.services.logging import get_logger

logger = get_logger()

# Create a client instance with your API key
client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_answer(question: str, retrieved_chunks: list[str], memory_context: str = "") -> str:
    logger.info("Generating answer using GPT-4o...")

    # Combine retrieved chunks and memory context (if provided)
    context = "\n\n".join(retrieved_chunks)
    system_context = memory_context + f"\n\nRelevant context:\n{context}" if memory_context else context

    # Prepare the prompt
    prompt = f"""You are a helpful assistant for Fort Wise AI answering questions based on the following context. Use the context provided to give accurate, detailed answers. If the information isn't in the context, say "I don't have enough information to answer that completely.

Context:
{system_context}

Question: {question}
Answer:"""

    # Send the request to OpenAI API
    response = client.chat.completions.create(
        model=Config.MODEL_NAME,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Context:\n{system_context}\n\nQuestion: {question}"}
        ],
        temperature=0.2,
        max_tokens=2048,
    )

    # Extract and return the answer (updated syntax)
    answer = response.choices[0].message.content
    logger.info("Generated answer successfully.")
    return answer.strip()