import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    result = c.fetchone()
    conn.close()
    
    if result:
        role = result[3]
        if role == "admin":
            show_admin_options(username)
        else:
            show_client_options(username)
    else:
        messagebox.showerror("Error", "Login failed. Incorrect username or password.")

def register_client():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, "client"))
        conn.commit()
        messagebox.showinfo("Success", "Client registered successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    finally:
        conn.close()

def show_admin_options(admin_name):
    # Clear the login screen
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Label(frame, text=f"Welcome, {admin_name} (Admin)").grid(row=0, column=0, padx=10, pady=10)

    tk.Button(frame, text="Manage Groups", command=manage_groups).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, text="Send Files", command=send_files_to_group).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(frame, text="View Logs", command=view_logs).grid(row=3, column=0, padx=10, pady=10)

def show_client_options(client_name):
    # Clear the login screen
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Label(frame, text=f"Welcome, {client_name} (Client)").grid(row=0, column=0, padx=10, pady=10)
    tk.Button(frame, text="Join Group", command=join_group).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, text="View My Groups", command=view_my_groups).grid(row=2, column=0, padx=10, pady=10)

def manage_groups():
    # Admin options to manage groups (create, delete, add/remove clients)
    pass

def send_files_to_group():
    # Admin option to send files to selected groups
    pass

def view_logs():
    # Admin option to view logs
    pass

def join_group():
    # Client option to join available groups
    pass

def view_my_groups():
    # Client option to view groups they have joined
    pass

# GUI setup
app = tk.Tk()
app.title("File Sharing System")

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

button_login = tk.Button(frame, text="Login", command=login_user)
button_login.grid(row=2, column=1, pady=10)

button_register = tk.Button(frame, text="Register as Client", command=register_client)
button_register.grid(row=3, column=1, pady=10)

app.mainloop()
