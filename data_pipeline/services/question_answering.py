from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

def answer_question(question, context):

    prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=50
    )

    generated_text = result[0]["generated_text"]

    return generated_text.replace(prompt, "").strip()