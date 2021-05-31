import requests
from requests.auth import HTTPDigestAuth
import xmltodict
import device_settings
import const
import rtsp

class Hikvision:

    def __init__(self, ipaddr, user='admin', paswd='Admin1337', port=80):
        
        self.ipaddr = ipaddr
        self.user = user
        self.paswd = paswd
        self.port = port
        device_status = requests.get(f'http://{self.ipaddr}:{self.port}/ISAPI/System/status',
                               auth=HTTPDigestAuth(self.user, self.paswd)).status_code
        if device_status == 400: 
            raise ConnectionError("Bad request")
        elif device_status == 401:
            raise ConnectionError("Unauthorized")
        elif device_status == 403:
            raise ConnectionError("Forbidden")
        elif device_status == 404:
            raise ConnectionError("Not Found")
        elif device_status == 500:
            raise ConnectionError("Internal Server Error")
        elif device_status == 501:
            raise ConnectionError("Not Implemented")
    
    def __repr__(self):
        
        return f"<Device adress: {self.ipaddr}, user: {self.user}, password: {self.paswd}, port: {self.port}>"

    def get_model_name(self):
        
        device_info = requests.get(f'http://{self.ipaddr}:{self.port}/ISAPI/System/deviceinfo',
                               auth=HTTPDigestAuth(self.user, self.paswd))
        all_device_info = xmltodict.parse(device_info.text)
        return all_device_info['DeviceInfo']['model']
    
    def get_device_capabilities(self, stream='101'):  #101 - основной поток камеры. 102 - субпоток
        
        device_capabilities = requests.get(f'http://{self.ipaddr}:{self.port}/ISAPI/Streaming/channels/{stream}/capabilities',
                               auth=HTTPDigestAuth(self.user, self.paswd))
        dict_with_all_capabilities = xmltodict.parse(device_capabilities.text)
        # берем из полученной xml только нужные параметры
        width = dict_with_all_capabilities['StreamingChannel']['Video']['videoResolutionWidth']['@opt'].split(',')
        height = dict_with_all_capabilities['StreamingChannel']['Video']['videoResolutionHeight']['@opt'].split(',')
        resolutions = [[w + 'x' + h] for w, h in zip(width, height)]  # чтобы разрешение было в понятном виде
        fps = dict_with_all_capabilities['StreamingChannel']['Video']['maxFrameRate']['@opt'].split(',')
        codecs = dict_with_all_capabilities['StreamingChannel']['Video']['videoCodecType']['@opt'].split(',')
        audio_codecs = dict_with_all_capabilities['StreamingChannel']['Audio']['audioCompressionType']['@opt'].split(',')
        dict_with_useful_capabilities = { 'resolutions' : resolutions,
                                          'codecs' : codecs,
                                          'fps' : fps,
                                          'audio_codecs' : audio_codecs
                                        }
        return dict_with_useful_capabilities
    
    def set_device_settings(self, codec, resolution, fps, audio_codec):
      #  device_capabilities = get_device_capabilities()
      #  device_setting = device_settings.device_config
       # return device_setting
       pass

    def set_image_settings(self):
        pass

    def set_network_settings(self):
        pass

    def set_datetime(self):
        pass

    def set_motion_detector(self):
        pass

    def upgrade_firmware(self):
        pass

    def restore_to_default(self):
        restoring = requests.put(f'http://{self.ipaddr}:{self.port}/ISAPI/System/factoryReset',
                               auth=HTTPDigestAuth(self.user, self.paswd))
        if restoring.status_code == 200:
            return "Устройство сбрасывается до заводских настроек. Не перезагружайте камеру."
        else:
            return f"Что-то пошло не так. Камера вернула {restoring.status_code}"

    def reboot(self):
        rebooting = requests.put(f'http://{self.ipaddr}:{self.port}/ISAPI/System/reboot',
                               auth=HTTPDigestAuth(self.user, self.paswd))
        if rebooting.status_code == 200:
            return "Устройство перезагружается"
        else:
            return f"Что-то пошло не так. Камера вернула {rebooting.status_code}"
    
    def get_events(self):
       # events = requests.get(f'http://{self.ipaddr}:{self.port}/ISAPI/Event/notification/alertStream',
                            #auth=HTTPDigestAuth(self.user, self.paswd))
        #return events, events.status_code, events.text   тут все сложно
        pass

    def get_device_config(self):
        device_config = requests.get(f'http://{self.ipaddr}:{self.port}/ISAPI/System/configurationData',
                                         auth=HTTPDigestAuth(self.user, self.paswd))
        with open('configuration_data', 'wb') as config:
            config.write(device_config.content)
        return 'Конфигурация скопирована'

    def set_device_config(self):
        pass

    def get_screenshot(self):
        pass


if __name__ == "__main__":
    a = Hikvision('172.16.13.70', 'admin', 'Admin321678')
    #print(a.get_device_capabilities())
    #print(a.set_device_settings('h.264'))
    
    