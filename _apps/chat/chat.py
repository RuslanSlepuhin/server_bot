import g4f

g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking
from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
    Phind,
)
class Chat:

# Normal response
    def get_answer(self, request):
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{"role": "user", "content": request}],
                provider=You,
                cookies={"cookie_name": "value", "cookie_name2": "value2"},
                auth=True
            )  # Alternative model setting
            print(response)
            return response
        except Exception as ex:
            print("Что-то пошло не так")

if __name__ == "__main__":
    chat = Chat()
    print(chat.get_answer(request="сколько лет земле"))