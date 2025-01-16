
import sqlite3
import tkinter as tk
from tkinter import messagebox

def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def register_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    
    conn.close()
    show_users()

def login_user():
    username = entry_username.get()
    password = entry_password.get()
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Success", "Login successful")
    else:
        messagebox.showerror("Error", "Invalid username or password")

def show_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    user_list.delete(0, tk.END)
    for user in users:
        user_list.insert(tk.END, f"ID: {user[0]}, Username: {user[1]}")

# Initialize database
create_database()

# Create GUI
root = tk.Tk()
root.title("Login Page")
root.geometry("300x350")

tk.Label(root, text="Username:").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password:").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login_user).pack()
tk.Button(root, text="Register", command=register_user).pack()

tk.Label(root, text="Registered Users:").pack()
user_list = tk.Listbox(root)
user_list.pack()

show_users()

root.mainloop()





  