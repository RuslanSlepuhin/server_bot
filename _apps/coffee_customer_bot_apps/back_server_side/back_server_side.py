import os
from flask import Flask, request
from flask_cors import CORS
from _apps.coffee_customer_bot_apps.variables import variables
import requests

class BackServer:
    def __init__(self):
        self.db_request = None

    def main_back_server(self):
        app = Flask(__name__)
        CORS(app)

        @app.route("/", methods=['GET'])
        def main_page():
            return {"message": "site was started"}

        @app.route(variables.server_test_status_endpoint_from_customer, methods=['POST'])
        def status_from_customer():
            print('1')
            data = request.json
            print('data', data)
            url = f"http://127.0.0.1:7000{variables.provide_message_to_horeca_endpoint}"
            print(url)
            requests.post(url, json=data)
            return {"response": data}

        @app.route(variables.server_test_status_endpoint_from_horeca, methods=['POST'])
        def status_from_horeca():
            print('1')
            data = request.json
            print('data', data)
            url = f"http://127.0.0.1:7000{variables.provide_message_to_user_endpoint}"
            print(url)
            requests.post(url, json=data)
            return {"response": data}

        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)))

if __name__ == '__main__':
    ep = BackServer()
    ep.main_back_server()
