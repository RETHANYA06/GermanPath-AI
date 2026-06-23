import google.generativeai as genai

from app.chatbot.config import (
    GEMINI_API_KEY
)

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_tutor(question):

    prompt = f"""
You are a German language tutor.

Answer in simple English.

If needed:
- Explain grammar
- Explain vocabulary
- Correct German sentences
- Give examples
- Help A1 to B1 learners

Question:
{question}
"""

    response = model.generate_content(
        prompt
    )

    return response.text