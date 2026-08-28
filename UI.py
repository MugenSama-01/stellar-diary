import sqlite3
import customtkinter as ctk
from PIL import Image, ImageFilter
from tkcalendar import Calendar
import backend



class main(ctk.CTk):
    def __init__(self):
        super().__init__()

        window_width = 1200
        window_height = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        img=Image.open("images/sky1.jpg").resize((1200, 800))

        self.logo = ctk.CTkLabel(self, image=ctk.CTkImage(dark_image=img, size=(1200, 800)), text="")
        self.logo.place(x=0, y=0, relwidth=1, relheight=1)

        self.l = ctk.CTkLabel(self, width=240, height=80, text="Stellar",image = ctk.CTkImage(img.crop((60, 50,  300 , 130 )),size=(240,80)),
                              font=("Forte", 70, "bold"), anchor="w", text_color="#FFFDD0")
        self.l.place(x=60, y=50)

        self.l = ctk.CTkLabel(self, width=200, height=80, text="Diary", image = ctk.CTkImage(img.crop((200, 130,  400 , 210 )),size=(200,80)),
                              font=("Forte", 70, "bold"), anchor="w", text_color="#FFFDD0")
        self.l.place(x=200, y=130)

        self.newlog = ctk.CTkButton(self, text="New log",  border_color="#00F0FF",border_width=2, fg_color="#0B0C15",text_color="#00F0FF",font=("Forte", 40, "bold"), width=350,height=60,command=self.newlogwin)
        self.newlog.place(x=800, y=330)

        self.oldlog = ctk.CTkButton(self, text="Check old logs", border_color="#00F0FF",border_width=2,fg_color="#0B0C15",text_color="#00F0FF",font=("Forte", 40, "bold"), width=350,height=60)
        self.oldlog.place(x=800, y=430)

        self.ack = ctk.CTkButton(self, text="Gratitude",  border_color="#00F0FF",border_width=2, fg_color="#0B0C15",text_color="#00F0FF",font=("Forte", 40, "bold"),  width=350,height=60)
        self.ack.place(x=800, y=530)

    def newlogwin(self):
        self.withdraw()
        self.new_log_window = new_log(self)


sky2=Image.open("images/sky2.jpg")
sky2p=sky2.resize((1400, 800)).filter(ImageFilter.GaussianBlur(radius=3))
starnames=backend.star_name()

def frame_crop_log(x, y, w, h):
    return ctk.CTkImage(dark_image=sky2p.crop((x+15, y+180, x+15+w,y+180+ h)),size=(w,h))

def frame2_crop_log(x, y, w, h):
    return ctk.CTkImage(dark_image=sky2p.crop((x+1070, y+120, x+1070+w,y+120+ h)),size=(w,h))

