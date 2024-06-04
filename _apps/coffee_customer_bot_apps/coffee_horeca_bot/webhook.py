import sys

from aiogram import types
from aiohttp import web

class WebHoock:
    def __init__(self, bot_class):
        self.main = bot_class

    async def webhook_handler(self, request):
        try:
            update = await request.json()
            try:
                await self.main.dp.process_update(types.Update(**update))
            except IndexError as e:
                print(f"IndexError in process_update: {e} at line {sys.exc_info()[-1].tb_lineno}")
                pass
        except Exception as e:
            print(f"Error handling request: {e}")
            return web.Response(status=500)
        return web.Response()

    async def get_new_order(self, request):
        data = await request.json()
        data = [data] if type(data) not in [tuple, list, set] else data
        for object in data:
            await self.main.methods.new_order(order=object)
        return web.Response()

    async def provide_message_from_customer(self, request):
        data = await request.json()
        await self.main.methods.horeca_send_message(data=data)
        return web.Response()

    async def is_horeca_active(self, request) -> web.json_response:
        horeca_user_id = request.path_qs.split("?")[-1]
        if 'horeca_user_id=' in horeca_user_id:
            horeca_user_id = horeca_user_id.split("=")[-1]
            if horeca_user_id.isdigit():
                response = await self.main.methods.check_available_bot(horeca_user_id)
                return web.json_response(response)
        return web.json_response(
            {'error': 'make sure that horeca_user_id is in the request arguments ?horeca_user_id=<number>'})
