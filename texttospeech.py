import tkinter as tk
from tkinter import *
from tkinter import filedialog
import customtkinter
from tkinter.ttk import Combobox
import pyttsx3
import os
from PIL import Image, ImageTk
import mysql.connector
import time
import datetime

if "__main__" == __name__:
    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")

    root = customtkinter.CTk()
    root.title("Text to Speech")
    root.geometry("800x500")
    root.resizable(0, 0)
    root.configure(bg="#305065")
    root.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\textspeech1.ico"
)

    x = 0

    def toggle_value():
        global x
        if x == 0:
            customtkinter.set_appearance_mode("light")
            x = 1
        else:
            x = 0
            customtkinter.set_appearance_mode("dark")

    engine = pyttsx3.init()

    def speaknow():
        text = text_area.get(1.0, END)
        gender = gender_combobox.get()
        speed = speed_combobox.get()
        voices = engine.getProperty("voices")

        def setvoice():
            if gender == "Male":
                engine.setProperty("voice", voices[0].id)
                engine.say(text)
                engine.runAndWait()
            else:
                engine.setProperty("voice", voices[1].id)
                engine.say(text)
                engine.runAndWait()

        if text:
            if speed == "Fast":
                engine.setProperty("rate", 250)
                setvoice()
            elif speed == "Normal":
                engine.setProperty("rate", 150)
                setvoice()
            else:
                engine.setProperty("rate", 60)
                setvoice()

        db_connection = mysql.connector.connect(
            host="db4free.net",
            user="teamtoolhub",
            password="t00lhub123",
            database="toolhub",
        )

        # Create a cursor object to execute SQL queries
        db_cursor = db_connection.cursor()

        db_cursor.execute("SELECT * FROM report WHERE tool_id = 'ttospeech'")

        result = db_cursor.fetchone()

        if result:
            tool_usage = result[2]  # Access the tool_usage column
            print("TOTAL TOS USAGE:", tool_usage)

            # UPDATING
            tool_usage = tool_usage + 1
            print(tool_usage)
            x = 3

            db_cursor.execute(
                "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='ttospeech'"
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
                "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('TEXT TO SPEECH','{}','{}','{}','{}')".format(
                    date, entry_time, exit_time, total
                )
            )
            db_connection.commit()

            db_cursor.execute("SELECT * FROM total WHERE tool_name = 'Text_to_Speech'")
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
                "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='Text_to_Speech'".format(
                    ttttt
                )
            )
            db_connection.commit()
            db_cursor.close()
       

            db_connection.commit()

            db_cursor.close()
            db_connection.close()

            

    def export_as_mp3():
        text = text_area.get(1.0, END)
        filepath = filedialog.asksaveasfilename(
            defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")]
        )
        if filepath:
            voices = engine.getProperty("voices")
            gender = gender_combobox.get()
            if gender == "Male":
                engine.setProperty("voice", voices[0].id)
            else:
                engine.setProperty("voice", voices[1].id)
            engine.save_to_file(text, filepath)
            engine.runAndWait()

    # top frame
    # top_frame = customtkinter.CTkFrame(root, width=890, height=120)
    # top_frame.place(x=10, y=8)

    label3 = customtkinter.CTkLabel(
        root,
        text="Text to Speech",
        font=customtkinter.CTkFont(family="MS Sans Serif", size=40, weight="bold"),
    )
    label3.place(x=290, y=30)

    ##################
    label_1 = customtkinter.CTkLabel(
        root,
        text="Enter the text to convert to a audio",
        font=customtkinter.CTkFont(family="Sans Serif", size=18),
    )
    label_1.place(x=10, y=120)

    text_area = customtkinter.CTkTextbox(
        root,
        width=350,
        height=300,
        border_width=3,
        font=customtkinter.CTkFont(family="Ubuntu", size=18),
    )
    text_area.place(x=10, y=150)

    label = customtkinter.CTkLabel(
        root, text="VOICE", font=customtkinter.CTkFont(family="Ubuntu", size=18)
    )
    label.place(x=455, y=135)

    label1 = customtkinter.CTkLabel(
        root, text="SPEED", font=customtkinter.CTkFont(family="Ubuntu", size=18)
    )
    label1.place(x=600, y=135)

    gender_combobox = customtkinter.CTkComboBox(root, values=["Male", "Female"])
    gender_combobox.place(x=450, y=175)
    gender_combobox.set("Male")  # Leave the default value blank

    speed_combobox = customtkinter.CTkComboBox(root, values=["Fast", "Normal", "Slow"])
    speed_combobox.place(x=600, y=175)
    speed_combobox.set("Normal")

    imageicon = customtkinter.CTkImage(
        dark_image=Image.open(
            "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\speak.png"
        )
    )
    btn = customtkinter.CTkButton(
        root,
        text="Speak",
        compound=LEFT,
        image=imageicon,
        height=40,
        width=135,
        command=speaknow,
    )
    btn.place(x=450, y=285)

    imageicon2 = customtkinter.CTkImage(
        dark_image=Image.open(
            "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\download.png"
        )
    )
    save = customtkinter.CTkButton(
        root,
        text="Export MP3",
        compound=LEFT,
        image=imageicon2,
        height=40,
        width=135,
        command=export_as_mp3,
    )
    save.place(x=600, y=285)

    imageicon3 = customtkinter.CTkImage(
        dark_image=Image.open(
            "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\R.png"

        )
    )
    appearence_button = customtkinter.CTkButton(
        root,
        text="Appearence Toggle",
        command=toggle_value,
        height=40,
        width=135,
        image=imageicon3,
    )
    appearence_button.place(x=520, y=350)

    root.mainloop()


