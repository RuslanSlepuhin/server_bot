import asyncio

from sites.scraping_hh import HHGetInformation

hh = HHGetInformation(main_class=None)
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