import asyncio
import os
from flask import Flask, request
from flask_cors import CORS


from _apps.coffee_customer_bot_apps.variables import variables

class Endpoints:
    def __init__(self, horeca_bot, customer_bot):
        self.db_request = None
        self.horeca_bot = horeca_bot
        self.customer_bot = customer_bot

    def main_endpoints(self, customer_bot, horeca_bot):
        app = Flask(__name__)
        CORS(app)

        @app.route("/", methods=['GET'])
        async def main_page():
            return {"message": "site was started"}

        @app.route(variables.is_user_active_endpoint, methods=['GET'])
        async def is_user_active():
            user_id = request.args.get('telegram_user_id')
            active = True
            return {"response": active}

        @app.route(variables.provide_message_to_user_endpoint, methods=['POST'])
        async def provide_message_to_user():
            data = request.json
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            await customer_bot.custom_send_message(data=data)
            return {"response": data}

        @app.route(variables.provide_message_to_horeca_endpoint, methods=['POST'])
        async def provide_message_to_horeca():
            data = request.json
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            await horeca_bot.custom_send_message(data=data)
            return {"response": data}

        @app.route(variables.impossible_to_cancel_order_endpoints, methods=['GET'])
        def impossible_to_cancel_order():
            return {"response": "good"}

        @app.route(f"{variables.get_subscribe_status}", methods=['GET'])
        def get_subscribe_status( *args, **kwargs):
            query = request.args
            if 'customer_bot' in query:
                status = asyncio.run(self.customer_bot.check_subscriber(user_id=int(query['telegram_user_id'])))
            elif 'horeca_bot' in query:
                status = asyncio.run(self.horeca_bot.check_subscriber(user_id=int(query['telegram_user_id'])))
                pass
            else:
                return {"error": "You need to provide the one of recipient bots like 'customer_bot' or 'horeca_bot' "}
            return {"status": status}

        @app.route(f"{variables.user_verification_endpoint}", methods=['POST'])
        def user_verification_endpoint( *args, **kwargs):
            # asyncio.run(self.customer_bot.)
            pass

        app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)))

