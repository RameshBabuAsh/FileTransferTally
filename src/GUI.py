import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import sqlite3
import hashlib

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

    # Create a new window to manage groups
    group_window = tk.Toplevel()
    group_window.title("Manage Groups")

    tk.Button(group_window, text="Create Group", command=create_group).pack(pady=5)
    tk.Button(group_window, text="Delete Group", command=delete_group).pack(pady=5)
    tk.Button(group_window, text="Add Client to Group", command=add_client_to_group).pack(pady=5)
    tk.Button(group_window, text="Remove Client from Group", command=remove_client_from_group).pack(pady=5)


def send_files_to_group():
    group_name = simpledialog.askstring("Input", "Enter group name to send files to:")
    if not group_name:
        return

    # Select the file to send
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

                # Simulate sending file (In actual implementation, this would involve network transfer)
                success = simulate_file_send(client_name, file_path)
                
                if success:
                    log_message = f"Admin sent '{file_path}' to '{client_name}' in group '{group_name}'."
                else:
                    log_message = f"Failed to send '{file_path}' to '{client_name}' in group '{group_name}'. Client might be offline."

                # Log the activity
                c.execute('INSERT INTO logs (log_message) VALUES (?)', (log_message,))
                
            conn.commit()
        else:
            messagebox.showerror("Error", f"No clients found in group '{group_name}'.")
    else:
        messagebox.showerror("Error", "Group not found.")
    
    conn.close()

def simulate_file_send(client_name, file_path):
    # Placeholder for file sending logic
    # Return True if successful, False if failed
    return True  # Simulate success

def view_logs():
    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()

    c.execute('SELECT * FROM logs')
    logs = c.fetchall()

    log_window = tk.Toplevel()
    log_window.title("View Logs")

    text_widget = tk.Text(log_window, wrap=tk.WORD)
    text_widget.pack(expand=True, fill='both')

    for log in logs:
        text_widget.insert(tk.END, f"{log[2]} - {log[1]}\n")

    conn.close()

def join_group():
    global userName  # Ensure that the global variable is being accessed

    if not userName:
        messagebox.showerror("Error", "User is not logged in.")
        return

    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()

    # Fetch all available groups
    c.execute('SELECT group_name FROM groups')
    groups = c.fetchall()

    if not groups:
        messagebox.showinfo("Join Group", "No groups available to join.")
        conn.close()
        return

    group_list = [group[0] for group in groups]
    
    group_name = simpledialog.askstring("Input", f"Available groups: {', '.join(group_list)}\nEnter group name to join:")
    
    if group_name:
        # Get the user ID for the logged-in user
        c.execute('SELECT id FROM users WHERE username = ?', (userName,))
        user_id = c.fetchone()
        # Get the group ID for the entered group name
        c.execute('SELECT id FROM groups WHERE group_name = ?', (group_name,))
        group_id = c.fetchone()
        
        if user_id and group_id:
            try:
                c.execute('INSERT INTO group_members (group_id, user_id) VALUES (?, ?)', (group_id[0], user_id[0]))
                conn.commit()
                messagebox.showinfo("Success", f"You have joined the group '{group_name}'.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"You are already a member of the group '{group_name}'.")
        else:
            messagebox.showerror("Error", "Invalid group name or user not found.")
    
    conn.close()



def view_my_groups():
    global userName  # Ensure that the global variable is being accessed

    if not userName:
        messagebox.showerror("Error", "User is not logged in.")
        return

    conn = sqlite3.connect('file_sharing.db')
    c = conn.cursor()
    
    # Get the user ID for the logged-in user
    c.execute('SELECT id FROM users WHERE username = ?', (userName,))
    user_id = c.fetchone()
    
    if user_id:
        # Fetch the groups the user has joined
        c.execute('''SELECT groups.group_name 
                     FROM groups 
                     JOIN group_members ON groups.id = group_members.group_id 
                     WHERE group_members.user_id = ?''', (user_id[0],))
        groups = c.fetchall()
        
        if groups:
            group_list = [group[0] for group in groups]
            messagebox.showinfo("My Groups", f"You have joined the following groups: {', '.join(group_list)}")
        else:
            messagebox.showinfo("My Groups", "You have not joined any groups yet.")
    else:
        messagebox.showerror("Error", "User not found in the database.")
    
    conn.close()



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
