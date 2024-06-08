import json.decoder
import json
import time

import requests
from sites.sites_additional_utils.question import compose_question


async def ask_ai(question, text=None):
    if text:
        question_ai = compose_question(question, text)
    else:
        question_ai = question
    response = await get_ai_response(question_ai)
    byte_response = response.content
    events = byte_response.split(b'\r\n\r\n')
    answers = []
    for event in events:
        if event:
            answer = event.decode()
            answer = answer.replace("data: ", "")
            answers.append(json.loads(answer))
    for answer in answers:
        if answer['event'] == "final-response":
            return answer["data"]['message']

async def get_ai_response(question_ai):
    url = "https://creativeai-68gw.onrender.com/chat"
    data = {'query': f'{question_ai}', 'model': 'llama-3-70b'}
    headers = {"Content-Type": "application/json"}
    for _ in range(3):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 429:
            time.sleep(2)
            continue
        elif response.status_code == 200:
            return response
    

if __name__ == "__main__":
    trial_question = "Is IT?"
    trial_text = """
    Обучение.
    Мы предлагаем:
    Бесплатное обучение.
    Карьерные перспективы: получи оффер на позицию младшего backend-разработчика в команду
    Газпромбанка после успешного обучения;
    Обучение у экспертов: ты сможешь развиваться в backend-разработке под
    руководством опытных специалистов;
    Профессиональное развитие: ты освоишь актуальные мировые стандарты по востребованным
    стекам: Java 21, Kotlin, Spring Boot, PostgreSQL, Docker и k8s.
    Обратная связь: ты будешь получать обратную связь по всем выполненным задачам.
    """

    print(ask_ai(trial_question, trial_text))
    print(ask_ai("What is the capital of the US?"))
