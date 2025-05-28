import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_summary(text):
    prompt = (
        "You are a medical assistant. Read the following lab report and generate a 5-6 line "
        "simple summary in plain English, suitable for a normal person:\n\n"
        f"{text}\n\nSummary:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Sorry, AI summary generation failed. Please try again."
