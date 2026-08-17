import sqlite3


class Users:
    def __init__(self):
        self.db_path = 'old_users.db'


    def get_connection(self):
        return sqlite3.connect(self.db_path)


    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    last_name TEXT,
                    username TEXT,
                    count_message INTEGER,
                    conversation TEXT
                )
                '''
            )


            conn.commit()


    def add_user(self, user_id, name, last_name, username):
        with self.get_connection() as conn:
            cursor = conn.cursor()


            cursor.execute('SELECT user_id FROM Users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()


            if user is None:
                cursor.execute(
                    '''INSERT INTO Users (user_id, name, last_name, username)
                       VALUES (?, ?, ?, ?)''',
                    (user_id, name, last_name, username)
                )

            conn.commit()



    def update_conversation(self, user_id, new_message):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT conversation FROM Users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row is None:
                # если юезра нет — создаём запись с этим сообщением
                cursor.execute(
                    'INSERT INTO Users (user_id, conversation) VALUES (?, ?)',
                    (user_id, new_message)
                )
            else:
                # если уже есть — дописываем через \n
                current = row[0] or ""  # может быть None
                updated = current + "\n" + new_message if current else new_message
                cursor.execute(
                    'UPDATE Users SET conversation = ? WHERE user_id = ?',
                    (updated, user_id)
                )
            conn.commit()




    def get_full_conversation(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT conversation FROM Users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            return row[0] if row else ""




    def get_messages_list(self, user_id):
        history = self.get_full_conversation(user_id)
        if not history:
            return []


        messages = []
        for line in history.split("\n"):
            if ": " in line:
                role, content = line.split(": ", 1)
                messages.append({"role": role, "content": content})
        return messages




    def clean_history(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Users SET conversation = ? WHERE user_id = ?',('updated', user_id))