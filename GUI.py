from tkinter import *
from PIL import ImageTk, Image
import cv2

from hikisapi import Hikvision
from hikdb import Hikdb

class MainWindow(Tk):
    
    def __init__(self):
        super().__init__()
        self.title("HIKVISION VMS")
        self.geometry('1100x700')

        self.cameras_list = Listbox(self, width=23, height=20)
        self.cameras_list.place(x=2, y=30)
        self.cameras_list_label = Label(self, text='List of cameras', bg='white', font="Arial 8")
        self.cameras_list_label.place(x=5, y=35)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.cameras_list.yview)

        self.journal_events = Listbox(self, width=23, height=18)
        self.journal_events.place(x=2, y=385)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.journal_events.yview)

        self.add_device_btn = Button(self, text="Add device", command=self.add_device_window)
        self.add_device_btn.place(x=0, y=1)

        self.del_device_btn = Button(self, text="Delete device", command=self.remove_device)
        self.del_device_btn.place(x=75, y=1)

        self.events_btn = Button(self, width=20, height=1, text="Show events", command=self.add_motion_events)
        self.events_btn.place(x=7, y=357)

        self.motion_detector_btn = Button(self, text="Motion detector", command=self.md_setting)
        self.motion_detector_btn.place(x=175, y=457)

        self.cap = cv2.VideoCapture("rtsp://admin:Admin1337@172.16.13.93:554/h264/ch01/sub/av_stream")
        self.player = Canvas(self, width=650, height=450)
        self.player.place(x=175, y=5)
        self.update_image()

    def add_device_window(self):
        
        self.remove_label()
        self.device_window = Tk()
        self.device_window.title("Device add")
        self.device_window.geometry('260x180')

        self.ip = Entry(self.device_window,width=15)  
        self.ip.place(x=80, y=40)
        self.ip_lbl = Label(self.device_window, text="IP adress:")
        self.ip_lbl.place(x=13, y=38)

        self.port = Entry(self.device_window,width=3)  
        self.port.place(x=80, y=65)
        self.port_lbl = Label(self.device_window, text="Port:")
        self.port_lbl.place(x=13, y=63)

        self.user =  Entry(self.device_window,width=10)  
        self.user.place(x=80, y=90)
        self.user_lbl = Label(self.device_window, text="User:")
        self.user_lbl.place(x=13, y=88)

        self.password = Entry(self.device_window,width=10)  
        self.password.place(x=80, y=115)
        self.password_lbl = Label(self.device_window, text="Password:")
        self.password_lbl.place(x=13, y=113)

        self.add_btn = Button(self.device_window, text="Add device", command=self.add_device_to_list)
        self.add_btn.place(x=80, y=140)

        self.cancel_btn = Button(self.device_window, text="Cancel", command=self.device_window.destroy)
        self.cancel_btn.place(x=160, y=140)
    
    def add_device_to_list(self):
        model_name = Hikvision(self.ip.get(), self.user.get(), self.password.get(), self.port.get())
        self.cameras_list.insert(0, model_name.get_model_name())

    def remove_device(self):
        self.cameras_list.delete(0)
    
    def remove_label(self):
        self.cameras_list_label.configure(text="")

    def add_motion_events(self):
        events = Hikdb('hik.db')
        self.journal_events.insert(0, *events.show_events())

    def md_setting(self):
        self.md_window = Tk()
        self.md_window.title("Motion detector")
        self.md_window.geometry('260x180')
        self.enable_md_checkbutton = Checkbutton(text="Enable detector")
        self.enable_md_checkbutton.pack(anchor=CENTER)
        self.sensivity_scale = Scale(self.md_window, orient=HORIZONTAL)
        self.sensivity_scale.place(x=70, y=20)


    def update_image(self):
       
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image = cv2.resize(self.image, (650,450)) # resize for my canvas
        self.image = Image.fromarray(self.image) # to PIL format
        self.image = ImageTk.PhotoImage(self.image, master=self) # to ImageTk format
        # Update image
        self.player.create_image(0, 0, anchor=NW, image=self.image)
        self.after(20, self.update_image)  # 20 - interval in ms to get the latest frame
       
       


a = MainWindow()
a.mainloop()