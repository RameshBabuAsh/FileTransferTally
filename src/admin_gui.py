import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

def register_admin():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, hashed_password))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Admin registered successfully")

def login_admin():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    conn = sqlite3.connect('admin.db')
    c = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, hashed_password))
    result = c.fetchone()
    conn.close()
    
    if result:
        messagebox.showinfo("Success", f"Welcome, {username}!")
    else:
        messagebox.showerror("Error", "Login failed. Incorrect username or password.")

app = tk.Tk()
app.title("Admin Login System")

frame = tk.Frame(app)
frame.pack(pady=20)

label_username = tk.Label(frame, text="Username:")
label_username.grid(row=0, column=0, pady=10)

entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1, pady=10)

label_password = tk.Label(frame, text="Password:")
label_password.grid(row=1, column=0, pady=10)

entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, pady=10)

button_login = tk.Button(frame, text="Login", command=login_admin)
button_login.grid(row=2, column=1, pady=10)

# button_register = tk.Button(frame, text="Register", command=register_admin)
# button_register.grid(row=2, column=1, pady=10)

app.mainloop()
