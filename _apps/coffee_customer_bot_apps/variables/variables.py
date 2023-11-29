
# Requests variables
customer_pressed_cancel_endpoint = "https://test.ru"
customer_feedback_endpoint = "https://test.ru"
customer_add_username_to_database_endpoint = "https://test.ru"

# Endpoints variables
is_user_active_endpoint = "/is_user_active"
provide_message_to_user_endpoint = "/provide_message_to_user"
impossible_to_cancel_order_endpoints = "/impossible_to_cancel_order"
user_verification_endpoint = "/verification"
provide_message_to_horeca_endpoint = "/provide_message_to_horeca"

#--------------- server urls ---------------
server_test_status_endpoint_from_customer = "/client/status_from_user/" # take the POST from customer to send to horeca
server_test_status_endpoint_from_horeca = "/client/status_from_horeca/" # take the POST from horeca to send to customer
# GET# -> take json from customer with verification code and user_id
# POST -> {"user_id": user_id:int , "verification_code": verification_code:str}
verification_endpoint = "/client/enter_key_from_user/"

request_exists_user_id = "/user-id-exists/"
get_user_verification_info = "/client/user-info/" # GET

get_user_data = "/client/user_info/"
# -------------- common info --------------
main_endpoint = "http://127.0.0.1:5000/is_user_active"
# server_domain = "http://127.0.0.1:7000"
server_domain = "https://fcmapi.herokuapp.com" # tunnel
customer_bot_domain = "http://127.0.0.1:5000"
horeca_bot_domain = "http://127.0.0.1:5000"

customer_bot_name = "@a34fgh5_bot"
horeca_bot_name = "@a34fgh6_bot"

get_subscribe_status = "/subscribe-status/"

n = 5502797471
rus = 5884559465

dialog_customer = {
    "verification": "Введите верификационный код",
    "verification_error": "Верификация неуспешна, проверьте правильность кода",
}

USER_STATUS_BUTTONS = {
    'canceled_by_user': 'Отменен пользователем',
    'feedback': "Оставить отзыв",
}

customer_buttons_status = {}
for key in USER_STATUS_BUTTONS:
    customer_buttons_status[USER_STATUS_BUTTONS[key]] = key


# Выбор статуса заказа
BARISTA_STATUS_CHOICES = {
    # {'payment_process', 'В процессе оплаты'},
    # {'placed', 'Размещен - успешно оплачен'},
    'in_progress': 'В работе - Чек вышел бариста',
    'ready': 'Готов - Заказ готов к передаче',
    'delivered': 'Выдан - получен клиентом',
}


BARISTA_NEGATIVE_STATUS_CHOICES = {
    'utilized': 'Утилизирован - кафе уничтожило заказ, за которым не явились вовремя',
    'canceled_by_cafe': 'Отменен заведением',
}

complete_statuses = [
    'delivered',
    'utilized',
    'canceled_by_cafe',
    'canceled_by_user',
    ]

user_data = {
    "telegram_user_id": None,
    "telegram_horeca_id": None,
    "enter_key": None,
    "order_id": None,
    "status": None,
}
user_table_name = "mokka"
database_user_create_table = f"CREATE TABLE IF NOT EXISTS {user_table_name} " \
                             "(id SERIAL PRIMARY KEY, telehram_user_id INT, " \
                             "verification_code VARCHAR(150), order_id JSONB, " \
                             "horeca_id JSONB, status JSONB, bot_subscribing BOOL);"

status_text_customer = "Ваш заказ №"