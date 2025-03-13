# importing the necessary modules
# Importing the necessary modules
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import key

import threading

import urllib.request
from io import BytesIO

import yt_dlp as youtube_dl
import re
import os

import customtkinter

import mysql.connector
import time
import datetime

if "__main__" == __name__:
    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")
    x = 0

    class YoutubeDownloadWindow(customtkinter.CTk):
        def db(self):
            db_connection = mysql.connector.connect(
                host="db4free.net",
                user="teamtoolhub",
                password="t00lhub123",
                database="toolhub",
            )

            # Create a cursor object to execute SQL queries
            db_cursor = db_connection.cursor()

            db_cursor.execute("SELECT * FROM report WHERE tool_id = 'yt'")

            result = db_cursor.fetchone()

            if result:
                db_cursor.execute(
                    "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='yt'"
                )

            db_connection.commit()

            db_cursor.close()
            db_connection.close()

        def get_unique_resolutions(self, inf_dict):
            resolutions = {}
            for format in inf_dict["formats"]:
                if re.match(r"^\d+p", format["format_note"]):
                    resolution_id = format["format_id"]
                    resolution = format["format_note"]
                    if "HDR" in resolution:
                        resolution = re.search(r"\d+p HDR", resolution)[0]
                    resolutions[resolution] = resolution_id

            resolutions = [(v, k) for k, v in resolutions.items()]
            return sorted(
                resolutions,
                key=lambda k: [int(k[1].split("p")[0]), k[1].split("p")[-1]],
            )

        def download_info_dict(self):
            ydl_opts = {
                "format": "bestvideo[ext=mp4]+bestaudio/best",
                "forcejson": True,
                "dump_single_json": True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.video_url.get(), download=False)
            return info_dict

        def download_thumbnail(self, url):
            with urllib.request.urlopen(url) as url:
                img_data = url.read()
            return img_data

        def create_pil_image(self, img_data):
            img = Image.open(BytesIO(img_data))
            img.thumbnail((120, 120))
            return img

        def create_photo_image(self, img):
            return ImageTk.PhotoImage(img)

        def display_image_and_title(self, info_dict, photo2):
            label = customtkinter.CTkLabel(self.image_frame, image=photo2)
            label.grid(row=0, padx=5, pady=5)
            label.configure(image=photo2)
            label.image = photo2

            text_label = customtkinter.CTkLabel(
                self.image_frame, text=info_dict["title"]
            )
            text_label.grid(row=1, padx=5, pady=5)

        def create_resolutions_label(self):
            resolutions_label = customtkinter.CTkLabel(
                self.entry_frame, text="Resolutions:", anchor=customtkinter.SE
            )
            resolutions_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

        def create_resolutions_dropdown(self, info_dict):
            resolutions = self.get_unique_resolutions(info_dict)
            self.resolutions_fields["values"] = [res[1] for res in resolutions]
            self.ids = {res[1]: res[0] for res in resolutions}
            self.resolutions_fields.current(0)
            self.resolutions_fields.grid(row=2, column=1, pady=5)

        def set_image(self):
            info_dict = self.download_info_dict()
            img_data = self.download_thumbnail(info_dict["thumbnail"])
            img = self.create_pil_image(img_data)
            photo2 = self.create_photo_image(img)
            self.display_image_and_title(info_dict, photo2)
            self.create_resolutions_label()
            self.create_resolutions_dropdown(info_dict)

        def progress_hook(self, data):
            if data["status"] == "downloading":
                downloaded = data["downloaded_bytes"]

                total = (
                    data["total_bytes"]
                    if data.get("total_bytes", None)
                    else data["total_bytes_estimate"]
                )
                percentage = downloaded / total * 100
                percentage = round(percentage, 2)

                self.progress_bar["value"] = percentage
                self.progress_bar.update()

                self.style.configure(
                    "text.Horizontal.TProgressbar", text="{:g} %".format(percentage)
                )

        def setup_ydl_opts(self):
            # Retrieve the string from the entry fields
            format = self.ids[self.resolutions_fields.get()]
            download_folder = self.download_dir.get()

            return {
                "format": format,
                "progress_hooks": [self.progress_hook],
                "outtmpl": os.path.join(
                    download_folder, "%(title)s-%(format)s.%(ext)s"
                ),
            }

        def download_video(self):
            # Retrieve the string from the entry fields
            youtube_url = self.video_url.get()
            download_folder = self.download_dir.get()

            # Check if the entry fields are not empty
            if youtube_url and download_folder:
                # Display progress bar
                self.progress_bar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

                # Set up options for youtube-dl
                ydl_opts = self.setup_ydl_opts()

                # Download the video
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_url])

                # Hide progress bar and show download complete message
                self.progress_bar.grid_remove()
                messagebox.showinfo(
                    title="Download Complete",
                    message="Video has been downloaded successfully.",
                )
                self.db()

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
                    str(total_hours)
                    + "h:"
                    + str(total_minutes)
                    + "m:"
                    + str(total_seconds)
                    + "s"
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
                    "INSERT INTO `user_time`(`tool_name`, `date_used`, `entry_time`, `exit_time`, `total_time`) VALUES ('YOUTUBE DOWNLOADER','{}','{}','{}','{}')".format(
                        date, entry_time, exit_time, total
                    )
                )
                db_connection.commit()

                db_cursor.execute("SELECT * FROM total WHERE tool_name = 'Youtube_Downloader'")
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
                    "UPDATE `total` SET `total_time`='{}' WHERE `tool_name`='Youtube_Downloader'".format(
                        ttttt
                    )
                )
                db_connection.commit()
                db_cursor.close()
                db_connection.close()
            else:
                # Display error message for empty fields
                messagebox.showerror("Empty Fields", "Fields are empty!")

        def browse_folder(self):
            # using the askdirectory() method of the filedialog module to select the directory
            download_path = filedialog.askdirectory(
                initialdir="D:\Downloads", title="Select the folder to save the video"
            )
            # using the set() method to set the directory path in the entry field
            self.download_dir.set(download_path)

            if self.video_url.get() == "":
                return

            download_thread = threading.Thread(target=self.set_image)
            download_thread.start()

        def browse_folder1(self):
            os.system("python key.py")

        def download_video_thread(self):
            download_thread = threading.Thread(target=self.download_video)
            download_thread.start()

        def reset(self):
            self.video_url.set("")
            self.download_dir.set("")
            self.url_field.focus_set()

        def exit(self):
            self.destroy()

        def toggle_value(self):
            global x
            if x == 0:
                customtkinter.set_appearance_mode("light")
                x = 1
            else:
                x = 0
                customtkinter.set_appearance_mode("dark")

        def __init__(self):
            super().__init__()

            # setting the title of the window
            self.title("YouTube Downloader")

            # setting the size and position of the window
            self.geometry("700x700")

            # disabling the resizable option for better UI
            self.resizable(0, 0)

            # configuring the background color of the window

            # configuring the icon of the window
            self.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\yt1.ico")

            # adding frames to the window using the Frame() widget
            header_frame = customtkinter.CTkFrame(self)
            self.image_frame = customtkinter.CTkFrame(self, height=0, width=0)
            self.entry_frame = customtkinter.CTkFrame(self)
            button_frame = customtkinter.CTkFrame(self, width=400)
            progress_frame = customtkinter.CTkFrame(self, height=0, width=0)

            # using the pack() method to set the positions of the frames
            header_frame.pack(pady=20)
            self.image_frame.pack(pady=10)
            self.entry_frame.pack(pady=10)
            button_frame.pack(pady=20)

            progress_frame.pack(padx=10)

            # ------------------------- the self.entry_frame frame -------------------------

            yt_downloader_icon = customtkinter.CTkImage(
                Image.open(
                    "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\yt1.png"
                ),
                size=(30, 30),
            )

            header_label = customtkinter.CTkLabel(
                header_frame,
                text="YouTube Video Downloader",
                anchor=customtkinter.SE,
                image=yt_downloader_icon,
                compound="left",
            )

            # using the grid() method to set the position of the labels in the grid format
            header_label.grid(row=0, column=1, padx=10, pady=10)

            # ------------------------- the self.entry_frame frame -------------------------

            # adding the labels to the self.entry_frame frame using the Label() widget
            url_label = customtkinter.CTkLabel(
                self.entry_frame, text="Video URL:", anchor=customtkinter.SE
            )
            des_label = customtkinter.CTkLabel(
                self.entry_frame, text="Destination:", anchor=customtkinter.SE
            )

            # using the grid() method to set the position of the labels in the grid format
            url_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
            des_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

            # creating the objects of the StringVar() class
            self.video_url = tk.StringVar()
            self.download_dir = tk.StringVar()

            # adding the entry fields to the self.entry_frame frame using the Entry() widget
            self.url_field = customtkinter.CTkEntry(
                self.entry_frame, textvariable=self.video_url, width=200
            )

            des_field = customtkinter.CTkEntry(
                self.entry_frame,
                textvariable=self.download_dir,
                width=200,
            )

            # using the grid() method to set the position of the entry fields in the grid format
            self.url_field.grid(
                row=0, column=1, padx=5, pady=5, columnspan=2, sticky=tk.W
            )
            des_field.grid(row=1, column=1, padx=5, pady=5)

            resolution = tk.StringVar()

            self.resolutions_fields = ttk.Combobox(
                self.entry_frame, state="readonly", width=20, font=("verdana", "8")
            )

            browse_button1 = customtkinter.CTkButton(
                self.entry_frame, text="Keyword Search", command=self.browse_folder1
            )

            # using the grid() method to set the position of the button in the grid format
            browse_button1.grid(row=0, column=2, padx=5, pady=5)

            # adding a button to the self.entry_frame frame using the Button() widget
            browse_button = customtkinter.CTkButton(
                self.entry_frame, text="Browse", command=self.browse_folder
            )

            # using the grid() method to set the position of the button in the grid format
            browse_button.grid(row=1, column=2, padx=5, pady=5)

            self.style = ttk.Style(self)
            self.style.layout(
                "text.Horizontal.TProgressbar",
                [
                    (
                        "Horizontal.Progressbar.trough",
                        {
                            "children": [
                                (
                                    "Horizontal.Progressbar.pbar",
                                    {"side": "left", "sticky": "ns"},
                                )
                            ],
                            "sticky": "nswe",
                        },
                    ),
                    ("Horizontal.Progressbar.label", {"sticky": ""}),
                ],
            )
            self.style.configure("text.Horizontal.TProgressbar", text="0 %")

            self.progress_bar = ttk.Progressbar(
                progress_frame,
                orient=tk.HORIZONTAL,
                style="text.Horizontal.TProgressbar",
                length=250,
                mode="determinate",
            )

            self.progress_bar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

            # hide the progress bar
            self.progress_bar.grid_remove()

            # db connection

            # ------------------------- the button_frame frame -------------------------

            # adding the buttons to the button_frame frame using the Button() widget
            download_button = customtkinter.CTkButton(
                button_frame,
                text="DOWNLOAD!",
                width=100,
                command=self.download_video_thread,
            )

            reset_button = customtkinter.CTkButton(
                button_frame, text="Clear", width=100, command=self.reset
            )

            close_button = customtkinter.CTkButton(
                button_frame, text="EXIT", width=100, command=self.exit
            )

            # using the grid() method to set the position of the buttons in the grid format
            download_button.grid(row=0, column=0, padx=5, pady=10)
            reset_button.grid(row=0, column=1, padx=5, pady=10)
            close_button.grid(row=0, column=2, padx=5, pady=10)

            appearence_button = customtkinter.CTkButton(
                button_frame,
                text="Appearence Toggle",
                width=100,
                command=self.toggle_value,
            )
            appearence_button.grid(row=0, column=3, padx=5, pady=10)

    if __name__ == "__main__":
        app = YoutubeDownloadWindow()
        app.mainloop()


