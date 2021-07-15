from tkinter import *
from PIL import ImageTk, Image
import cv2

from hikisapi import Hikvision
from hikdb import Hikdb
import const

class MainWindow(Tk):
    
    def __init__(self):
        super().__init__()
        self.title("HIKVISION VMS")
        self.geometry('1020x700')
        self.resizable(False, False)
        icon = PhotoImage(file='hik.png')
        self.iconphoto(False, icon)
        self.job = None

        self.cameras_list = Listbox(self, width=23, height=20)
        self.cameras_list.place(x=2, y=30)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.cameras_list.yview)
        self.cameras_list.bind("<<ListboxSelect>>", self.callback_on_selection)

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

        self.reboot_btn = Button(self, text="Reboot device")
        self.reboot_btn.place(x=830, y=1)

        self.restore_btn = Button(self, text="Restore device")
        self.restore_btn.place(x=925, y=1, height=26, width=92)

        self.brightness = Scale(self, orient=HORIZONTAL)
        self.brightness.set(50)
        self.brightness.place(x=905, y=30)
        self.brightness_lbl = Label(self, text='Brightness:')
        self.brightness_lbl.place(x=827, y=48)

        self.contrast = Scale(self, orient=HORIZONTAL)
        self.contrast.place(x=905, y=67)
        self.contrast.set(50)
        self.contrast_lbl = Label(self, text='Contrast:')
        self.contrast_lbl.place(x=827, y=86)

        self.saturation = Scale(self, orient=HORIZONTAL)
        self.saturation.place(x=905, y=104)
        self.saturation.set(50)
        self.saturation_lbl = Label(self, text='Saturation:')
        self.saturation_lbl.place(x=827, y=125)

        self.image_default_btn = Button(self, text="Default settings", command=self.image_to_default)
        self.image_default_btn.place(x=916, y=150, height=21, width=92)
        

      #  self.cap = cv2.VideoCapture(f"rtsp://admin:Admin1337@172.16.13.184:554/h264/ch01/sub/av_stream")
        self.player = Canvas(self, width=650, height=450, bg='black')
        self.player.place(x=175, y=5)

        self.frame_for_chkbtn = Frame(self, width=50, height=50)
        self.frame_for_chkbtn.place(x=737, y=460)
        self.ishd = IntVar()
        self.hd_check_btn = Checkbutton(self.frame_for_chkbtn, text="High quality", variable=self.ishd, onvalue=1, command=self.choose_quality)
        self.hd_check_btn.pack(anchor=CENTER)
        #self.update_image()
    
    def callback_on_selection(self, event):
        self.selection = event.widget.curselection()
        if self.selection:
            if self.job:
                self.after_cancel(self.job)
                self.job = None
            index = self.selection[0]
            data = event.widget.get(index)
            name, ip, user, paswd = data.split()
            stream = self.choose_quality()
            self.cap = cv2.VideoCapture(f"rtsp://{user}:{paswd}@{ip}:554/h264/ch01/{stream}/av_stream")
            self.update_image()
    def callback_on_checkbox():
        pass
    def choose_quality(self):

        if self.ishd.get() == 0:
            return 'sub'
            
        else:
            return 'main'
            

    def image_to_default(self):
        
        self.saturation.set(50)
        self.contrast.set(50)
        self.brightness.set(50)

    def add_device_window(self):
        
        self.device_window = Tk()
        self.device_window.title("Device add")
        self.device_window.geometry('260x180')

        self.ip = Entry(self.device_window,width=15)  
        self.ip.place(x=80, y=40)
        self.ip.insert(-1, '172.16.13.202')
        self.ip_lbl = Label(self.device_window, text="IP adress:")
        self.ip_lbl.place(x=13, y=38)

        self.port = Entry(self.device_window,width=3)  
        self.port.insert(-1, 80)
        self.port.place(x=80, y=65)
        self.port_lbl = Label(self.device_window, text="Port:")
        self.port_lbl.place(x=13, y=63)

        self.user = Entry(self.device_window, width=10, )  
        self.user.place(x=80, y=90)
        self.user.insert(-1, 'admin')
        self.user_lbl = Label(self.device_window, text="User:")
        self.user_lbl.place(x=13, y=88)

        self.password = Entry(self.device_window,width=10)  
        self.password.place(x=80, y=115)
        self.password.insert(-1, 'Admin1337')
        self.password_lbl = Label(self.device_window, text="Password:")
        self.password_lbl.place(x=13, y=113)

        self.add_btn = Button(self.device_window, text="Add device", command=self.add_device_to_list)
        self.add_btn.place(x=80, y=140)

        self.cancel_btn = Button(self.device_window, text="Cancel", command=self.device_window.destroy)
        self.cancel_btn.place(x=160, y=140)

        
    
    def add_device_to_list(self):
        self.model_name = Hikvision(self.ip.get(), self.user.get(), self.password.get(), self.port.get())
        self.cameras_list.insert(0, f'{self.model_name.get_model_name()}                    {self.ip.get()} {self.user.get()} {self.password.get()}')
        self.device_window.destroy()
       

    def remove_device(self):
        self.cameras_list.delete(0)
        self.after_cancel(self.job)
        self.job = None

    def add_motion_events(self):
        events = Hikdb('hik.db')
        self.journal_events.insert(0, *events.show_events())

    def md_setting(self):
        self.md_window = Tk()
        self.md_window.title("Motion detector")
        self.md_window.geometry('260x180')
        self.enable_md_checkbutton = Checkbutton(self.md_window, text="Enable detector")
        self.enable_md_checkbutton.pack(anchor=CENTER)
        self.sensivity_scale = Scale(self.md_window, orient=HORIZONTAL)
        self.sensivity_scale.place(x=70, y=20)


    def update_image(self):
        
        # Get the latest frame and convert image format
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        resize_image = cv2.resize(self.image, (650,450)) # resize for my canvas
        pil_image = Image.fromarray(resize_image) # to PIL format
        self.frame = ImageTk.PhotoImage(pil_image, master=self) # to ImageTk format
        # Update image
        self.player.create_image(0, 0, anchor=NW, image=self.frame)
        #while self.selection:
        self.job = self.after(20, self.update_image) # 20 - interval in ms to get the latest frame
       # if not self.selection:
            #break
       
    
app = MainWindow()
app.mainloop()