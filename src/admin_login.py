import sqlite3
import hashlib

def admin_login(username, password):
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, hashed_password))
    result = c.fetchone()
    conn.close()
    
    if result:
        print(f"Welcome, {username}!")
        return True
    else:
        print("Login failed. Incorrect username or password.")
        return False

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    admin_login(username, password)
