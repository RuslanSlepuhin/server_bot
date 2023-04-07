import asyncio

from db_operations.scraping_db import DataBaseOperations

db = DataBaseOperations()
param = "WHERE profession=\"backend\""

async def get():
    response = await db.get_all_from_db_async(
        table_name='admin_last_session',
        param=param,
        field='id'
    )
    print(response)

asyncio.run(get())