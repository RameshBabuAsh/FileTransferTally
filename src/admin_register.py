import sqlite3
import hashlib

def register_admin(username, password):
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    print(f"Admin {username} registered successfully.")

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    register_admin(username, password)
