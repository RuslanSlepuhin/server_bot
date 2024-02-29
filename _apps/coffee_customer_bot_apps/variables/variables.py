
# Requests variables
customer_pressed_cancel_endpoint = "https://test.ru"
customer_feedback_endpoint = "https://test.ru"
customer_add_username_to_database_endpoint = "https://test.ru"

# ----------- Endpoints urls ------------
# impossible_to_cancel_order_endpoints = "/impossible_to_cancel_order"
# user_verification_endpoint = "/verification"
is_user_active_endpoint = "/is_user_active"
provide_message_to_user_endpoint = "/provide_message_to_user"
provide_message_to_horeca_endpoint = "/provide_message_to_horeca"

#--------------- server urls ---------------
# server_status_from_customer = "/client/status_from_user/" # take the POST from customer to send to horeca
# server_status_from_horeca = "/client/status_from_horeca/" # take the POST from horeca to send to customer
# # GET# -> take json from customer with verification code and user_id
# # POST -> {"user_id": user_id:int , "verification_code": verification_code:str}
# verification_endpoint = "/client/enter_key_from_user/"
# user_info = "/client/user-info" # GET
# request_exists_user_id = "/user-id-exists/"
#
# get_user_info = "/client/user_info" # for customer bot > GET data by customer telegram id
# get_horeca_info = "/client/horeca_info" # for horeca bot -> GET data by horeca telegram id

# ======= domain =======

server_status_from_customer = "/client/status_from_user/" # take the POST from customer to send to horeca
server_status_from_horeca = "/client/status_from_horeca/" # take the POST from horeca to send to customer
# GET# -> take json from customer with verification code and user_id
# POST -> {"user_id": user_id:int , "verification_code": verification_code:str}
verification_endpoint = "/client/enter_key_from_user/"
user_info = "/client/user-info" # GET
request_exists_user_id = "/user-id-exists/"

get_user_info = "/client/user_info" # for customer bot > GET data by customer telegram id
get_horeca_info = "/client/horeca_info" # for horeca bot -> GET data by horeca telegram id


# -------------- common info --------------
main_endpoint = "http://127.0.0.1:5000/is_user_active"

# server_domain = "http://127.0.0.1:7000"
# server_domain = "https://083d-46-53-248-34.ngrok-free.app"
server_domain = "https://dev.fcm.by" # tunnel
customer_bot_domain = "http://127.0.0.1:5000"
horeca_bot_domain = "http://127.0.0.1:5000"

customer_bot_name = "@a34fgh5_bot"
horeca_bot_name = "@a34fgh6_bot"

get_subscribe_status = "/subscribe-status/"

n = 5502797471
rus = 5884559465

fields = ["id", "telegram_user_id", "enter_key", "order_id", "status", "bot_subscribing", "telegram_horeca_id", "horeca_id", "order_description"]

dialog_customer = {
    "verification": "Введите верификационный код",
    "verification_error": "Верификация неуспешна, проверьте правильность кода",
}

USER_STATUS_BUTTONS = {
    'canceled_by_user': 'Отменен пользователем',
    'feedback': "Оставить отзыв",
}

USER_STATUSES_NOT_SHOW = {
    'canceled_by_user': 'Отменен пользователем',
    'canceled_by_cafe': 'Отменен заведением',
    'delivered': 'Выдан - получен клиентом',
    'utilized': 'Утилизирован - кафе уничтожило заказ, за которым не явились вовремя',
}

customer_buttons_status = {}
for key in USER_STATUS_BUTTONS:
    customer_buttons_status[USER_STATUS_BUTTONS[key]] = key

USER_STATUSES_CANCEL_IMPOSSIBLE = ['payment_process', 'placed']

# Выбор статуса заказа
BARISTA_STATUS_CHOICES = {
    'payment_process': 'В процессе оплаты',
    'placed': 'Размещен - успешно оплачен',
    'in_progress': 'В работе - Чек вышел бариста',
    'ready': 'Готов - Заказ готов к передаче',
    'delivered': 'Выдан - получен клиентом',
}

BARISTA_NEGATIVE_STATUS_CHOICES = {
    'utilized': 'Утилизирован - кафе уничтожило заказ, за которым не явились вовремя',
    'canceled_by_cafe': 'Отменен заведением',
    'canceled_by_user': 'Отменен пользователем',
}

complete_statuses = [
    'delivered',
    'utilized',
    # 'canceled_by_cafe',
    # 'canceled_by_user',
    ]

user_data = {
    "telegram_user_id": None,
    "telegram_horeca_id": None,
    "enter_key": None,
    "order_id": None,
    "status": None,
}

first_short_inline_buttons = {
    '⏬': 'maximize',
    'статус  ▶️': 'next_status',
}

between_short_inline_buttons = {}
between_short_inline_buttons['◀️ статус'] = 'previous_status'
between_short_inline_buttons.update(first_short_inline_buttons)

first_extended_inline_buttons = {
    '⏫': 'minimize',
    'статус  ▶️': 'next_status',
}
between_extended_inline_buttons = {}
between_extended_inline_buttons['◀️ статус'] = 'previous_status'
between_extended_inline_buttons.update(first_extended_inline_buttons)

addition_inline_buttons = {
    '⛔️ отменить': "canceled_by_cafe"
}
cancelled_by_cafe_status = 'canceled_by_cafe'

context_menu_list = set(first_extended_inline_buttons.values()).union(set(first_short_inline_buttons.values())).\
    union(set(between_short_inline_buttons.values())).union(set(between_extended_inline_buttons.values())).\
    union(set(addition_inline_buttons.values()))

user_table_name = "mokka"
database_user_create_table_Postgres = f"CREATE TABLE IF NOT EXISTS {user_table_name} " \
                             "(id SERIAL PRIMARY KEY, telehram_user_id INT, " \
                             "verification_code VARCHAR(150), order_id JSONB, " \
                             "horeca_id JSONB, status JSONB, bot_subscribing BOOL);"
database_user_create_table_SQLite = f"CREATE TABLE IF NOT EXISTS {user_table_name} " \
                             "(id INTEGER PRIMARY KEY, telehram_user_id INT, " \
                             "verification_code VARCHAR(150), order_id JSONB, " \
                             "horeca_id JSONB, status JSONB, bot_subscribing BOOL);"

status_text_customer = "Ваш заказ №"

you_have_any_order = "Sorry, You have any order"

mock_test = [
    "UPDATE mokka SET status='placed' WHERE id=1",
    "UPDATE mokka SET status='in_progress' WHERE id=2",
    "UPDATE mokka SET status='ready' WHERE id=3",
    "UPDATE mokka SET status='delivered' WHERE id=4",
]

# ------------------ database -------------------
use_database = "Postgres" # SQLite or Postgres
SQLite_path = "./coffee_customer_bot_apps/database/"
SQLite_name = "coffee.db"

#---------------- MOCK DATA -------------------
mock_object = [
    {
        "telegram_user_id": 648154559,
        "status": "placed",
        "telegram_horeca_id": 658965231,
        "order_description": [
            "американо",
            "американо",
            "кепка",
            "пирог с вишней"
        ],
        "enter_key": "8e2b8d",
        "order_id": "79cfba",
        "horeca_name": "Golden CaFE"
    },
{
        "telegram_user_id": 588655489,
        "status": "placed",
        "telegram_horeca_id": 588655489,
        "order_description": [
            "каппуч",
            "сахар",
            "мед",
            "корица"
        ],
        "enter_key": "8e2hhg8d",
        "order_id": "FFcf65",
        "horeca_name": "Vasilki"
    },
]
