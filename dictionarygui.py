from tkinter import *
from tkinter import filedialog
from PyMultiDictionary import MultiDictionary
from fpdf import FPDF
import customtkinter
import time
import datetime
import mysql.connector

if "__main__" == __name__:
    print("Window created at:", time.strftime("%H:%M:%S"))
    entry_time = time.strftime("%H:%M:%S")

    dictionary = MultiDictionary()
    root = customtkinter.CTk()
    root.title("Word Dictionary GUI")
    root.geometry("600x1000")
    root.iconbitmap("C:\\Users\\91998\\Desktop\\college_assignments\\CLEAN_MAJOR_PROJECT_FINAL\\CLEAN_MAJOR_PROJECT\\assets\\Dictionary.ico")

    x = 0

    def toggle_value():
        global x
        if x == 0:
            customtkinter.set_appearance_mode("light")
            x = 1
        else:
            x = 0
            customtkinter.set_appearance_mode("dark")

    def dict():
        meaning_text = dictionary.meaning("en", word.get())[1]
        synonym_list = dictionary.synonym("en", word.get())
        antonym_list = dictionary.antonym("en", word.get())

        meaning.delete("1.0", "end")
        meaning.insert("end", meaning_text)

        # Adding commas between synonyms and a full stop at the end
        synonym_text = ", ".join(synonym_list) + "." if synonym_list else "No synonyms found."
        synonym.delete("1.0", "end")
        synonym.insert("end", synonym_text)

        antonym_text = ", ".join(antonym_list) + "." if antonym_list else "No synonyms found."
        antonym.delete("1.0", "end")
        antonym.insert("end", antonym_text)

        db_connection = mysql.connector.connect(
            host="db4free.net",
            user="teamtoolhub",
            password="t00lhub123",
            database="toolhub",
        )
        # Create a cursor object to execute SQL queries
        db_cursor = db_connection.cursor()

        db_cursor.execute("SELECT * FROM report WHERE tool_id = 'dict1'")

        result = db_cursor.fetchone()

        if result:
            tool_usage = result[2]  # Access the tool_usage column
            print("dictionary :", tool_usage)

            # UPDATING
            tool_usage = tool_usage + 1
            print(tool_usage)
            x = 3

            db_cursor.execute(
                "UPDATE `report` SET `tool_usage`= tool_usage+1 WHERE tool_id='dict1'"
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

            # ... (unchanged code)

        db_connection.commit()

        db_cursor.close()
        db_connection.close()

    def clear_data():
        word.delete(0, "end")
        meaning.delete("1.0", "end")
        synonym.delete("1.0", "end")
        antonym.delete("1.0", "end")

    def export_pdf():
        destination = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
        )
        if destination:
            pdf = FPDF(format="A4")
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            keyword = word.get()
            meaning_text = meaning.get("1.0", "end-1c")
            synonym_text = synonym.get("1.0", "end-1c")
            antonym_text = antonym.get("1.0", "end-1c")

            pdf.cell(200, 10, txt="Word: " + keyword, ln=True)
            pdf.multi_cell(200, 10, txt="Meaning: " + meaning_text, align="L")
            pdf.multi_cell(200, 10, txt="Synonym: " + synonym_text, align="L")
            pdf.multi_cell(200, 10, txt="Antonym: " + antonym_text, align="L")
            pdf.output(destination)

    title = customtkinter.CTkLabel(
        root,
        text="Word Dictionary",
        font=customtkinter.CTkFont(family="Roboto", size=26, weight="bold"),
    )
    title.pack(pady=10,padx=10)

    frame = customtkinter.CTkFrame(root)
    label1 = customtkinter.CTkLabel(
        frame,
        text="Type Word:",
        font=customtkinter.CTkFont(family="Belanosima", size=18, weight="bold"),
    ).pack(
        side=LEFT,
    )
    word = customtkinter.CTkEntry(frame, font=customtkinter.CTkFont(family="Arial"))
    word.pack(
        ipadx=90,
    )
    frame.pack()

    frame1 = customtkinter.CTkFrame(root)
    meaning1 = customtkinter.CTkLabel(
        frame1,
        text="Meaning: ",
        font=customtkinter.CTkFont(family="Belanosima", size=18, weight="bold"),
    ).pack(side=LEFT)
    meaning = customtkinter.CTkTextbox(
        frame1,
        font=customtkinter.CTkFont(family="Arial"),
        wrap="word",
        width=300,
        height=150,
        border_width=3,
    )
    meaning.pack()
    frame1.pack(pady=15)

    frame2 = customtkinter.CTkFrame(root)
    Synonm1 = customtkinter.CTkLabel(
        frame2,
        text="Synonym: ",
        font=customtkinter.CTkFont("Belanosima", size=18, weight="bold"),
    ).pack(side=LEFT)

    synonym = customtkinter.CTkTextbox(
        frame2,
        font=customtkinter.CTkFont(family="Belanosima", size=18),
        wrap="word",
        width=300,
        height=150,
        border_width=3,
    )
    synonym.pack()
    frame2.pack(pady=15)

    frame3 = customtkinter.CTkFrame(root)
    antonym1 = customtkinter.CTkLabel(
        frame3,
        text="Antonym: ",
        font=customtkinter.CTkFont(family="Belanosima", size=18, weight="bold"),
    ).pack(side=LEFT)
    antonym = customtkinter.CTkTextbox(
        frame3,
        font=customtkinter.CTkFont(family="Belanosima", size=18),
        wrap="word",
        width=300,
        height=150,
        border_width=3,
    )
    antonym.pack(side=LEFT)
    frame3.pack(pady=15)

    frame4 = customtkinter.CTkFrame(
        root,
    )
    frame4.pack()

    submit1 = customtkinter.CTkButton(
        frame4, text="Submit", font=customtkinter.CTkFont(family="Arial"), command=dict
    ).pack(side=LEFT, padx=10, pady=10)

    frame5 = customtkinter.CTkFrame(
        root,
    )
    frame5.pack()

    clear1 = customtkinter.CTkButton(
        frame5,
        text="Clear",
        font=customtkinter.CTkFont(family="Arial"),
        command=clear_data,
    ).pack(side=LEFT, padx=10, pady=10)

    exportpdf = customtkinter.CTkButton(
        frame5,
        text="Export PDF",
        font=customtkinter.CTkFont(family="Arial"),
        command=export_pdf,
    ).pack(side=LEFT, padx=10, pady=10)

    exit = customtkinter.CTkButton(
        frame5, text="Exit", font=customtkinter.CTkFont("Arial"), command=root.quit
    ).pack(side=LEFT, padx=10, pady=10)

    appearence_button = customtkinter.CTkButton(
        frame4, text="Appearence Toggle", command=toggle_value
    )
    appearence_button.pack(side="left", padx=10, pady=10)

    root.mainloop()


