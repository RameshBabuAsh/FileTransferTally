import sqlite3

def setup_database():
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT NOT NULL UNIQUE)''')

    c.execute('''CREATE TABLE IF NOT EXISTS group_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (group_id) REFERENCES groups(id),
                    FOREIGN KEY (user_id) REFERENCES users(id))''')

    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    log_message TEXT NOT NULL)''')

    conn.commit()
    conn.close()
