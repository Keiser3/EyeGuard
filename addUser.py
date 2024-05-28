import sqlite3
import bcrypt
import tkinter as tk


def AddUser(first_name, last_name, email,password):
    try:
        conn = sqlite3.connect('USERS.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, password))
        # Commit the changes
        conn.commit()

        print("New user and user face inserted successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()
def insertUser():
        firstname = firstname_entry.get()
        lastname = lastname_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        password = password.encode('utf-8')
        hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
        AddUser(firstname, lastname, email,hashedPassword)
        


# Create the main window
parent = tk.Tk()
parent.geometry('400x400')
parent.title("Signup Form")

# Create and place the username label and entry
firstname_label = tk.Label(parent, text="firstname:")
firstname_label.pack()

firstname_entry = tk.Entry(parent)
firstname_entry.pack()


lastname_label = tk.Label(parent, text="lastname:")
lastname_label.pack()

lastname_entry = tk.Entry(parent)
lastname_entry.pack()


email_label = tk.Label(parent, text="Email:")
email_label.pack()

email_entry = tk.Entry(parent)
email_entry.pack()

# Create and place the password label and entry
password_label = tk.Label(parent, text="Password:")
password_label.pack()

password_entry = tk.Entry(parent, show="*")  # Show asterisks for password
password_entry.pack()

# Create and place the login button
login_button = tk.Button(parent, text="Login", command=insertUser)
login_button.pack()

# Start the Tkinter event loop
parent.mainloop()



