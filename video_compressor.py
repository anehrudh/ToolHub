import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import *
import customtkinter
from PIL import Image, ImageTk
import mysql.connector
import time
import datetime

if '__main__' == __name__:

    x = 0


    def toggle_value():
        global x
        if x == 0:
            customtkinter.set_appearance_mode("light")
            x = 1
        else:
            x = 0
            customtkinter.set_appearance_mode("dark")


    def browse_input_file():
        # Get input file path
        input_file = filedialog.askopenfilename(
            filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")]
        )
        if input_file:
            input_file_entry.delete(0, tk.END)
            input_file_entry.insert(tk.END, input_file)


    def browse_save_destination():
        # Get output file path
        output_file = filedialog.asksaveasfilename(
            defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")]
        )
        if output_file:
            output_file_entry.delete(0, tk.END)
            output_file_entry.insert(tk.END, output_file)


    def convert_video():
        # Get input file path
        input_file = input_file_entry.get()
        if not input_file:
            messagebox.showerror("Error", "Please select an input file.")
            return

        # Get output file path
        output_file = output_file_entry.get()
        if not output_file:
            messagebox.showerror("Error", "Please select a destination file.")
            return

        # Get conversion percentage
        conversion_percentage = conversion_entry.get()
        if not conversion_percentage:
            messagebox.showerror("Error", "Please enter a conversion percentage.")
            return

        # Convert the video
        try:
            video = VideoFileClip(input_file)
            new_width = int(video.w * float(conversion_percentage) / 100)
            new_height = int(video.h * float(conversion_percentage) / 100)
            video_resized = video.resize((new_width, new_height))
            video_resized.write_videofile(output_file, codec="libx264", bitrate="450k")

            messagebox.showinfo("Conversion Complete", "Video conversion completed!")

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

            total = str(total_hours) + "h:" + str(total_minutes) + "m:" + str(total_seconds) + "s"
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
                "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('VIDEO COMPRESSOR','{}','{}','{}','{}')".format(
                    date, entry_time, exit_time, total
                )
            )
            db_connection.commit()

            db_cursor.execute("SELECT * FROM total WHERE tool_name = 'Video_Compressor'")
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
                "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='Video_Compressor'".format(
                    ttttt
                )
            )
            db_connection.commit()
            db_cursor.close()
            db_connection.close()

            # connection to database
            db_connection = mysql.connector.connect(
                host="db4free.net",
                user="teamtoolhub",
                password="t00lhub123",
                database="toolhub",
            )

            # tracking tool usage
            db_cursor = db_connection.cursor()

            db_cursor.execute("SELECT * FROM report WHERE tool_id = 'VidComp'")

            result = db_cursor.fetchone()

            if result:
                tool_usage = result[2]  # Access the tool_usage column
                print("TOTAL Video Compresser USAGE:", tool_usage)

                # UPDATING
                tool_usage = tool_usage + 1
                print(tool_usage)
                x = 3

                db_cursor.execute(
                    "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='VidComp'"
                )

            db_connection.commit()

            db_cursor.close()
            db_connection.close()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")


    # Create Tkinter window
    window = customtkinter.CTk()
    window.title("Video Converter")
    window.geometry("600x400")
    window.resizable(0, 0)
    window.iconbitmap(
       "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\compressor.ico"

    )


    top_frame = customtkinter.CTkFrame(window)
    top_frame.pack(side="top")

    add_folder_image = ImageTk.PhotoImage(
        Image.open(
            "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\compressor.png"

        ).resize((30, 30), Image.ANTIALIAS)
    )

    header_label = customtkinter.CTkLabel(
        top_frame,
        font=customtkinter.CTkFont(family="Torus Notched SemiBold", size=20, weight="bold"),
        text="Video Compressor",
        anchor=customtkinter.N,
        image=add_folder_image,
        compound="left",
    )

    # using the grid() method to set the position of the labels in the grid format
    header_label.grid(row=0, column=0, padx=5, pady=5)

    frame1 = customtkinter.CTkFrame(window)
    frame1.pack(pady=15)

    frame2 = customtkinter.CTkFrame(window)
    frame2.pack(pady=15)

    frame3 = customtkinter.CTkFrame(window)
    frame3.pack(pady=15)

    frame4 = customtkinter.CTkFrame(window)
    frame4.pack()


    # text for input file
    text1 = customtkinter.CTkLabel(
        frame1,
        text="Choose Input Video",
        font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=14),
    )
    text1.pack(ipadx=38, padx=5, pady=5, expand=True, fill=tk.BOTH, side=tk.LEFT)
    # Input File Entry
    input_file_entry = customtkinter.CTkEntry(frame1)
    input_file_entry.pack(
        ipadx=40, padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT
    )
    # Browse Input Video button
    browse_input_button = customtkinter.CTkButton(
        frame1, text="Browse Input Video", command=browse_input_file
    )
    browse_input_button.pack(
        ipadx=30, padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT
    )


    # text for output file
    text2 = customtkinter.CTkLabel(
        frame2,
        text="Choose Output Destination",
        font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=14),
    )
    text2.pack(ipadx=10, padx=5, pady=5, expand=True, fill=tk.BOTH, side=tk.LEFT)

    # Output File Entry
    output_file_entry = customtkinter.CTkEntry(frame2)
    output_file_entry.pack(
        ipadx=40, padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT
    )


    # Browse Save Destination button
    browse_save_button = customtkinter.CTkButton(
        frame2, text="Browse Save Destination", command=browse_save_destination
    )
    browse_save_button.pack(
        ipadx=30, padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT
    )


    # Conversion Percentage entry
    conversion_label = customtkinter.CTkLabel(
        frame3,
        text="Conversion Percentage%",
        font=customtkinter.CTkFont(family="Bahnschrift SemiBold", size=14),
    )
    conversion_label.pack(
        ipadx=30, padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT
    )
    conversion_entry = customtkinter.CTkEntry(frame3)
    conversion_entry.pack(
        ipadx=30, padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.RIGHT
    )

    # Convert button
    convert_button = customtkinter.CTkButton(frame4, text="Convert", command=convert_video)
    convert_button.pack(ipadx=30, padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.LEFT)


    appearence_button = customtkinter.CTkButton(
        frame4, text="Appearence Toggle", width=100, command=toggle_value
    )
    appearence_button.pack(
        ipadx=30, padx=10, pady=10, fill=tk.BOTH, expand=True, side=tk.RIGHT
    )

    # Run the Tkinter event loop
    window.mainloop()



