import asyncio
import os
from flask import Flask, request
from flask_cors import CORS

from _apps.coffee_customer_bot_apps.variables import variables

class Endpoints:
    def __init__(self):
        self.db_request = None

    def main_endpoints(self, customer_bot, horeca_bot):
        app = Flask(__name__)
        CORS(app)

        @app.route("/", methods=['GET'])
        async def main_page():
            return {"message": "site was started"}

        @app.route(variables.is_user_active_endpoint, methods=['GET'])
        async def is_user_active():
            user_id = request.args.get('user_id')
            active = True
            return {"response": active}

        @app.route(variables.provide_message_to_user_endpoint, methods=['POST'])
        async def provide_message_to_user():
            data = request.json
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            # loop = asyncio.get_event_loop()
            # loop.create_task(customer_bot.custom_send_message(data=data))
            # loop.run_until_complete(customer_bot.custom_send_message(data=data))
            await customer_bot.custom_send_message(data=data)
            return {"response": data}

        @app.route(variables.provide_message_to_horeca_endpoint, methods=['POST'])
        async def provide_message_to_horeca():
            data = request.json
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            # loop = asyncio.get_event_loop()
            # loop.create_task(horeca_bot.custom_send_message(data=data))
            # loop.run_until_complete(horeca_bot.custom_send_message(data=data))
            await horeca_bot.custom_send_message(data=data)
            return {"response": data}

        @app.route(variables.impossible_to_cancel_order_endpoints, methods=['GET'])
        def impossible_to_cancel_order():
            return {"response": "good"}

        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)))

