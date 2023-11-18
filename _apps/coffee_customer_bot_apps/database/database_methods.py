import psycopg2
from coffee_customer_bot_apps.variables import variables


class DataBase:

    def connect(self):
        self.con = psycopg2.connect(
            database="coffee_bot",
            user='ruslan',
            password='12345',
            host='localhost',
            port='5432'
        )

    def db_execute(self, query, output_text=None):
        query = query if query else variables.database_user_create_table
        if not self.con:
            self.connect()
        cur = self.con.cursor()
        with self.con:
            print(query)
            cur.execute(query)
            print(output_text) if output_text else None

    def insert_data(self, insert_dict:dict):
        values = ""
        fields = ""
        for key in insert_dict:
            if insert_dict[key]:
                print(type(key))
                fields = fields + key,
                if type(insert_dict) in [str, bool]:
                    values += f"'{insert_dict[key]}', "
                else:
                    values += f"{str(insert_dict[key])}, "

        fields = fields[:-2]
        values = values[:-2]

        query = f"INSERT INTO {variables.user_table_name} ({fields}) VALUES ({values})"
        self.db_execute(query, "Done")
        pass








