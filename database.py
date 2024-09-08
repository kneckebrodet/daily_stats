import mysql.connector
from datetime import datetime, timedelta

class MySQL:
    def __init__(self):
        self.db = mysql.connector.connect(
            user='root',
            password='saqr7ttxlucke',
            host='localhost',
            database='daily_stats'
        )

        self.cursor = self.db.cursor()

    def check_user_login(self, username):
        self.cursor.execute("SELECT * FROM users")
        all_users = self.cursor.fetchall()
        user_in_db = False
        userid = None
        for user_object in all_users:
            if username in user_object:
                user_in_db = True
                userid = user_object[0]
                break
        
        if user_in_db:
            return True, userid
        else:
            return False, None
        
    def check_if_entry_exists(self, id, table, date):
        query = "SELECT COUNT(*) FROM {} WHERE user_id = %s AND date = %s".format(table)

        self.cursor.execute(query,(id,date))
        exists = self.cursor.fetchone()
        if exists[0]:
            return True
        else:
            return False

    def add_data(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())

        query = "INSERT INTO {} ({}) VALUES ({})".format(table, columns, placeholders)

        self.cursor.execute(query, values)
        self.db.commit()

    def get_wakeup_time(self, id):
        today = str(datetime.now().date())
        try:
            query = f"SELECT time FROM wakeup_times WHERE user_id = {id} AND date = '{today}'"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except:
            return None
        
    def get_bedtime(self,id):
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        try:
            query = f"SELECT time FROM wakeup_times WHERE user_id = {id} AND date = '{yesterday}'"
            self.cursor.execute(query)
            return self.cursor.fetchone()[0]
        except:
            return None

    def update_data(self, id, table, data):
        today = str(datetime.now().date())
        # Construct the SET clause with the columns and new values
        set_clause = ", ".join([f"{key} = '{value}'" for key, value in data.items()])
        set_clause = set_clause.replace("False", "0")
        set_clause = set_clause.replace("True", "1")

        query = f"UPDATE {table} SET {set_clause} WHERE user_id = {id} AND date = '{today}'"
        
        self.cursor.execute(query)
        # Commit the changes to the database
        self.db.commit()

    def get_todo_list(self, id):
        query = f"SELECT task, detail FROM to_do_lists WHERE user_id = {id}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        todo_list = {}
        for row in results:
            task, detail = row
            todo_list[task] = detail

        return todo_list
    
    def remove_task_from_db(self, id, task_name):
        try:
            query = f"DELETE FROM to_do_lists WHERE user_id = {id} AND task = '{task_name}'"
            self.cursor.execute(query)
            self.db.commit()
            return 1
        except:
            return 0

    def get_stat(self, id, date, key):
        query = f"SELECT {key} FROM user_data WHERE user_id = {id} AND date = '{date}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0]
    
    def check_if_available(self, username):
        self.cursor.execute("SELECT username FROM users")
        all_users = self.cursor.fetchall()
        username_is_available = False
        for user in all_users:
            if username in user:
                username_is_available = False
                break
            else:
                username_is_available = True

        if username == "":
            return False, "Please fill out all fields"
        elif not username_is_available:
            return False, f"\"{username}\" is already taken"
        else:

            return True, f"Successfully added \"{username}\" to database"

    def add_user(self, username, password=""):
        query = f"INSERT INTO users (username) VALUES (%s)"
        new_user = (username,)

        self.cursor.execute(query, new_user)
        self.db.commit()
