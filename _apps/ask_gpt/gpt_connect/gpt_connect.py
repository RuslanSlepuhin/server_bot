import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def get_gpt4_response(prompt, model="gpt-4", temperature=0.7, max_tokens=150):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        timeout=15,
    )
    return response.choices[0].text.strip()

prompt = "Расскажи мне интересный факт о космосе."
response = get_gpt4_response(prompt)
print(response)
