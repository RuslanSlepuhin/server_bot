# sqlite_db_path = "./_apps/coffee_customer_bot_apps/database"
sqlite_db_path = "./coffee_db.sqlite3"

log_messages_table_name = "log_messages"
create_log_messages_table = f"CREATE TABLE IF NOT EXISTS {log_messages_table_name} (id INTEGER PRIMARY KEY, user_id INTEGER, messages_array TEXT);"
