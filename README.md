It is simple VMS for Hikvision cameras. You can add several devices, watch streams and change some settings(motion detector, image settings, device settings)

If you want to use only hikisapi.py you should write access info of camera in settings.py

def get_events() writes events about motion in the db. If you need it you should create db with name hik.db. For this you should use def create_db in hikdb.py 

You should installed before using:

xmltodict
sqlite3
tkinter
PIL
cv2
