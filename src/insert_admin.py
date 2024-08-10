import sqlite3
import hashlib

def insert_admin(username, password):
    # Connect to the database
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Insert the admin user into the users table
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', 
                  (username, hashed_password, "admin"))
        conn.commit()
        print(f"Admin user '{username}' inserted successfully.")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()

# Replace these with your desired admin username and password
admin_username = "root"
admin_password = "root"

# Insert the admin
insert_admin(admin_username, admin_password)
