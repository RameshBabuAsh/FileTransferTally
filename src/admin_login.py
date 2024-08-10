# src/admin_login.py
import sqlite3

def create_admin_db():
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_admin_db()
    print("Admin database setup completed.")
