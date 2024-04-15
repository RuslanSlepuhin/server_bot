import configparser
from _debug import debug

# api_id = os.getenv('api_id')
# api_hash = os.getenv('api_hash')
# username = os.getenv('username')
# token = os.getenv('token')
#
config_keys = configparser.ConfigParser()
config_keys.read("./settings/config_keys.ini")
if not debug:
    api_id = config_keys['Telegram']['api_id']
    api_hash = config_keys['Telegram']['api_hash']
    username = config_keys['Telegram']['username']
    token = config_keys['Token']['token']
    talking_token = config_keys['Token_talking_bot']['token']
    token_red = config_keys['Token']['token_red']
    api_id_double = config_keys['Telegram_double']['api_id']
    api_hash_double = config_keys['Telegram_double']['api_hash']
    username_double = config_keys['Telegram_double']['username']
    individual_tg_bot = config_keys['Individual_tg_bot']['token']
    db_url = config_keys['DB_local_clone']['DB_URL']
else:
    api_id = config_keys['Telegram_TEST']['api_id']
    api_hash = config_keys['Telegram_TEST']['api_hash']
    username = config_keys['Telegram_TEST']['username']
    token = config_keys['Token_TEST']['token']
    talking_token = config_keys['Token_talking_bot_TEST']['token']
    token_red = config_keys['Token_TEST']['token_red']
    api_id_double = config_keys['Telegram_double_TEST']['api_id']
    api_hash_double = config_keys['Telegram_double_TEST']['api_hash']
    username_double = config_keys['Telegram_double_TEST']['username']
    individual_tg_bot = config_keys['Individual_tg_bot']['token']
    db_url = config_keys['DB_local_clone']['DB_URL']

