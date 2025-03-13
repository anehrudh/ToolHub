import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo
from wikipedia import summary
import customtkinter
import pyperclip
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import mysql.connector
import time
import datetime

if "__main__" == __name__:
    x = 0

    def get_summary():
        try:
            answer.delete(1.0, tk.END)
            summary_text = summary(keyword_entry.get())
            answer.insert(tk.INSERT, summary_text)
            # Show the copy and export buttons when the answer is displayed
            copy_button.pack(side="left", padx=10, pady=10)
            pdf_button.pack(side="left", padx=10, pady=10)

            db_connection = mysql.connector.connect(
                host="db4free.net",
                user="teamtoolhub",
                password="t00lhub123",
                database="toolhub",
            )
            # Create a cursor object to execute SQL queries
            db_cursor = db_connection.cursor()

            db_cursor.execute("SELECT * FROM report WHERE tool_id = 'wiki'")

            result = db_cursor.fetchone()

            if result:
                tool_usage = result[2]  # Access the tool_usage column
                print("TOTAL WIKI USAGE:", tool_usage)

                # UPDATING
                tool_usage = tool_usage + 1
                print(tool_usage)
                x = 3

                db_cursor.execute(
                    "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='wiki'"
                )

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

               

                # Create a cursor object to execute SQL queries
                db_cursor = db_connection.cursor()

                db_cursor.execute(
                    "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('WIKIPEDIA SUMMARY','{}','{}','{}','{}')".format(
                        date, entry_time, exit_time, total
                    )
                )
                db_connection.commit()

                db_cursor.execute("SELECT * FROM total WHERE tool_name = 'Wikipedia_Summary'")
                result = db_cursor.fetchall()

                if result:
                    tme = str(result[0][1])

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
                    "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='Wikipedia_Summary'".format(
                        ttttt
                    )
                )
                db_connection.commit()
                db_cursor.close()
                

            db_connection.commit()

            db_cursor.close()
            db_connection.close()

        except Exception as error:
            showerror("Error", error)

    def copy_text():
        text = answer.get(1.0, tk.END)
        pyperclip.copy(text)

    def export_pdf():
        text = answer.get(1.0, tk.END)
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        if filepath:
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            paragraphs = text.split("\n")
            for para in paragraphs:
                p = Paragraph(para.strip(), styles["Normal"])
                story.append(p)
            doc.build(story)
            showinfo("Exported", "Answer has been exported as PDF.")

    def toggle_value():
        global x
        if x == 0:
            customtkinter.set_appearance_mode("light")
            x = 1
        else:
            x = 0
            customtkinter.set_appearance_mode("dark")

    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")

    root = customtkinter.CTk()
    root.title("Wikipedia Summary")
    root.geometry("770x520")
    root.resizable(False, False)
    root.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\wiki.ico")


    customtkinter.set_appearance_mode("dark")

    top_frame = customtkinter.CTkFrame(root)
    top_frame.pack(side="top", fill="x", padx=50, pady=10)

    bottom_frame = customtkinter.CTkFrame(root)
    bottom_frame.pack(side="top", fill="x", padx=10, pady=10)

    below_frame = customtkinter.CTkFrame(root)
    below_frame.pack()

    keyword_entry = customtkinter.CTkEntry(top_frame, width=400)
    keyword_entry.pack(side="left", ipady=6)

    search_button = customtkinter.CTkButton(
        top_frame, text="SEARCH", command=get_summary
    )
    search_button.pack(side="right")

    pdf_button = customtkinter.CTkButton(
        below_frame, text="EXPORT PDF", command=export_pdf
    )
    copy_button = customtkinter.CTkButton(below_frame, text="COPY", command=copy_text)

    scroll = customtkinter.CTkScrollbar(bottom_frame)
    answer = customtkinter.CTkTextbox(
        bottom_frame,
        width=760,
        height=370,
        font=("Arial", 28),
        yscrollcommand=scroll.set,
    )
    answer.pack(side="left", fill="y")
    scroll.pack(side="left", fill="y")

    # Hide the copy and export buttons initially
    copy_button.pack_forget()
    pdf_button.pack_forget()

    search_button.pack(side="right")

    appearence_button = customtkinter.CTkButton(
        below_frame, text="Appearence Toggle", command=toggle_value
    )
    appearence_button.pack(side="left", padx=10, pady=10)

    root.mainloop()

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
        host="db4free.net",
        user="teamtoolhub",
        password="t00lhub123",
        database="toolhub",
    )

    # Create a cursor object to execute SQL queries
    db_cursor = db_connection.cursor()

    db_cursor.execute(
        "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('WIKIPEDIA SUMMARY','{}','{}','{}','{}')".format(
            date, entry_time, exit_time, total
        )
    )
    db_connection.commit()

    db_cursor.execute("SELECT * FROM total WHERE tool_name = 'Wikipedia_Summary'")
    result = db_cursor.fetchall()

    if result:
        tme = str(result[0][1])

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
        "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='Wikipedia_Summary'".format(
            ttttt
        )
    )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
