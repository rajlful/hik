from tkinter import *
from tkinter import ttk
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

        self.cameras_list = Listbox(self, width=23, height=26)
        self.cameras_list.place(x=2, y=30)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.cameras_list.yview)
        self.cameras_list.bind("<<ListboxSelect>>", self.callback_on_selection)

        self.journal_events = Listbox(self, width=43, height=12)
        self.journal_events.place(x=2, y=490)
        self.scrollbar = Scrollbar(self)
        self.scrollbar.config(command=self.journal_events.yview)

        self.add_device_btn = Button(self, text="Add device", command=self.add_device_window)
        self.add_device_btn.place(x=0, y=1)

        self.del_device_btn = Button(self, text="Delete device", command=self.remove_device)
        self.del_device_btn.place(x=75, y=1)

        self.events_btn = Button(self, text="Show events", command=self.add_motion_events)
        self.events_btn.place(x=7, y=459)

        self.motion_detector_btn = Button(self, text="Motion detector", command=self.md_setting)
        self.motion_detector_btn.place(x=200, y=459)

        self.reboot_btn = Button(self, text="Reboot device", command=self.reboot_device)
        self.reboot_btn.place(x=830, y=1)

        self.restore_btn = Button(self, text="Restore device", command=self.restore_device)
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
        self.image_default_btn.place(x=923, y=150, height=21, width=92)
        self.save_image_btn = Button(self, text="Save", command=self.save_image_settings)
        self.save_image_btn.place(x=835, y=150, height=21, width=85)
        

      #  self.cap = cv2.VideoCapture(f"rtsp://admin:Admin1337@172.16.13.184:554/h264/ch01/sub/av_stream")
        self.player = Canvas(self, width=650, height=450, bg='black')
        self.player.place(x=172, y=1)
        self.player_lbl = Label(self, text="No signal", fg='red', bg='black', font="Courier 20" )
        self.player_lbl.place(x=410, y= 200)

        self.frame_for_chkbtn = Frame(self, width=50, height=50)
        self.frame_for_chkbtn.place(x=737, y=460)
        self.ishd = IntVar()
        self.ishd.set(1)
        self.hd_check_btn = Checkbutton(self.frame_for_chkbtn, text="High quality", variable=self.ishd, onvalue=1, command=self.choose_quality)
        self.hd_check_btn.pack(anchor=CENTER)
        #self.update_image()

        self.frame_with_settings = Frame(self, width=185, height=275)
        self.frame_with_settings.place(x=840, y=180)

        self.resolv_lbl = Label(self.frame_with_settings, text="Resolution:")
        self.resolv_lbl.pack()
        self.resolv_cmbbox = ttk.Combobox(self.frame_with_settings)
        self.resolv_cmbbox.pack()
        
        self.codecs_lbl = Label(self.frame_with_settings, text="Codecs:")
        self.codecs_lbl.pack()
        self.codecs_cmbbox = ttk.Combobox(self.frame_with_settings)
        self.codecs_cmbbox.pack()

        self.fps_lbl = Label(self.frame_with_settings, text="Fps:")
        self.fps_lbl.pack()
        self.fps_cmbbox = ttk.Combobox(self.frame_with_settings)
        self.fps_cmbbox.pack()

        self.aud_codecs_lbl = Label(self.frame_with_settings, text="Audio codecs:")
        self.aud_codecs_lbl.pack()
        self.aud_codecs_cmbbox = ttk.Combobox(self.frame_with_settings)
        self.aud_codecs_cmbbox.pack()

        self.get_cap_btn = Button(self, text="Show capabilies", command=self.get_device_cap)
        self.get_cap_btn.place(x=920,y=365)

        self.get_cap_btn = Button(self, text="Apply settings", command=self.apply_settings)
        self.get_cap_btn.place(x=830,y=365)

    def save_image_settings(self):
        name, ip, user, paswd = self.data.split()
        self.settings = Hikvision(ip, user, paswd)
        self.settings.set_image_settings(self.contrast.get(), self.contrast.get(), self.saturation.get())
        
    def reboot_device(self):
        name, ip, user, paswd = self.data.split()
        self.reboot = Hikvision(ip, user, paswd)    
        self.reboot.reboot()

    def restore_device(self):
        name, ip, user, paswd = self.data.split()
        self.restore = Hikvision(ip, user, paswd)    
        self.restore.restore_to_default()

    def apply_settings(self):
        name, ip, user, paswd = self.data.split()
        self.settings = Hikvision(ip, user, paswd)
        self.settings.set_device_settings(self.codecs_cmbbox.get(), self.resolv_cmbbox.get(), self.fps_cmbbox.get())

    def get_device_cap(self):

        name, ip, user, paswd = self.data.split()
        self.device_cap = Hikvision(ip, user, paswd)
        dict_with_caps = self.device_cap.get_device_capabilities()
        
        self.codecs_cmbbox['values'] = dict_with_caps['codecs']
        self.fps_cmbbox['values'] = dict_with_caps['fps']
        self.aud_codecs_cmbbox['values'] = dict_with_caps['audio_codecs']
        self.resolv_cmbbox['values'] = dict_with_caps['resolutions']
       # return resolutions

    def callback_on_selection(self, event):
      
        self.selection = event.widget.curselection()
        if self.selection:
            if self.job:
                self.after_cancel(self.job)
                self.job = None
            index = self.selection[0]
            self.data = event.widget.get(index)
            name, ip, user, paswd = self.data.split()
            stream = self.choose_quality()
            self.cap = cv2.VideoCapture(f"rtsp://{user}:{paswd}@{ip}:554/h264/ch01/{stream}/av_stream")
            self.update_image()
  
    def callback_on_checkbox(self):
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
        self.player_lbl.destroy()
        self.device_window.destroy()
       
    def remove_device(self):
        self.cameras_list.delete(0)
        self.after_cancel(self.job)
        self.job = None

    def add_motion_events(self):
        self.journal_events.delete(0,'end')
        events = Hikdb('hik.db')
        tuple_events = events.show_events()
        for events in tuple_events:
            l = ' '.join(events)
            print(l)
            self.journal_events.insert(0, l)
          
    def md_setting(self):
        self.md_window = Tk()
        self.md_window.title("Motion detector")
        self.md_window.geometry('260x180')
        self.enable_md_checkbutton = Checkbutton(self.md_window, text="Enable detector")
        self.enable_md_checkbutton.pack(anchor=CENTER)
        self.sensivity_scale = Scale(self.md_window, orient=HORIZONTAL)
        self.sensivity_scale.place(x=70, y=20)
        self.apply_btn = Button(self.md_window, text="Apply", command=self.md_enabled)
        self.apply_btn.place(x=100 , y=70)
    
    def md_enabled(self):    
        name, ip, user, paswd = self.data.split()
        self.enable = Hikvision(ip, user, paswd)
        self.isenable = IntVar()
        self.isenable.set(1)
        self.enable.enable_motion_detector(self.isenable.get())
        self.enable.set_md_sensitivity(self.sensivity_scale.get())

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
    def flow_events(self):
        name, ip, user, paswd = self.data.split()
        self.events_flow = Hikvision(ip, user, paswd)  
        self.events_flow.get_events() 

if __name__ == '__main__':    
    app = MainWindow()
    app.mainloop()



   # process1 = Process(target=app.mainloop)
   # process2 = Process(target=app.flow_events)

   # process1.start()
   # process2.start()

   # process1.join()
   # process2.join()