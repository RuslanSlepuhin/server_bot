import asyncio
import json.decoder
import json
from utils.additional_variables.additional_variables import valid_professions
import time
import requests
from sites.sites_additional_utils.question import compose_question


async def ask_ai(question, ai:str, text=None):
    if text:
        question_ai = compose_question(question, text)
    else:
        question_ai = question

    match ai:
        case "Gemini":
            url = "http://194.163.44.157/gemini_request"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json={"request": question_ai})
            print(f"\033[1;31m***** Gemini ***** {response.status_code}\033[0m")
            if 200 <= response.status_code < 300:
                answer = response.json()['answer']
                return answer, response.status_code, 'approved by ai Gemini', ai
            return "", response.status_code, None, ai


        case "Llama":
            ai_name_from = "Llama"
            url = "https://creativeai-q3g0.onrender.com/chat"
            data = {'query': f'{question_ai}', 'model': 'llama-3-70b'}
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if 200 <= response.status_code < 300:
                byte_response = response.content
                events = byte_response.split(b'\r\n\r\n')
                events.reverse()
                answers = []
                for event in events:
                    if event:
                        answer = event.decode("unicode-escape")
                        answer = answer.replace("data: ", "")
                        item = json.loads(answer)
                        if item['event'] == "final-response":
                            print(f"\033[1;31m***** Llama ***** {response.status_code}\033[0m")
                            return item['data']['message'], response.status_code, 'approved by ai Llama', ai
                return "", 500, None, ai

            else:
                print(f"\033[1;31m***** Llama ***** {response.status_code}\033[0m")
                return "", 500, None, ai

    # for _ in range(0, 3):
    #     response = requests.post(url, headers=headers, json=data, timeout=10)
    #     if response.status_code != 429:
    #         break
    #     else:
    #         print('sleep 20')
    #         await asyncio.sleep(20)
    # if response.status_code == 429:
    #     print('return empty str')
    #     return ""
    # byte_response = response.content
    # events = byte_response.split(b'\r\n\r\n')
    # answers = []
    # for event in events:
    #     if event:
    #         answer = event.decode()
    #         answer = answer.replace("data: ", "")
    #         answers.append(json.loads(answer))
    # for answer in answers:
    #     if answer['event'] == "final-response":
    #         return answer["data"]['message'], response.status_code

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
