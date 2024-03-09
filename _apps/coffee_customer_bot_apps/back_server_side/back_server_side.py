import os
from flask import Flask, request, Response, jsonify
from flask_cors import CORS

from _apps.coffee_customer_bot_apps.database.database_methods import DataBase
from _apps.coffee_customer_bot_apps.variables import variables
import requests

class BackServer:
    def __init__(self, **kwargs):
        self.database = kwargs['database'] if 'database' in kwargs else DataBase()
        self.db_request = None

    def main_back_server(self):
        app = Flask(__name__)
        CORS(app)

        @app.route("/", methods=['GET'])
        def main_page():
            return {"message": "site was started"}

        # status from USER
        @app.route(f"{variables.server_status_from_customer}<order_id>", methods=['PUT'])
        def status_from_customer(order_id):
            data = request.json
            if self.database.update(data):
                print('data', data)
                url = f"{variables.horeca_bot_domain}{variables.provide_message_to_horeca_endpoint}"
                print(url)
                requests.post(url, json=data)
                return jsonify({"response": data})
            else:
                return jsonify({"response": "error"})

        # status from HORECA
        @app.route(f"{variables.server_status_from_horeca}<order_id>/", methods=['PUT'])
        def status_from_horeca(order_id):
            data = request.json
            # >>> save to db
            url = f"{variables.customer_bot_domain}{variables.provide_message_to_user_endpoint}"
            requests.post(url, json=data)
            return jsonify({"response": data})

        # USER- INFO
        @app.route(variables.user_info, methods=["GET"])
        def get_user_verification_info():
            response_list = []
            telegram_user_id = request.args.get('telegram_user_id')
            conditions = f"telegram_user_id={int(telegram_user_id)}"
            if 'active' in request.args:
                active = request.args.get('active')
                if active == 'true':
                    # negative_scenario = set(variables.BARISTA_NEGATIVE_STATUS_CHOICES.keys())
                    # complete_scenario = set(variables.complete_statuses)
                    # negative_scenario = negative_scenario.union(complete_scenario)
                    negative_scenario = set(variables.USER_STATUSES_NOT_SHOW.keys())
                    conditions += f" AND status NOT IN {tuple(negative_scenario)}"
            response = self.database.select_from("mokka", conditions)
            for i in response:
                response_list.append(from_list_to_dict(variables.fields, i))
            return jsonify({"response": response_list})


        # verification code
        @app.route(variables.verification_endpoint, methods=["POST"])
        def check_verification_code():
            code = '5212'
            if request.json['enter_key'] and request.json['enter_key'] == code:
                return jsonify({"message": "successfully"})
            else:
                return jsonify({"error": "unsuccessfully"})

        @app.route("/`mock`", methods=['GET'])
        async def mock():

            telegram_user_id = request.args.get('telegram_user_id') if 'telegram_user_id' in request.args else None
            for query in variables.mock_test:
                self.database.db_execute(query)

            if telegram_user_id:
                query = f"UPDATE mokka SET telegram_user_id={int(telegram_user_id)}, telegram_horeca_id={int(telegram_user_id)}"
                self.database.db_execute(query)

            return {"response": True}

        @app.route(variables.get_horeca_info, methods=["GET"])
        def get_horeca_info():
            response_list = []
            telegram_user_id = request.args.get('telegram_horeca_id')
            conditions = f"telegram_horeca_id={int(telegram_user_id)}"
            if 'active' in request.args:
                active = request.args.get('active')
                if active == 'true':
                    negative_scenario = set(variables.USER_STATUSES_NOT_SHOW.keys())
                    conditions += f" AND status NOT IN {tuple(negative_scenario)}"
            match variables.use_database:
                case "Postgres": response = self.database.select_from("mokka", conditions)
                case "SQLite": response = self.database.select_from("coffee", conditions)
            for i in response:
                response_list.append(from_list_to_dict(variables.fields, i))
            return jsonify(response_list)


        def from_list_to_dict(keys, values):
            response_dict = {}
            for i in range(0, len(values)):
                response_dict[keys[i]] = values[i]
            return response_dict

        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 7000)))


if __name__ == '__main__':
    ep = BackServer()
    ep.main_back_server()
