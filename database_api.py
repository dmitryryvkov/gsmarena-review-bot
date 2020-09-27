
import sqlite3


class DatabaseAPI:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status=True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM subscriptions WHERE status = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id, status):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM subscriptions WHERE user_id = ? AND status =?",
                                         (user_id, status)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status):
        with self.connection:
            return self.cursor.execute("INSERT INTO subscriptions (user_id, status) VALUES (?,?)",
                                       (user_id, status))

    def update_subscriptions(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE subscriptions SET status = ? WHERE user_id=?", (status, user_id))

    def close(self):
        self.connection.close()
