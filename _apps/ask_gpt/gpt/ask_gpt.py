import requests

def take_dialog():
    dialog = []
    while True:
        dialog.append(input("Question: "))
        dialog.append(send_request(actual_dialog(dialog, 10)))
        print("\n" + dialog[-1] + "\n")

def set_prompt():
    prompt = "Imagine you are a highly skilled and experienced salesperson with 12 years in the industry. " \
             "Your goal is to aggressively pursue sales opportunities, using assertive strategies to close deals, " \
             "but always maintaining a polite and professional demeanor. You are known for your ability to identify " \
             "potential customers' pain points quickly, offer tailored solutions, and overcome objections effectively. " \
             "Your approach combines confidence, persistence, and respect for the customer's perspective."
    return prompt

def send_request(dialog):
    response = requests.post(url="http://mixail132.pythonanywhere.com/askgpt", json={"question": "\n".join(dialog)})
    return response.json()['answer']

def send_request_USA_server(dialog):
    response = requests.post(url="http://194.163.44.157/gpt_request", json={"request": "\n".join(dialog)})
    return response.json()['answer']


def actual_dialog(message, dialog, length, prompt:bool):
    act_dialog = [set_prompt()] if prompt else []
    if length > 0:
        act_dialog = act_dialog + dialog[-length:]
    else:
        act_dialog = act_dialog + dialog[-1:]
    return act_dialog

if __name__=='__main__':
    take_dialog()