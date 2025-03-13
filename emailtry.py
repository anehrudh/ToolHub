import tkinter as tk
from tkinter import filedialog, messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
import customtkinter as CTk
import customtkinter as ttk
import customtkinter
import tkinter as tk
from tkinter import ttk
import mysql.connector
import time
import datetime

if "__main__" == __name__:
    x = 0

    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")

    def toggle_value():
        global x
        if x == 0:
            customtkinter.set_appearance_mode("light")
            x = 1
        else:
            x = 0
            customtkinter.set_appearance_mode("dark")

    def send_email(
        provider, email, password, subject, message, receiver_emails, attachment_file
    ):
        try:
            # SMTP server settings
            smtp_server = None
            smtp_port = None

            if provider == "Gmail":
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
            elif provider == "Outlook":
                smtp_server = "smtp-mail.outlook.com"
                smtp_port = 587
            elif provider == "Yahoo":
                smtp_server = "smtp.mail.yahoo.com"
                smtp_port = 587

            # Check if user logged in with the correct domain
            if not email.endswith(f"@{provider.lower()}.com"):
                raise ValueError("Invalid email domain!")

            # Login to SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email, password)

            # Send email to each receiver
            for receiver_email in receiver_emails:
                msg = MIMEMultipart()
                msg["From"] = email
                msg["To"] = receiver_email
                msg["Subject"] = subject

                # Attach message
                msg.attach(MIMEText(message, "plain"))

                # Attach attachment file
                if attachment_file:
                    attachment = open(attachment_file, "rb")
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        "attachment; filename= %s" % attachment_file,
                    )
                    msg.attach(part)

                # Send email
                server.sendmail(email, receiver_email, msg.as_string())

            server.quit()
            messagebox.showinfo("Success", "Emails sent successfully!")

            print("Window exited at:", time.strftime("%H:%M:%S"))
            exit_time = time.strftime("%H:%M:%S")
            date = time.strftime("%d:%m:%Y")
            print(date)

            exit_datetime = datetime.datetime.strptime(exit_time, "%H:%M:%S")
            entry_datetime = datetime.datetime.strptime(entry_time, "%H:%M:%S")

            time_difference = exit_datetime - entry_datetime

            total_hours = time_difference.seconds // 3600
            total_minutes = (time_difference.seconds % 3600) // 60
            total_seconds = (time_difference.seconds % 3600) % 60

            total = (
                str(total_hours) + "h:" + str(total_minutes) + "m:" + str(total_seconds) + "s"
            )
            print(total)

            total1 = total + total
            print(total1)

            # Print the total time
            print(
                f"Total time: {total_hours} hours, {total_minutes} minutes, {total_seconds} seconds"
            )

            db_connection = mysql.connector.connect(
                host="xxxxx",
                user="xxxxx",
                password="xxxxx",
                database="xxxxxx",
            )

            # Create a cursor object to execute SQL queries
            db_cursor = db_connection.cursor()

            db_cursor.execute(
                "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('BULK MAIL','{}','{}','{}','{}')".format(
                    date, entry_time, exit_time, total
                )
            )
            db_connection.commit()

            db_cursor.execute("SELECT * FROM total WHERE tool_name = 'BULK_MAIL'")
            result = db_cursor.fetchall()
            db_connection.commit()

            if result:
                tme = str(result[0][1])
                print(tme)

            db_connection.commit()

            x = total
            print("X=", total)
            y = tme
            print("Y=", tme)

            # Step 1: Parse the time strings
            x_parts = x.split(":")
            y_parts = y.split(":")
            x_hours, x_minutes, x_seconds = (
                map(int, x_parts[0].split("h")),
                map(int, x_parts[1].split("m")),
                map(int, x_parts[2].split("s")),
            )

            y_hours, y_minutes, y_seconds = (
                map(int, y_parts[0].split("h")),
                map(int, y_parts[1].split("m")),
                map(int, y_parts[2].split("s")),
            )
            print(y_parts)
            # Step 2: Convert to integers
            x_hours = int(next(x_hours))
            x_minutes = int(next(x_minutes))
            x_seconds = int(next(x_seconds))
            y_hours = int(next(y_hours))
            y_minutes = int(next(y_minutes))
            y_seconds = int(next(y_seconds))

            # Step 3: Add the values
            total_hours = x_hours + y_hours
            total_minutes = x_minutes + y_minutes
            total_seconds = x_seconds + y_seconds

            # Step 4: Adjust values if necessary
            if total_seconds >= 60:
                total_minutes += total_seconds // 60
                total_seconds = total_seconds % 60

            if total_minutes >= 60:
                total_hours += total_minutes // 60
                total_minutes = total_minutes % 60

            # Step 5: Format the resulting time
            ttttt = f"{total_hours}h:{total_minutes}m:{total_seconds}s"

            # Print the result
            print("Total time:", ttttt)

            db_cursor.execute(
                "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='BULK_MAIL'".format(
                    ttttt
                )
            )
            db_connection.commit()
            db_cursor.close()
            db_connection.close()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def login():
        def check_login():
            email = email_entry.get()
            password = password_entry.get()
            provider = provider_var.get()

            # Check if email and password are entered
            if not email or not password:
                messagebox.showerror("Error", "Please enter both email and password!")
                return

            # Check if the chosen provider matches the email domain
            if not email.endswith(f"@{provider.lower()}.com"):
                messagebox.showerror(
                    "Error", "Please choose the correct domain for your email!"
                )
                return

            db_connection = mysql.connector.connect(
                host="xxxxx",
                user="xxxxb",
                password="xxxxx",
                database="xxxxx",
            )

            # tracking tool usage
            db_cursor = db_connection.cursor()

            db_cursor.execute("SELECT * FROM report WHERE tool_id = 'bulkmail'")

            result = db_cursor.fetchone()

            if result:
                tool_usage = result[2]  # Access the tool_usage column
                print("TOTAL Image Converter USAGE:", tool_usage)

                # UPDATING
                tool_usage = tool_usage + 1
                print(tool_usage)
                x = 3

                db_cursor.execute(
                    "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='bulkmail'"
                )

            db_connection.commit()

            db_cursor.close()
            db_connection.close()

            # Hide the login window
            login_window.withdraw()

            # Open compose window
            compose(email, password, provider)

        login_window = customtkinter.CTk()
        login_window.title("Login")
        login_window.geometry("500x450")
        login_window.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\user.ico"
)

        top_frame = customtkinter.CTkFrame(
            login_window,
        )
        top_frame.pack(padx=10, pady=10, expand=True)

        title = customtkinter.CTkLabel(
            top_frame,
            text="Bulk Email Sender",
            font=customtkinter.CTkFont(family="Roboto", size=20, weight="bold"),
        )
        title.pack(expand=True)

        # creating tabview
        tabview = customtkinter.CTkTabview(login_window, width=800, height=800)
        tabview.pack()

        tabview.add("Login")
        tabview.add("About")

        tabview.tab("Login").grid_columnconfigure(
            0, weight=1
        )  # configure grid of individual tabs
        tabview.tab("About").grid_columnconfigure(0, weight=1)

        print("Window created at:", time.strftime("%H:%M:%S"))
        entry_time = time.strftime("%H:%M:%S")

        about_text = customtkinter.CTkLabel(
            tabview.tab("About"),
            text="INSTRUCTIONS:\n ",
            font=customtkinter.CTkFont(family="Kanit", size=25),
        )
        about_text.pack()

        about_text2 = customtkinter.CTkLabel(
            tabview.tab("About"),
            text=" \n 1.Bulk Email Sender is designed to send a mail to multiple \n user at a time. \n\n 2.Login with correct credentils such as \n email and password \n\n 3.Chosse the correct domain, according \n to email. \n\n 4.For gmail the password, should \n be the key password that provide by google,\n orginal password for gmail wont work \n for security purpose. \n\n 5.For all other domains orginal password will \n work, exept gmail.",
            font=customtkinter.CTkFont(family="Kanit", size=16),
            justify="left",
        )

        about_text2.pack(padx=10)

        email_label = customtkinter.CTkLabel(
            tabview.tab("Login"),
            text="Email:",
            font=customtkinter.CTkFont(family="Anton", size=16),
        )
        email_label.pack()
        email_entry = customtkinter.CTkEntry(tabview.tab("Login"))
        email_entry.pack(ipadx=25)

        password_label = customtkinter.CTkLabel(
            tabview.tab("Login"),
            text="Password:",
            font=customtkinter.CTkFont(family="Anton", size=16),
        )
        password_label.pack()
        password_entry = customtkinter.CTkEntry(tabview.tab("Login"), show="*")
        password_entry.pack(ipadx=25)

        # Default provider

        provider_label = customtkinter.CTkLabel(
            tabview.tab("Login"),
            text="Provider:",
            font=customtkinter.CTkFont(family="Anton", size=16),
        )
        provider_label.pack()

        provider_var = customtkinter.CTkOptionMenu(
            tabview.tab("Login"), values=["Gmail", "Outlook", "Yahoo"]
        )
        provider_var.pack(ipadx=25)

        login_button = customtkinter.CTkButton(
            tabview.tab("Login"), text="Login", command=check_login
        )
        login_button.pack(pady=40, ipadx=25)

        appearence_button = customtkinter.CTkButton(
            tabview.tab("Login"),
            text="Appearence Toggle",
            command=toggle_value,
        )
        appearence_button.pack(ipadx=25)

        login_window.mainloop()

    def compose(email, password, provider):
        def attach_file():
            attachment_file = filedialog.askopenfilename()
            attachment_file_entry.delete(0, tk.END)
            attachment_file_entry.insert(0, attachment_file)

        def attach_recipients():
            csv_file = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            recipient_emails = load_recipient_emails(csv_file)
            recipient_emails_text.delete(1.0, tk.END)
            recipient_emails_text.insert(tk.END, recipient_emails)

        def load_recipient_emails(csv_file):
            recipient_emails = []
            with open(csv_file, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    recipient_emails.extend(row)
            return ", ".join(recipient_emails)

        def send():
            subject = subject_entry.get()
            message = message_text.get("1.0", "end-1c")
            recipient_emails = recipient_emails_text.get("1.0", "end-1c")
            attachment_file = attachment_file_entry.get()

            receiver_emails = [email.strip() for email in recipient_emails.split(",")]

            send_email(
                provider,
                email,
                password,
                subject,
                message,
                receiver_emails,
                attachment_file,
            )

        compose_window = customtkinter.CTkToplevel()
        compose_window.title("Compose Email")
        compose_window.geometry("600x900")
        compose_window.resizable(0, 0)
        compose_window.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\email.ico"
)

        tabview = customtkinter.CTkTabview(compose_window, width=800, height=800)
        tabview.pack()

        tabview.add("Compose Mail")
        tabview.add("Note")

        tabview.tab("Compose Mail").grid_columnconfigure(
            0, weight=1
        )  # configure grid of individual tabs
        tabview.tab("Note").grid_columnconfigure(0, weight=1)

        note1 = customtkinter.CTkLabel(
            tabview.tab("Note"),
            text="INSTRUCTION:",
            font=customtkinter.CTkFont(family="Roboto", size=25, weight="bold"),
        )
        note1.pack(padx=10)

        note2 = customtkinter.CTkLabel(
            tabview.tab("Note"),
            text="1.In Compose Mail window you can send to multiple recipents \n 2.You can send by typing mail in textbox of \n recipent mail with comma after each email. \n 3.Or you can attach CSV format file to \n send multiple recipents at once \n 4.You can choose any sort of docs such as \n PDF,WORD,Docs etc to send",
            font=customtkinter.CTkFont(family="Roboto", size=18, weight="bold"),
        )
        note2.pack(pady=20)

        subject_label = customtkinter.CTkLabel(
            tabview.tab("Compose Mail"),
            text="Subject:",
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
        )
        subject_label.pack()

        subject_entry = customtkinter.CTkEntry(
            tabview.tab("Compose Mail"),
            border_width=3,
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
        )
        subject_entry.pack(ipadx=100, pady=10)

        message_label = customtkinter.CTkLabel(
            tabview.tab("Compose Mail"),
            text="Message:",
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
        )
        message_label.pack()

        message_text = customtkinter.CTkTextbox(
            tabview.tab("Compose Mail"),
            width=300,
            height=200,
            activate_scrollbars=True,
            border_width=3,
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
        )
        message_text.pack(pady=10)

        recipient_label = customtkinter.CTkLabel(
            tabview.tab("Compose Mail"),
            text="Recipient Emails:",
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
        )
        recipient_label.pack()

        recipient_emails_text = customtkinter.CTkTextbox(
            tabview.tab("Compose Mail"),
            width=300,
            height=100,
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
            border_width=3,
        )
        recipient_emails_text.pack()

        attach_recipients_button = customtkinter.CTkButton(
            tabview.tab("Compose Mail"),
            text="Attach Recipients",
            command=attach_recipients,
        )
        attach_recipients_button.pack(ipadx=30, pady=20)

        attachment_file_label = customtkinter.CTkLabel(
            tabview.tab("Compose Mail"),
            text="Attachment File:",
            font=customtkinter.CTkFont(family="Ubuntu", size=18),
        )
        attachment_file_label.pack(padx=10)

        attachment_file_entry = customtkinter.CTkEntry(
            tabview.tab("Compose Mail"),
            border_width=3,
        )
        attachment_file_entry.pack(ipadx=100)

        attachment_file_button = customtkinter.CTkButton(
            tabview.tab("Compose Mail"), text="Attach File", command=attach_file
        )
        attachment_file_button.pack(ipadx=30, pady=20)

        send_button = customtkinter.CTkButton(
            tabview.tab("Compose Mail"), text="Send", command=send
        )
        send_button.pack(ipadx=30, padx=10)

        compose_window.lift()  # Lift the compose window above the login window

        compose_window.mainloop()

    login()


