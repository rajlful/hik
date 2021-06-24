from tkinter import *

from hikisapi import Hikvision

class Main_window(Tk):

    def __init__(self):
        
        super().__init__()
        self.main_window = Tk()
        self.main_window.title("HIKVISION VMS")
        self.main_window.geometry('1100x700')

        self.cameras_list = Listbox(self.main_window, width=23, height=20)
        self.cameras_list.place(x=0, y=30)

        self.add_device_btn = Button(self.main_window, text="Add device", command=add_device_window)
        self.add_device_btn.place(x=0, y=1)

        self.del_device_btn = Button(self.main_window, text="Delete device")
        self.del_device_btn.place(x=75, y=1)






    


def add_device_window():
    
    device_window = Tk()
    device_window.title("Device add")
    device_window.geometry('260x180')

    ip = Entry(device_window,width=15)  
    ip.place(x=80, y=40)
    ip_lbl = Label(device_window, text="IP adress:")
    ip_lbl.place(x=13, y=38)

    port = Entry(device_window,width=3)  
    port.place(x=80, y=65)
    port_lbl = Label(device_window, text="Port:")
    port_lbl.place(x=13, y=63)

    user =  Entry(device_window,width=10)  
    user.place(x=80, y=90)
    user_lbl = Label(device_window, text="User:")
    user_lbl.place(x=13, y=88)

    password = Entry(device_window,width=10)  
    password.place(x=80, y=115)
    password_lbl = Label(device_window, text="Password:")
    password_lbl.place(x=13, y=113)

    add_btn = Button(device_window, text="Add device", command=create_new_example(ip,port,user,password))
    add_btn.place(x=80, y=140)

    cancel_btn = Button(device_window, text="Cancel", command=device_window.destroy)
    cancel_btn.place(x=160, y=140)


#main gui start
#main_window = Tk()
#main_window.title("HIKVISION VMS")
#main_window.geometry('1100x700')

#cameras_list = Listbox(main_window, width=23, height=20)
#cameras_list.place(x=0, y=30)

#add_device_btn = Button(main_window, text="Add device", command=add_device_window)
#add_device_btn.place(x=0, y=1)

#del_device_btn = Button(main_window, text="Delete device")
#del_device_btn.place(x=75, y=1)
#main gui stop 





a = Main_window()
a.mainloop()
