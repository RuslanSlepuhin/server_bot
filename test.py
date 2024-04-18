import asyncio

from report.reports import Reports

from sites.hh_get_report_links import HhLinks

hh = HhLinks(main_class=None, bot_dict=None, report=Reports())
asyncio.run(hh.get_content(words_pattern=['junior']))
# param = "WHERE profession=\"backend\""
#
# async def get():
#     response = await db.get_all_from_db_async(
#         table_name='admin_last_session',
#         param=param,
#         field='id'
#     )
#     print(response)
#
# asyncio.run(get())