class new_log(ctk.CTkToplevel):
    def __init__(self,parent):
        super().__init__(parent)

        window_width = 1400
        window_height = 800
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        lat,lon,tz=backend.location()

        im = ctk.CTkImage(dark_image=sky2, size=(1400, 800))

        self.logo = ctk.CTkLabel(self, image=im, text="")
        self.logo.place(x=0, y=0, relwidth=1, relheight=1)

        self.cal = Calendar(self, selectmode="day", date_pattern="dd-mm-yyyy", year=2026, month=1, day=1)
        self.cal.place(x=15, y=20)
        self.cal.bind("<<CalendarSelected>>")

        self.frame = ctk.CTkFrame(self, border_color="#00F0FF", border_width=5, height=560, width=520,)
        self.frame.place(x=15, y=180)

        self.logo = ctk.CTkLabel(self.frame, image=frame_crop_log(0, 0, 520, 560), text="")
        self.logo.place(x=5.5, y=5.5, relwidth=0.978, relheight=0.983)

        self.time_from = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 10, 160, 30),text="Time(From)                  :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.time_from.place(x=10, y=10)
        self.time_from_inputx = ctk.CTkEntry(self.frame, width=300, height=30, placeholder_text="Ex-20:30")
        self.time_from_inputx.place(x=200, y=10)

        self.time_to = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 60, 160, 30),text="Time(To)                     :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.time_to.place(x=10, y=60)
        self.time_to_inputx = ctk.CTkEntry(self.frame, width=300, height=30, placeholder_text="Ex-20:30")
        self.time_to_inputx.place(x=200, y=60)

        self.lp = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 110, 160, 30),text="Appx. Light Pollution :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.lp.place(x=10, y=110)
        self.lp_inputcb = ctk.CTkComboBox(self.frame, values=["0","1","2","3","4","5","6","7","8","9"], width=300)
        self.lp_inputcb.place(x=200, y=110)
        self.lp_inputcb.set("Select Bortle Level")

        self.weather = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 160, 160, 30),text="Weather                       :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.weather.place(x=10, y=160)
        self.weather_inputcb = ctk.CTkComboBox(self.frame, values=["Clear","Hazy","Cloudy"], width=300)
        self.weather_inputcb.place(x=200, y=160)
        self.weather_inputcb.set("Select Weather Condition")

        self.star_name = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 210, 160, 30),text="Star Name                   :", font=("Segoe UI", 15,"bold"), anchor="w", text_color="#F0F4F8")
        self.star_name.place(x=10, y=210)
        self.star_name_inputcb = ctk.CTkComboBox(self.frame, values=starnames, width=300,command=self.auto_hip)
        self.star_name_inputcb.place(x=200, y=210)
        self.star_name_inputcb.set("Enter Star Name")

        self.hip_id = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 260, 160, 30),text="HIP ID                         :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.hip_id.place(x=10, y=260)
        self.hip_id_inputx = ctk.CTkEntry(self.frame, width=300, height=30, placeholder_text="Enter HIP ID")
        self.hip_id_inputx.place(x=200, y=260)

        self.direction = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 310, 160, 30),text="Direction                   :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.direction.place(x=10, y=310)
        self.direction_inputcd = ctk.CTkComboBox(self.frame, values=["N", "NE", "E", "SE","S","SW","W","NW","Zenith"], width=300)
        self.direction_inputcd.place(x=200, y=310)
        self.direction_inputcd.set("Select Direction")

        self.brightness = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(10, 360, 160, 30),text="Brightness                  :", font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F0F4F8")
        self.brightness.place(x=10, y=360)
        self.brightness_inputcb = ctk.CTkComboBox(self.frame, values=["High", "Medium", "low", "Faint"], width=300)
        self.brightness_inputcb.place(x=200, y=360)
        self.brightness_inputcb.set("Select Brightness")

        self.add = ctk.CTkButton(self.frame, text="Add", border_color="black", fg_color="blue", width=120,command=self.add)
        self.add.place(x=100, y=430)

        self.save = ctk.CTkButton(self.frame, text="Save", border_color="black", fg_color="blue", width=120)
        self.save.place(x=300, y=430)

        self.moto = ctk.CTkLabel(self.frame, width=160, height=30, image=frame_crop_log(150, 500, 160, 30),text="Keep Looking Up!!!", font=("Segoe UI", 18, "bold"), anchor="w", text_color="#F0F4F8")
        self.moto.place(x=180, y=500)

        self.textbox = ctk.CTkTextbox(self, width=300, height=100, border_color="#00F0FF", border_width=5)
        self.textbox.place(x=1070, y=15)
        self.textbox.insert("end", "Added Stars\n")
        self.textbox.configure(state="disabled")

        self.frame2 = ctk.CTkFrame(self, border_color="#00F0FF", border_width=5, height=150, width=300, )
        self.frame2.place(x=1070, y=120)

        self.logo2 = ctk.CTkLabel(self.frame2, image=frame2_crop_log(0, 0, 300, 150), text="")
        self.logo2.place(x=5.5, y=5.5, relwidth=0.965, relheight=0.91)

        self.latitude = ctk.CTkLabel(self.frame2, width=75, height=30,text="Latitude:",image=frame2_crop_log(10, 10, 75, 30), font=("Segoe UI", 15, "bold"), anchor="w",text_color="#F0F4F8")
        self.latitude.place(x=10, y=10)
        self.latitudex = ctk.CTkEntry(self.frame2, width=130, height=30)
        self.latitudex.place(x=150, y=10)
        self.latitudex.insert(0,str(lat))

        self.longitude = ctk.CTkLabel(self.frame2, width=80, height=30, text="Longitude:",image=frame2_crop_log(10, 60, 80, 30), font=("Segoe UI", 15, "bold"), anchor="w",text_color="#F0F4F8")
        self.longitude.place(x=10, y=60)
        self.longitudex = ctk.CTkEntry(self.frame2, width=130, height=30)
        self.longitudex.place(x=150, y=60)
        self.longitudex.insert(0,str(lon))

        self.time_zone = ctk.CTkLabel(self.frame2, width=75, height=30,text="Time Zone",image=frame2_crop_log(10, 110, 75, 30), font=("Segoe UI", 15, "bold"), anchor="w",text_color="#F0F4F8")
        self.time_zone.place(x=10, y=110)
        self.time_zonex = ctk.CTkEntry(self.frame2, width=130, height=30)
        self.time_zonex.place(x=150, y=110)
        self.time_zonex.insert(0,tz)

        self.msgbox=ctk.CTkLabel(self,font=("Segoe UI", 15, "bold"),text_color="red",text="")
        self.msgbox.place(x=1070,y=750)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def add(self):
        timefrom=self.time_from_inputx.get()
        timeto=self.time_to_inputx.get()
        if timefrom == "" or timeto=="":
            self.msg_send("Invalid Time")
            return

        lp = self.lp_inputcb.get()
        if lp == "Select Bortle Level":
            self.msg_send("Invalid Bortle")
            return
        if not (0 <= int(lp) <= 9):
            self.msg_send("Invalid Bortle")
            return

        weather=self.weather_inputcb.get()
        if weather not in ["Clear","Hazy","Cloudy"] :
            self.msg_send("Invalid Weather")
            return

        starname=self.star_name_inputcb.get()
        if starname not in starnames and starname!="" :
            self.msg_send("Invalid Star Name")
            return

        hip = self.hip_id_inputx.get()
        if hip == "":
            self.msg_send("Invalid HIP")
            return

        try:
            hip=int(hip)
        except:
            self.msg_send("Invalid HIP")
            return

        if backend.sname(hip)!= starname:
            self.msg_send("Invalid HIP")
            return

        direction = self.direction_inputcd.get()
        if direction not in ["N", "NE", "E", "SE","S","SW","W","NW","Zenith"]:
            self.msg_send("Invalid Direction")
            return

        brightness=self.brightness_inputcb.get()
        if brightness not in ["High", "Medium", "low", "Faint"]:
            self.msg_send("Invalid Brightness")
            return

        try:
            lat=float(self.latitudex.get())
            lon=float(self.longitudex.get())
        except:
            self.msg_send("Invalid Coordinates")
            return

        if not(-90 <= lat <= 90 and -180 <= lon <= 180):
            self.msg_send("Invalid Coordinates")
            return

        if backend.add(hip, self.cal.get_date(), self.time_from_inputx.get(),
                        self.time_to_inputx.get(), float(self.latitudex.get()),
                        float(self.longitudex.get()), self.lp_inputcb.get(),
                        self.weather_inputcb.get(), self.direction_inputcd.get(),
                        self.brightness_inputcb.get(),self.time_zonex.get()):
            self.textbox.configure(state="normal")
            self.textbox.insert("end", f"{hip} ({starname})\n")
            self.textbox.configure(state="disabled")
        else:
            self.msg_send("Data already enlisted")

    def msg_send(self,msg):
        self.msgbox.configure(text=msg)

    def auto_hip(self,selected_star):
        self.hip_id_inputx.delete(0, "end")
        self.hip_id_inputx.insert(0,backend.find_hip(selected_star))

    def on_close(self):
        self.destroy()
        self.master.destroy()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app=main()
app.mainloop()