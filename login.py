import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt

# Function to verify login credentials
def login():
    email = entry_email.get()
    password = entry_password.get()
    password = password.encode('utf-8')
    
     
    # Connect to the SQLite3 database
    conn = sqlite3.connect('USERS.db')
    c = conn.cursor()

    # Query to check if the email and password are correct
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    result = c.fetchone()
    print(result)
    if result:
        if bcrypt.checkpw(password, result[4]):
             messagebox.showinfo("Login Success", "You have successfully logged in!")
             root.destroy()
             import main
    else:
        messagebox.showerror("Login Error", "Invalid email or password.")

    # Close the database connection
    conn.close()

# Create the main application window
root = tk.Tk()
root.geometry('400x400')
root.minsize(400,400)
image = tk.PhotoImage(file='Ressources/icons/1231006.png')
root.iconphoto(False,image)
root.title("Login Page")

# Create and place the email and password labels and entry widgets
label_email = tk.Label(root, text="email")
label_email.pack(pady=10)
entry_email = tk.Entry(root)

entry_email.pack(pady=10)

label_password = tk.Label(root, text="Password")
label_password.pack(pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=10)

# Create and place the login button
button_login = tk.Button(root, text="Login", command=login)
button_login.pack(pady=20)

# Start the main event loop
root.mainloop()




