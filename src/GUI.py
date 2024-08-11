import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import hashlib
import sqlite3
import os
from client import connect_to_server
from server import BUFFER_SIZE
import time


userName = None
passWord = None

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    global userName
    userName = username
    global passWord
    passWord = password

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
            client_socket = connect_to_server()
            if client_socket:
                show_client_options(username, client_socket)
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
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Label(frame, text=f"Welcome, {admin_name} (Admin)").grid(row=0, column=0, padx=10, pady=10)

    tk.Button(frame, text="Manage Groups", command=manage_groups).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, text="Send Files", command=send_files_to_group).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(frame, text="View Logs", command=view_logs).grid(row=3, column=0, padx=10, pady=10)

def show_client_options(client_name, client_socket):
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Label(frame, text=f"Welcome, {client_name} (Client)").grid(row=0, column=0, padx=10, pady=10)
    tk.Button(frame, text="Join Group", command=lambda: join_group(client_socket)).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(frame, text="View My Groups", command=view_my_groups).grid(row=2, column=0, padx=10, pady=10)

def manage_groups():
    def create_group():
        group_name = simpledialog.askstring("Input", "Enter group name:")
        if group_name:
            conn = sqlite3.connect('file_sharing.db')
            c = conn.cursor()
            try:
                c.execute('INSERT INTO groups (group_name) VALUES (?)', (group_name,))
                conn.commit()
                messagebox.showinfo("Success", f"Group '{group_name}' created successfully.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Group name already exists.")
            finally:
                conn.close()

    def delete_group():
        group_name = simpledialog.askstring("Input", "Enter group name to delete:")
        if group_name:
            conn = sqlite3.connect('file_sharing.db')
            c = conn.cursor()
            c.execute('DELETE FROM groups WHERE group_name = ?', (group_name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Group '{group_name}' deleted successfully.")

    def add_client_to_group():
        group_name = simpledialog.askstring("Input", "Enter group name:")
        client_username = simpledialog.askstring("Input", "Enter client username:")
        if group_name and client_username:
            conn = sqlite3.connect('file_sharing.db')
            c = conn.cursor()
            c.execute('SELECT id FROM groups WHERE group_name = ?', (group_name,))
            group_id = c.fetchone()
            c.execute('SELECT id FROM users WHERE username = ?', (client_username,))
            user_id = c.fetchone()
            if group_id and user_id:
                c.execute('INSERT INTO group_members (group_id, user_id) VALUES (?, ?)', (group_id[0], user_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"Client '{client_username}' added to group '{group_name}'.")
            else:
                messagebox.showerror("Error", "Invalid group name or client username.")
            conn.close()

    def remove_client_from_group():
        group_name = simpledialog.askstring("Input", "Enter group name:")
        client_username = simpledialog.askstring("Input", "Enter client username:")
        if group_name and client_username:
            conn = sqlite3.connect('file_sharing.db')
            c = conn.cursor()
            c.execute('SELECT id FROM groups WHERE group_name = ?', (group_name,))
            group_id = c.fetchone()
            c.execute('SELECT id FROM users WHERE username = ?', (client_username,))
            user_id = c.fetchone()
            if group_id and user_id:
                c.execute('DELETE FROM group_members WHERE group_id = ? AND user_id = ?', (group_id[0], user_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"Client '{client_username}' removed from group '{group_name}'.")
            else:
                messagebox.showerror("Error", "Invalid group name or client username.")
            conn.close()

    group_management_window = tk.Toplevel(root)
    group_management_window.title("Group Management")

    tk.Button(group_management_window, text="Create Group", command=create_group).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(group_management_window, text="Delete Group", command=delete_group).grid(row=1, column=0, padx=10, pady=10)
    tk.Button(group_management_window, text="Add Client to Group", command=add_client_to_group).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(group_management_window, text="Remove Client from Group", command=remove_client_from_group).grid(row=3, column=0, padx=10, pady=10)


def send_file(client_socket, file_path, username):
    try:
        client_socket.send(username.encode('utf-8'))
        time.sleep(1)

        filename = os.path.basename(file_path)
        client_socket.send(filename.encode('utf-8'))
        time.sleep(1)

        # Send the file content
        with open(file_path, 'rb') as file:
            while (data := file.read(BUFFER_SIZE)):
                client_socket.send(data)
        
        print("File sent successfully.")
    except Exception as e:
        print(f"Failed to send file: {e}")


def send_files_to_group():
    group_name = simpledialog.askstring("Input", "Enter group name to send files to:")
    if not group_name:
        return

    file_path = filedialog.askopenfilename(title="Select a file")
    if not file_path:
        return

    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()

    c.execute('SELECT id FROM groups WHERE group_name = ?', (group_name,))
    group_id = c.fetchone()

    if group_id:
        c.execute('SELECT user_id FROM group_members WHERE group_id = ?', (group_id[0],))
        clients = c.fetchall()
        
        if clients:
            for client in clients:
                user_id = client[0]
                c.execute('SELECT username FROM users WHERE id = ?', (user_id,))
                client_name = c.fetchone()[0]

                client_socket = connect_to_server()
                if client_socket:
                    success = send_file(client_socket, file_path, client_name)
                    client_socket.close()
                
                if client_socket:
                    log_message = f"Admin sent '{file_path}' to '{client_name}' in group '{group_name}'."
                else:
                    log_message = f"Failed to send '{file_path}' to '{client_name}' in group '{group_name}'. Client might be offline."

                c.execute('INSERT INTO logs (log_message) VALUES (?)', (log_message,))
                
        else:
            messagebox.showerror("Error", "No clients found in this group.")
        
    else:
        messagebox.showerror("Error", "Invalid group name.")
    
    conn.commit()
    conn.close()

def join_group(client_socket):
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()

    c.execute('SELECT group_name FROM groups')
    groups = c.fetchall()

    group_list = [group[0] for group in groups]
    
    group_name = simpledialog.askstring("Input", f"Available groups: {', '.join(group_list)}\nEnter group name to join:")
    
    if group_name:
        global userName
        username = userName
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_id = c.fetchone()
        c.execute('SELECT id FROM groups WHERE group_name = ?', (group_name,))
        group_id = c.fetchone()
        
        if user_id and group_id:
            c.execute('INSERT INTO group_members (group_id, user_id) VALUES (?, ?)', (group_id[0], user_id[0]))
            conn.commit()
            messagebox.showinfo("Success", f"You have joined the group '{group_name}'.")
        else:
            messagebox.showerror("Error", "Invalid group name.")
    
    conn.close()

def view_logs():
    log_window = tk.Toplevel(root)
    log_window.title("View Logs")
    log_window.geometry("400x300")

    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    c.execute('SELECT log_message FROM logs')
    logs = c.fetchall()
    conn.close()

    log_text = tk.Text(log_window)
    log_text.pack(expand=True, fill='both')

    for log in logs:
        log_text.insert(tk.END, f"{log[0]}\n")

def view_my_groups():
    groups_window = tk.Toplevel(root)
    groups_window.title("My Groups")
    groups_window.geometry("300x200")

    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    c.execute('SELECT group_name FROM groups JOIN group_members ON groups.id = group_members.group_id JOIN users ON users.id = group_members.user_id WHERE users.username = ?', (userName,))
    groups = c.fetchall()
    conn.close()

    group_text = tk.Text(groups_window)
    group_text.pack(expand=True, fill='both')

    for group in groups:
        group_text.insert(tk.END, f"{group[0]}\n")

root = tk.Tk()
root.title("File Sharing System")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(frame, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

tk.Button(frame, text="Login", command=login_user).grid(row=2, column=0, padx=10, pady=10)
tk.Button(frame, text="Register", command=register_client).grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
