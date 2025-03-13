import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import customtkinter
import mysql.connector
import time
import datetime

if "__main__" == __name__:
    x = 0

    def toggle_value():
        global x
        if x == 0:
            customtkinter.set_appearance_mode("light")
            x = 1
        else:
            x = 0
            customtkinter.set_appearance_mode("dark")

    def convert_image():
        selected_format = format_var.get()
        if not selected_format:
            messagebox.showerror("Error", "Please select a format.")
            return

        file_path = file_var.get()
        if not file_path:
            messagebox.showerror("Error", "Please select an image.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{selected_format}",
            filetypes=[("Image files", f"*.{selected_format}")],
        )
        if not save_path:
            return

        filename, _ = os.path.splitext(file_path)

        try:
            im = Image.open(file_path)
            rgb_im = im.convert("RGB")
            save_filename = os.path.join(save_path)
            rgb_im.save(save_filename)
            messagebox.showinfo("Success", "File converted and saved successfully.")

            db_connection = mysql.connector.connect(
                host="db4free.net",
                user="teamtoolhub",
                password="t00lhub123",
                database="toolhub",
            )

            # tracking tool usage
            db_cursor = db_connection.cursor()

            db_cursor.execute("SELECT * FROM report WHERE tool_id = 'imageconv'")

            result = db_cursor.fetchone()

            if result:
                tool_usage = result[2]  # Access the tool_usage column
                print("TOTAL Image Converter USAGE:", tool_usage)

                # UPDATING
                tool_usage = tool_usage + 1
                print(tool_usage)
                x = 3

                db_cursor.execute(
                    "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='imageconv'"
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

                db_connection = mysql.connector.connect(
                    host="db4free.net",
                    user="teamtoolhub",
                    password="t00lhub123",
                    database="toolhub",
                )

                # Create a cursor object to execute SQL queries
                db_cursor = db_connection.cursor()

                db_cursor.execute(
                    "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('IMAGE CONVERTER','{}','{}','{}','{}')".format(
                        date, entry_time, exit_time, total
                    )
                )
                db_connection.commit()

                db_cursor.execute("SELECT * FROM total WHERE tool_name = 'Image_Converter'")
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
                    "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='Image_Converter'".format(
                        ttttt
                    )
                )
                db_connection.commit()
                db_cursor.close()
                

            db_connection.commit()

            db_cursor.close()
            db_connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def browse_image():
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        file_var.set(file_path)

    # window cereated
    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")

    # Create Tkinter window
    window = customtkinter.CTk()
    window.geometry("700x300")
    window.resizable(0, 0)
    window.title("Image Converter")
    window.iconbitmap( "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\imageconvert.ico"
)

    label = customtkinter.CTkLabel(window, text="IMAGE CONVERTER", font=("", 25))
    label.pack(pady=(40, 35))

    frame1 = customtkinter.CTkFrame(window)
    frame1.configure(width=100)
    frame1.pack()

    frame2 = customtkinter.CTkFrame(window)
    frame2.configure(width=100)
    frame2.pack(pady=(20, 0))

    # Browse image button
    browse_button = customtkinter.CTkButton(
        frame1, text="Browse Image", command=browse_image
    )
    browse_button.pack(pady=(5, 5), side="left")

    # Radio buttons for format selection
    format_var = tk.StringVar()
    format_var.set("gif")

    radio_button1 = customtkinter.CTkRadioButton(
        frame1, text="PNG", variable=format_var, value="png"
    )
    radio_button1.pack(padx=(20, 0), pady=(5, 5), side="left")

    radio_button2 = customtkinter.CTkRadioButton(
        frame1, text="JPEG", variable=format_var, value="jpeg"
    )
    radio_button2.pack(pady=(5, 5), side="left")

    radio_button3 = customtkinter.CTkRadioButton(
        frame1, text="GIF", variable=format_var, value="gif"
    )
    radio_button3.pack(pady=(5, 5), side="left")

    radio_button4 = customtkinter.CTkRadioButton(
        frame1, text="PPM", variable=format_var, value="ppm"
    )
    radio_button4.pack(pady=(5, 5), side="left")

    radio_button5 = customtkinter.CTkRadioButton(
        frame1, text="TIFF", variable=format_var, value="tiff"
    )
    radio_button5.pack(pady=(5, 5), side="left")

    # Single button for selecting save filename and converting
    save_convert_button = customtkinter.CTkButton(
        frame2, text="CONVERT & SAVE", command=convert_image
    )
    save_convert_button.pack(side="left")

    appearence_button = customtkinter.CTkButton(
        frame2, text="Appearence Toggle", command=toggle_value
    )
    appearence_button.pack(side="left", padx=10, pady=10)

    # Variable to store selected image file path
    file_var = tk.StringVar()

    window.mainloop()

    
