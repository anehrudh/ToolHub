import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *
import customtkinter
import os
from tkinter import messagebox
from CTkMessagebox import CTkMessagebox

# Global dictionary to store sessions
sessions = {}


def login():
    username = username_entry.get()
    password = password_entry.get()

    # Perform login validation or other actions

    # Establish a connection to the MySQL database
    db_connection = mysql.connector.connect(
        host="db4free.net",
        user="teamtoolhub",
        password="t00lhub123",
        database="toolhub",
    )

    cursor = db_connection.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM admin")

    result = cursor.fetchone()

    # Add your own logic here
    if result:
        name = result[0]
        passw = result[1]

    if username == name and password == passw:
        session_id = 2435578  # Generate a session ID
        sessions[session_id] = username  # Store the username in the session
        print(sessions)
        os.system("python tool_report.py")
    else:
        CTkMessagebox(title="ERROR!", message="WRONG CREDENTIALS")


# Create the custom Tkinter GUI
root = customtkinter.CTk()
root.title("Login")
root.geometry("300x300")
root.resizable(0, 0)

admin_title = customtkinter.CTkLabel(
    root, text="ADMIN LOGIN", compound=LEFT, font=customtkinter.CTkFont(family="Roboto", size= 20,weight="bold")
)
admin_title.pack(pady=(20, 0))

# Create a frame to hold the login widgets
frame = customtkinter.CTkFrame(root)
frame.pack(pady=20)

# Username label and entry
username_label_frame = ttk.Frame(frame)
username_label_frame.grid(row=0, column=0, sticky=tk.W)

password_label = customtkinter.CTkLabel(frame, text="Username:", font=customtkinter.CTkFont(family="Roboto",size=15,weight="bold"), compound=LEFT)
password_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))

username_entry = customtkinter.CTkEntry(frame)
username_entry.grid(row=0, column=1)

# Password label and entry
password_label = customtkinter.CTkLabel(frame, text="Password:", font=customtkinter.CTkFont(family="Roboto",size=15,weight="bold"),compound=LEFT)
password_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 20), pady=(20, 0))

password_entry = customtkinter.CTkEntry(frame, show="*")
password_entry.grid(row=1, column=1, pady=(20, 0))

# Submit button
submit_button = customtkinter.CTkButton(root, text="Submit", command=login)
submit_button.pack(pady=10)

root.mainloop()
