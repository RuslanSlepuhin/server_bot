from _debug import debug
# admins_user_id = [466267908, 5884559465, 758905227, 156815785, 498109732, 840293048]
admins_user_id = [5884559465, 466267908, 758905227] # Руслан, Макс, Александр
test_admins_user_id = [5884559465, 466267908, 758905227] # Руслан, Макс, Александр
test_name_pattern = "[Tt][Ee][Ss][tT]"
config_path = "./_apps/web_form_bot/settings/config.ini"

superuser = [5884559465]
bar_buttons_start = ["Excel"]
# server_domain = "https://dev.fcm.by/form/"# if not debug else "http://127.0.0.1:8000/"
server_domain = "https://4dev.itcoty.ru/forms/"

form_page = "/home/"
# endpoint_form = "form/"
endpoint_form = "form_data/"
media_excel_path = "_apps/web_form_bot/media/excel/"
form_excel_name = "form_data.xlsx"
caption_send_file = "take it"
port = 3000
host = "0.0.0.0"

actual_ngrok_tunnel = "https://1000-178-122-196-59.ngrok-free.app"
bot_domain = "https://4dev.itcoty.ru" if not debug else actual_ngrok_tunnel
external_webhook_path = "/external"
webhook_path = "/webhook"

keys_as_questions = {
    "name": "Your name",
    "instrumentWorks": "Do you understand how this investment instrument works and have you familiarized yourself with the information about it?",
    "whatAmount": "What amount are you willing to allocate to work with our trading instruments (in USDT)?",
    "whatTradingStrategy": "What trading strategy do you prefer?",
    "optimalInvestmentPeriod": "What investment period suits you best?",
    "howToReach": "How to reach you (preferably Telegram)",
}