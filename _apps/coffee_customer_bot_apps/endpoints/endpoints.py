import asyncio
import os

from aiohttp import web
from flask import Flask, request, jsonify
from flask_cors import CORS
from _apps.coffee_customer_bot_apps.variables import variables

class Endpoints:

    def __init__(self, horeca_bot=None, customer_bot=None):

        self.db_request = None
        self.horeca_bot = horeca_bot
        self.customer_bot = customer_bot

    def main_endpoints(self):
        app = Flask(__name__)
        CORS(app)

        @app.route("/", methods=['GET'])
        async def main_page():
            return jsonify({"message": "site was started"})

        # try to send the message to user
        @app.route(variables.is_user_active_endpoint, methods=['GET'])
        async def is_user_active():
            telegram_user_id = request.args.get('telegram_user_id')
            horeca_user_id = request.args.get('horeca_user_id')

            if telegram_user_id:
                response = await self.customer_bot.check_subscriber(telegram_user_id)
                return jsonify({"response": True}) if response else ({"response": False})

            if horeca_user_id:
                response = await self.horeca_bot.check_subscriber_horeca(horeca_user_id)
                return jsonify(response) if response else ({"response": False})

        # check subscribe
        @app.route(f"{variables.get_subscribe_status}", methods=['GET'])
        def get_subscribe_status(*args, **kwargs):
            query = request.args
            if 'customer_bot' in query:
                status = asyncio.run(self.customer_bot.check_subscriber(user_id=int(query['telegram_user_id'])))
            elif 'horeca_bot' in query:
                status = asyncio.run(self.horeca_bot.check_subscriber(user_id=int(query['telegram_user_id'])))
                pass
            else:
                return {"error": "You need to provide the one of recipient bots like 'customer_bot' or 'horeca_bot' "}
            return jsonify({"status": status})

        # message to customer
        @app.route(variables.provide_message_to_user_endpoint, methods=['POST'])
        async def provide_message_to_user():
            data = request.json
            # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            print('AFTER')
            await self.customer_bot.customer_custom_send_message(data=data)
            print("BEFORE")
            return jsonify({"response": data})

        # message to horeca
        @app.route(variables.provide_message_to_horeca_endpoint, methods=['POST'])
        async def provide_message_to_horeca():
            data = request.json
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            await self.horeca_bot.horeca_send_message(data=data)
            return jsonify({"response": data})

        # customer made a new order. Provide it to barista
        @app.route(variables.new_order_endpoint, methods=['POST'])
        async def new_order():
            data = request.get_json()
            response = await self.horeca_bot.new_order(order=data)
            return jsonify(response)

        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)))


if __name__ == '__main__':
    e = Endpoints(None, None)
    e.main_endpoints()

