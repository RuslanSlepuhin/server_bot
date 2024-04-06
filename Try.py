import re

def matching(text):
    match = re.findall(r"[Tt][Ee][Ss][Tt]", text)
    return True if match else False

text = "TdEST"
match = matching(text)
print(match)