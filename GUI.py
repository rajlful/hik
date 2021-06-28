from tkinter import *

from hikisapi import Hikvision
from hikdb import Hikdb

class MainWindow(Tk):
    
    def __init__(self):
        super().__init__()
        self.main_window = Tk()
        self.main_window.title("HIKVISION VMS")
        self.main_window.geometry('1100x700')

        self.cameras_list = Listbox(self.main_window, width=23, height=20)
        self.cameras_list.place(x=2, y=30)
        self.cameras_list_label = Label(self.main_window, text='List of cameras', bg='white', font="Arial 8")
        self.cameras_list_label.place(x=5, y=35)
        self.scrollbar = Scrollbar(self.main_window)
        self.scrollbar.config(command=self.cameras_list.yview)

        self.journal_events = Listbox(self.main_window, width=23, height=18)
        self.journal_events.place(x=2, y=385)
        self.scrollbar = Scrollbar(self.main_window)
        self.scrollbar.config(command=self.journal_events.yview)

        self.add_device_btn = Button(self.main_window, text="Add device", command=self.add_device_window)
        self.add_device_btn.place(x=0, y=1)

        self.del_device_btn = Button(self.main_window, text="Delete device", command=self.remove_device)
        self.del_device_btn.place(x=75, y=1)

        self.events_btn = Button(self.main_window, width=20, height=1, text="Show events", command=self.add_motion_events)
        self.events_btn.place(x=7, y=357)

        self.motion_detector_btn = Button(self.main_window, text="Motion detector", command=self.md_setting)
        self.motion_detector_btn.place(x=175, y=457)

        self.player = Frame(self.main_window, bg='black',width=650, height=450)
        self.player.place(x=175, y=5)
        self.player_label = Label(self.main_window, text="Player will be there...", fg='red', font="Arial 23", bg='black')
        self.player_label.place(x=350, y=250)
        
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


a = MainWindow()
a.mainloop()