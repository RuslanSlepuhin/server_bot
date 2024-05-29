import os

try:
    a = os.environ.get("EMAIL_HOST")
    print(a)
except Exception as ex:
    print("ERROR", ex)