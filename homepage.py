# importing required modules
import tkinter
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import customtkinter
import os
from PIL import Image, ImageTk
from customtkinter import CTkTabview
import dictionarygui
import emailtry
import image_converter
import texttospeech
import video_compressor
import wiki_new
import youtube





# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("TOOLHUB")
        self.geometry(f"{1100}x{580}")
        self.resizable(True, True)
        self.iconbitmap(
            r"C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\icon.ico"
        )

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # side frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # tabview
        self.tabview = customtkinter.CTkTabview(self, width=800, height=800)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="news")

        # tabview category
        self.tabview.add("Media Downloader")
        self.tabview.add("Media Converter")
        self.tabview.add("Email Section")
        self.tabview.add("Find Section")
        self.tabview.add("About ToolHub")

        # tabview configure
        self.tabview.tab("Media Downloader").grid_columnconfigure(
            0,
            weight=1,
        )  # configure grid of individual tabs
        self.tabview.tab("Media Converter").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Email Section").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Find Section").grid_columnconfigure(0, weight=1)
        self.tabview.tab("About ToolHub").grid_columnconfigure(0, weight=1)

        self.about_text = customtkinter.CTkLabel(
           self.tabview.tab("About ToolHub"),
            text="INSTRUCTIONS:\n ",
            font=customtkinter.CTkFont(family="Kanit", size=25),
        )
        self.about_text.pack()


        self.about_text2 = customtkinter.CTkLabel(
            self.tabview.tab("About ToolHub"),
            text="ToolHub is an all-in-one software solution that provides you with a comprehensive set of seven powerful tools to simplify \n various tasks. With ToolHub, you can conveniently access a range of functionalities,\n including: \n\n 1. YouTube Downloader \n 2. Wikipedia Summary \n 3. Bulk Mail Sender \n 4. Text to Speech \n 5. Dictionary \n 6. Video Compressor \n 7. Image Converter \n\n With ToolHub's diverse range of tools, you can streamline your tasks, enhance productivity, \n and save time by having multiple functionalities conveniently accessible within a single software solution.",
            font=customtkinter.CTkFont(family="Kanit", size=16),
            justify="left",
        )

        self.about_text2.pack(padx=10)


        # adding image to buttons
        yt_downloader_icon = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\yt1.png"
            ),
            size=(50, 50),
        )

        wikipedia = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\wiki.png"
            ),
            size=(50, 50),
        )

        image_converter_icon = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\imageconvert.ico"
            ),
            size=(50, 50),
        )

        texttospeech_icon = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\texttospeech.png"
            ),
            size=(50, 50),
        )

        bulkemail_icon = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\email.png"
            ),
            size=(50, 50),
        )

        dictionary_icon = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\Dictionary.png"
            ),
            size=(50, 50),
        )

        videcompress_icon = customtkinter.CTkImage(
            Image.open(
                "C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\compressor.png"
            ),
            size=(50, 50),
        )

        def helloCallBack():
            os.system("python youtube.py")

        # adding button widgets for media downloader
        self.string_input_button1 = customtkinter.CTkButton(
            self.tabview.tab("Media Downloader"),
            text="YouTube Downloader",
            font=customtkinter.CTkFont(family="Roboto", size=22),
            width=400,
            height=150,
            image=yt_downloader_icon,
            hover_color="#C77C78",
            command=helloCallBack,
        )

        self.string_input_button1.grid(row=2, column=0, padx=20, pady=(10, 10))

        def helloCallBack1():
            os.system("python image_converter.py")

        # adding button widgets for media converter
        self.string_input_button2 = customtkinter.CTkButton(
            self.tabview.tab("Media Converter"),
            text="Image Converter",
            width=400,
            height=150,
            font=customtkinter.CTkFont(family="Roboto", size=22),
            image=image_converter_icon,
            hover_color="#C77C78",
            command=helloCallBack1,
        )

        self.string_input_button2.grid(row=2, column=0, padx=20, pady=(10, 10))

        # calling texttospeech
        def helloCallBack2():
            os.system("python texttospeech.py")

        # media converter button 2 text ot speech
        self.string_input_button3 = customtkinter.CTkButton(
            self.tabview.tab("Media Converter"),
            text="Text-to-Speech",
            width=400,
            height=150,
            font=customtkinter.CTkFont(family="Roboto", size=22),
            image=texttospeech_icon,
            hover_color="#C77C78",
            command=helloCallBack2,
        )

        self.string_input_button3.grid(row=3, column=0, padx=20, pady=(10, 10))

        def helloCallBack3():
            os.system("python video_compressor.py")

        # media converter button 3 video compressor
        self.string_input_button3 = customtkinter.CTkButton(
            self.tabview.tab("Media Converter"),
            text="Video Compressor",
            width=400,
            height=150,
            font=customtkinter.CTkFont(family="Roboto", size=22),
            image=videcompress_icon,
            hover_color="#C77C78",
            command=helloCallBack3,
        )

        self.string_input_button3.grid(row=4, column=0, padx=20, pady=(10, 10))

        def helloCallBack4():
            os.system("python emailtry.py")

        # email section button1 bulk email
        self.string_input_button4 = customtkinter.CTkButton(
            self.tabview.tab("Email Section"),
            text="Bulk Email Sender",
            width=400,
            height=150,
            font=customtkinter.CTkFont(family="Roboto", size=22),
            image=bulkemail_icon,
            command=helloCallBack4,
        )

        self.string_input_button4.grid(row=1, column=0, padx=20, pady=(10, 10))

        def helloCallBack7():
            os.system("python dictionarygui.py")

        # find section button1 bulk email
        self.string_input_button5 = customtkinter.CTkButton(
            self.tabview.tab("Find Section"),
            text="Dictionary GUI",
            width=400,
            height=150,
            font=customtkinter.CTkFont(family="Roboto", size=22),
            image=dictionary_icon,
            command=helloCallBack7,
        )

        self.string_input_button5.grid(row=1, column=0, padx=20, pady=(10, 10))

        def helloCallBack6():
            os.system("python wiki_new.py")

        self.string_input_button6 = customtkinter.CTkButton(
            self.tabview.tab("Find Section"),
            text="Wikipedia Summary",
            width=400,
            height=150,
            font=customtkinter.CTkFont(family="Roboto", size=22),
            image=wikipedia,
            command=helloCallBack6,
        )

        self.string_input_button6.grid(row=2, column=0, padx=20, pady=(10, 10))

        # text of toolhub

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="ToolHub",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # logo for the toolhub on screen

        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w"
        )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))


        self.admin_button=customtkinter.CTkButton(
            self.sidebar_frame, text="ADMIN LOGIN", command=self.admin_log,
        )

       
        self.admin_button.grid(row=5, column=0, padx=20, pady=10)



        self.quit_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Quit app", command=self.quit_app, fg_color="Red"
        )
        self.quit_button.bind("<Escape>", self.quit_app)
        self.quit_button.grid(row=14, column=0, padx=20, pady=10)



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def helloCallBack():
        os.system("python youtube.py")

    def quit_app(self):
        self.destroy()

    def admin_log(self):
        os.system("python admin.py")


if __name__ == "__main__":
    app = App()
    app.mainloop()
