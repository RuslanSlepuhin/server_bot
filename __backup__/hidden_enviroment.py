import configparser

config = configparser.ConfigParser()
config.read("./settings_/config.ini")

token = config['Token']['token']
token_test = config['Token2Token']['token']

api_id = config['Ruslan']['api_id']
api_hash = config['Ruslan']['api_hash']
username = '137336064'
username_test = 'test_ruslan'

