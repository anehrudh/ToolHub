import tkinter as tk
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO
from youtube_search import YoutubeSearch
import requests
import pyperclip
import customtkinter
import youtube

if '__main__' == __name__:
    root = customtkinter.CTk()
    root.title("Youtube Search")
    root.geometry("600x600")
    root.resizable(0, 0)
    root.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\yt1.ico")

    button_frame = customtkinter.CTkFrame(root, width=250)
    button_frame.pack()

    # CREATE MAINFRAME
    main_frame = customtkinter.CTkFrame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    # CREATE CANVAS
    my_canvas = customtkinter.CTkCanvas(main_frame, highlightthickness=0)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # MYSCROLLBAR
    my_scrollbar = customtkinter.CTkScrollbar(
        main_frame, orientation=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # configure
    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(
        scrollregion=my_canvas.bbox("all")))
    my_canvas.configure(bg='#2D2D30')

    # ANOTHER FRAME
    second_frame = customtkinter.CTkFrame(
        my_canvas, width=800, height=570)

    # ADD THAT FRAME TO A WINDOW
    my_canvas.create_window((0, 0), window=second_frame, anchor='center')

    def callback():
        keyword = keywordentry.get()
        results = YoutubeSearch(keyword, max_results=10).to_dict()

        root.geometry("600x610")

        for i in range(0, 10):
            img_url = results[i]['thumbnails'][0]
            response = requests.get(img_url)
            img_data = response.content
            photo = Image.open(BytesIO(img_data))
            photo = photo.resize((200, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(photo)

            label = tk.Label(second_frame, image=photo)
            label.image = photo
            label.pack(pady=(30, 0), anchor=tk.CENTER)  # Center align label

            ent1 = customtkinter.CTkLabel(
                second_frame, text=results[i]['title'])
            ent1.pack(anchor=tk.CENTER)  # Center align label

            ent = customtkinter.CTkLabel(
                second_frame, text='youtube.com' + results[i]['url_suffix'])
            ent.pack(anchor=tk.CENTER)  # Center align label

            b = customtkinter.CTkButton(second_frame, text='COPY', command=lambda m='youtube.com' +
                                        results[i]['url_suffix']: copy_select(m))
            b.pack(anchor=tk.CENTER)  # Center align button

    def copy_select(m):  # copy selected text to clipboard
        global data
        data = m
        pyperclip.copy(data)
        youtube.hello(data)

    def scroll(event):
        my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # Bind scroll event to the scrollbar
    my_canvas.bind_all("<MouseWheel>", scroll)

    user_password = customtkinter.CTkLabel(button_frame,
                                           text="ANY KEYWORD").pack(side=tk.LEFT, padx=20)

    keywordentry = customtkinter.CTkEntry(button_frame, width=150)
    keywordentry.pack(side=tk.LEFT)
    submit_button = customtkinter.CTkButton(
        button_frame, text="Submit", command=callback)
    submit_button.pack(side=tk.LEFT)

    root.mainloop()
