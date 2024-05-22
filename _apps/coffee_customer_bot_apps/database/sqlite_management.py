import sqlite3
from functools import wraps
from _apps.coffee_customer_bot_apps.variables import database_variables as db_var

def sqlite_connections(func):
    @wraps(func)  # Эта строка сохраняет метаданные исходной функции
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(db_var.sqlite_db_path)
        result = func(conn, *args, **kwargs)
        conn.close()
        return result
    return wrapper

def execute_query(func):
    @wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = func(*args, **kwargs)
        cur = conn.cursor()
        cur.execute(query)
        return query
    return wrapper

@sqlite_connections
@execute_query
def create_tables():
    return db_var.create_log_messages_table

@sqlite_connections
@execute_query
def insert_into(data:dict, table_name:str=None) -> str:
    table = table_name if table_name else db_var.log_messages_table_name
    return get_query(data, table)

@sqlite_connections
@execute_query
def select_from(cur, selected_fields, conditions:dict, table_name:str=None) -> str:
    table_name = db_var.log_messages_table_name if not table_name else table_name
    selected_fields = ", ".join(selected_fields) if type(selected_fields) in [set, tuple, list] else selected_fields
    query = f"SELECT {selected_fields} from {table_name} {unpack_conditions(conditions)}"
    cur.execute(query)
    return cur.fetchall()

def get_query(data:dict, table:str) -> str:
    fields = ", ".join(tuple(data.keys()))
    values = tuple(data.values()) if len(data.keys()) > 1 else tuple(data.values())[0]
    return f"INSERT INTO {table} ({fields}) VALUES {values};" if len(data.keys()) > 1 else f"INSERT INTO {table} ({fields}) VALUES ({tuple(data.values())[0]})"

def unpack_conditions(conditions:dict) -> str:
    if conditions:
        condition_str = ["WHERE "]
        for key, value in conditions.items():
            condition_str.append(f"{key}={value}") if type(value) in [int] else condition_str.append(f"{key}='{value}'")
        return " AND ".join(condition_str)
    else:
        return ""

create_tables()