import g4f

g4f.debug.logging = True  # Enable logging
g4f.check_version = False  # Disable automatic version checking
# print(g4f.version)  # Check version
# print(g4f.Provider.Ails.params)  # Supported args

class Chat:
# Automatic selection of provider

# Streamed completion
# while True:
#     request = input(">>")
#
#     try:
#         response = g4f.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": request}],
#             stream=True,
#         )
#         for message in response:
#             print(message, flush=True, end='')
#     except Exception as ex:
#         print("Что-то пошло не так")

# Normal response
    def get_answer(self, request):
        while True:
            # request = input(">>")

            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=[{"role": "ruslan", "content": request}],
                )  # Alternative model setting
                return response
            except Exception as ex:
                print("Что-то пошло не так")

