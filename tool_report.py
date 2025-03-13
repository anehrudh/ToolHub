import mysql.connector
import tkinter as tk
from tkinter import ttk
import customtkinter

# Create the custom Tkinter GUI
root = customtkinter.CTk()
root.title('Admin Panel')
root.geometry("1000x700")
root.resizable(0, 0)

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
        host="db4free.net",
        user="teamtoolhub",
        password="t00lhub123",
        database="toolhub",
    )

cursor = db_connection.cursor()

# Fetch data from the database
cursor.execute('SELECT * FROM user_time')

l1 = customtkinter.CTkLabel(root, text="TOOL REPORT",font=customtkinter.CTkFont(family="Roboto", size=20,weight="bold"))
l1.configure(font=('Arial', 30))
l1.pack(pady=(5, 15))

# Create a tabbed view
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True)

# Create a frame for the first tab
tab1_frame = customtkinter.CTkFrame(notebook)
tab1_frame.pack(fill=tk.BOTH, expand=True)

tab2_frame = customtkinter.CTkFrame(notebook)
tab2_frame.pack(fill=tk.BOTH, expand=True)

tab3_frame = customtkinter.CTkFrame(notebook)
tab3_frame.pack(fill=tk.BOTH, expand=True)

# Create a treeview for the first tab
tree = ttk.Treeview(tab1_frame)
tree['show'] = 'headings'

style = ttk.Style()

style.theme_use("default")

style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=30,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0,
                font=('Arial', 14))

style.map('Treeview', background=[('selected', '#22559b')])

style.configure("Treeview.Heading",
                background="#565b5e",
                foreground="white",
                relief="flat",
                font=('Arial', 14, 'bold'))

style.map("Treeview.Heading",
          background=[('active', '#3484F0')])

# Define number of columns
tree["columns"] = ("tool_name", "date_used", "entry_time",
                   "exit_time", "total_time")

# Assign the width and design
tree.column("tool_name", width=200, minwidth=150, anchor=tk.CENTER)
tree.column("date_used", width=200, minwidth=150, anchor=tk.CENTER)
tree.column("entry_time", width=200, minwidth=150, anchor=tk.CENTER)
tree.column("exit_time", width=200, minwidth=150, anchor=tk.CENTER)
tree.column("total_time", width=200, minwidth=150, anchor=tk.CENTER)

# Assign heading to the columns
tree.heading("tool_name", text="TOOL NAME", anchor=tk.CENTER)
tree.heading("date_used", text="DATE", anchor=tk.CENTER)
tree.heading("entry_time", text="ENTRY TIME", anchor=tk.CENTER)
tree.heading("exit_time", text="EXIT TIME", anchor=tk.CENTER)
tree.heading("total_time", text="TOTAL TIME", anchor=tk.CENTER)

# Insert data into the treeview
for row in cursor:
    tree.insert('', tk.END, values=row)

hsb = customtkinter.CTkScrollbar(tab1_frame, orientation="vertical")
hsb.configure(command=tree.yview)
tree.configure(yscrollcommand=hsb.set)

hsb.pack(fill="y", side="right")
tree.pack(fill=tk.BOTH, expand=True)

# Add the first tab to the notebook
notebook.add(tab1_frame, text="Overall Tool Report")
notebook.add(tab2_frame, text="Tool Total Time Usage")
notebook.add(tab3_frame, text="No of Times Tools Used")


#total tool usage


cursor.execute("SELECT * FROM total")

l1 = customtkinter.CTkLabel(tab2_frame, text="TOOL TOTAL USAGE")
l1.configure(font=customtkinter.CTkFont(family="Roboto",size= 20,weight="bold"))
l1.pack(pady=(5, 10))

# Create a frame to hold the Treeview widget
frame = customtkinter.CTkFrame(tab2_frame)
frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame)
tree["show"] = "headings"

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#2a2d2e",
    foreground="white",
    rowheight=30,  # Increase row height
    fieldbackground="#343638",
    bordercolor="#343638",
    borderwidth=0,
    font=("Arial", 14),
)  # Increase font size for row values

style.map("Treeview", background=[("selected", "#22559b")])

style.configure(
    "Treeview.Heading",
    background="#565b5e",
    foreground="white",
    relief="flat",
    font=("Arial", 14, "bold"),
)

style.map("Treeview.Heading", background=[("active", "#3484F0")])

# Define no of columns
tree["columns"] = ("tool_name", "total_time")

# assign the width and design
tree.column("tool_name", width=200, minwidth=150, anchor=tk.CENTER)
tree.column("total_time", width=200, minwidth=150, anchor=tk.CENTER)

# Assign heading to the column
tree.heading("tool_name", text="TOOL NAME", anchor=tk.CENTER)
tree.heading("total_time", text="TOTAL TIME/TOOL USAGE", anchor=tk.CENTER)

i = 0

names = ["WIKIPEDIA SUMMARY", "TEXT TO SPEECH", "IMAGE CONVERTER", "VIDEO COMPRESSOR","BULK MAIL","DICTIONARY GUI","YOUTUBE DOWNLOADER"]
for row in cursor:
    tree.insert("", i, text="", values=(names[i], row[1]))
    i = i + 1

hsb = customtkinter.CTkScrollbar(frame, orientation="vertical")
hsb.configure(command=tree.yview)
tree.configure(yscrollcommand=hsb.set)

hsb.pack(fill="y", side="right")
tree.pack(fill=tk.BOTH, expand=True)



cursor.execute("SELECT * FROM report")

l1 = customtkinter.CTkLabel(tab3_frame, text="TOOL REPORT",font=customtkinter.CTkFont(family="Roboto",size=20,weight="bold"))
l1.configure(font=("Arial", 30))
l1.pack(pady=(5, 15))

# Create a frame to hold the Treeview widget
frame = customtkinter.CTkFrame(tab3_frame)
frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame)
tree["show"] = "headings"

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="#2a2d2e",
    foreground="white",
    rowheight=30,  # Increase row height
    fieldbackground="#343638",
    bordercolor="#343638",
    borderwidth=0,
    font=("Arial", 14),
)  # Increase font size for row values

style.map("Treeview", background=[("selected", "#22559b")])

style.configure(
    "Treeview.Heading",
    background="#565b5e",
    foreground="white",
    relief="flat",
    font=("Arial", 14, "bold"),
)

style.map("Treeview.Heading", background=[("active", "#3484F0")])

# Define no of columns
tree["columns"] = ("tool_name", "tool_usage")

# assign the width and design
tree.column("tool_name", width=200, minwidth=150, anchor=tk.CENTER)
#
tree.column("tool_usage", width=200, minwidth=150, anchor=tk.CENTER)

# Assign heading to the column
tree.heading("tool_name", text="TOOL NAME", anchor=tk.CENTER)
#
tree.heading("tool_usage", text="TOOL USAGE", anchor=tk.CENTER)

i = 0

names = [
    "YOUTUBE DOWNLOADER",
    "WIKIPEDIA SUMMARY",
    "TEXT TO SPEECH",
    "IMAGE CONVERTER",
    "VIDEO COMPRESSOR",
    "BULK EMAIL SENDER",
    "DICTIONARY GUI",
]
for row in cursor:
    tree.insert("", i, text="", values=(names[i], row[2]))
    i = i + 1

hsb = customtkinter.CTkScrollbar(frame, orientation="vertical")
hsb.configure(command=tree.yview)
tree.configure(yscrollcommand=hsb.set)

hsb.pack(fill="y", side="right")
tree.pack(fill=tk.BOTH, expand=True)

# Close the database connection
db_connection.close()

root.mainloop()
