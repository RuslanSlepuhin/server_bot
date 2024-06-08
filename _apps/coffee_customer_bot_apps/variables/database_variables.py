# sqlite_db_path = "./_apps/coffee_customer_bot_apps/database"
sqlite_db_path = "./_apps/coffee_customer_bot_apps/database/coffee_db.sqlite3"

tables = {
    "log_messages": {
        "table_name": "log_messages",
        "create_query": "CREATE TABLE IF NOT EXISTS log_messages (id INTEGER PRIMARY KEY, user_id INTEGER, messages_array TEXT);"
    },
    "users": {
        "table_name": "users",
        "create_query": "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id TEXT NOT NULL UNIQUE);"
    },
    "service_messages": {
        "table_name": "service_messages",
        "create_query": "CREATE TABLE IF NOT EXISTS service_messages (id INTEGER PRIMARY KEY, messages TEXT NOT NULL UNIQUE, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id));"
    },
    "order_messages": {
        "table_name": "order_messages",
        "create_query": "CREATE TABLE IF NOT EXISTS order_messages (id INTEGER PRIMARY KEY, messages TEXT NOT NULL UNIQUE, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id));"
    },
}
