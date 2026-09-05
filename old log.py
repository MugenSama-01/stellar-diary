import sqlite3
import tkinter
import customtkinter as ctk
from PIL import Image, ImageFilter
from tkcalendar import Calendar
import datetime

import backend

sky3=Image.open("images/sky3.jpg")
sky3p=sky3.resize((1400, 800)).filter(ImageFilter.GaussianBlur(radius=3))

def frame_crop_log(x, y, w, h):
    return ctk.CTkImage(dark_image=sky3p.crop((x+15, y+180, x+15+w,y+180+ h)),size=(w,h))

class main(ctk.CTk):
    def __init__(self):
        super().__init__()

        window_width = 1400
        window_height = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        im = ctk.CTkImage(dark_image=sky3, size=(1400, 800))

        self.logo = ctk.CTkLabel(self, image=im, text="")
        self.logo.place(x=0, y=0, relwidth=1, relheight=1)

        self.logs_frame= ctk.CTkScrollableFrame(self, width=1000, height=760,corner_radius=10)
        self.logs_frame.place(x=10, y=10)

        header_frame = ctk.CTkFrame(self.logs_frame, corner_radius=0, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        headers = ["HIP ID", "Star Name", "Date", "Time", "Latitude", "Longitude", "Light Pollution", "Weather","Brightness"]

        for i, col_name in enumerate(headers):
            header_frame.columnconfigure(i, weight=1,uniform="a")  # This ensures equal spacing
            lbl = ctk.CTkLabel(header_frame, text=col_name, font=("Arial", 14, "bold"))
            lbl.grid(row=0, column=i, sticky="ew", padx=5, pady=5)

        logs=backend.get_it_ALL()
        self.show_data(logs)

        self.cal = Calendar(self, selectmode="day",
                    date_pattern="dd-mm-yyyy",
                    year=2026, month=1, day=1,
                    # --- Dark Mode Styling ---
                    background="gray15",
                    foreground="white",
                    headersbackground="gray15",
                    headersforeground="white",
                    normalbackground="gray20",
                    normalforeground="white",
                    weekendbackground="gray20",
                    weekendforeground="white",
                    bordercolor="gray10")
        self.cal.place(x=1400, y=40)
        self.cal.bind("<<CalendarSelected>>", self.date_clicked)
        self.cal.tag_config(tag="back",background="cyan", foreground="Black")
        for i in logs:
            self.cal.calevent_create(datetime.datetime.strptime(i[3], "%d-%m-%Y").date(),text="log",tags="back")

        self.radio_var = tkinter.IntVar(value=0)
        self.date_filter_state = ctk.CTkCheckBox(self, text="Use date to filter", variable=self.radio_var, onvalue=1, offvalue=0, fg_color="dark blue")
        self.date_filter_state.place(x=1150,y=200)

        self.hiplable= ctk.CTkLabel(self, text="  H  I  P  :  ")
        self.hiplable.place(x=1070, y=250)

        self.hipin = ctk.CTkEntry(self,width=200, height=30, placeholder_text="Enter HIP ID")
        self.hipin.place(x=1150, y=250)

        self.filter= ctk.CTkButton(self, text="Filter",command=self.filter)
        self.filter.place(x=1150, y=320)

        self.reset = ctk.CTkButton(self, text="Reset", command=self.reset)
        self.reset.place(x=1150, y=370)

        self.back=ctk.CTkButton(self, text="Go Back", command=self.back)
        self.back.place(x=1150, y=700)

    def show_data(self,logs):
        for row_index, log in enumerate(logs):
            row_frame = ctk.CTkFrame(self.logs_frame, fg_color="gray15", corner_radius=5)
            row_frame.pack(fill="x", pady=2)
            col_index = 0
            for check_me, value in enumerate(log):
                if check_me ==0 or check_me == 5 or check_me == 10 or check_me == 11 or check_me == 14 or check_me == 12:
                    continue
                row_frame.columnconfigure(col_index, weight=1,uniform="a")
                val_lbl = ctk.CTkLabel(row_frame, text=str(value))
                val_lbl.grid(row=0, column=col_index, sticky="ew", padx=5, pady=5)
                col_index+=1

    def date_clicked(self, event):
            print("User clicked:", self.cal.get_date())

    def clear_rows(self):
        all_widgets = self.logs_frame.winfo_children()

        for widget in all_widgets[1:]:
            widget.destroy()

    def filter(self):
        self.clear_rows()
        if self.radio_var.get()==0:
            date ="--"
        else:
            date = self.cal.get_date()
        hip=self.hipin.get()
        if hip=="":
            hip="--"
        logs= backend.filter(date,hip)
        self.show_data(logs)

    def reset(self):
        self.clear_rows()
        self.show_data(backend.get_it_ALL())

    def back(self):
        pass



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app=main()
app.mainloop()
