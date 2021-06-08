import requests
from requests.auth import HTTPDigestAuth
import xmltodict
from http import HTTPStatus
import const
import settings
import socket

class Hikvision:

    def __init__(self, ipaddr, user='admin', paswd='Admin1337', port=80):
        
        self.ipaddr = ipaddr
        self.user = user
        self.paswd = paswd
        self.port = port
        self.HOST = f'http://{self.ipaddr}:{self.port}/ISAPI' 
    
    def __repr__(self):
        
        return f"<Device adress: {self.ipaddr}, user: {self.user}, password: {self.paswd}, port: {self.port}>"

    def __send_request(self, method, path, data=None, timeout=None, stream=None):
                
        method = getattr(requests, method) 
        incoming_request = method(f'{self.HOST}{path}', auth=HTTPDigestAuth(self.user, self.paswd), data=data, timeout=timeout, stream=stream)
        return incoming_request
        
    def is_device_status_ok(self):
        
        device_status = self.__send_request('get', '/System/status').status_code
        if device_status == HTTPStatus.OK:
            return True
        elif device_status == HTTPStatus.BAD_REQUEST: 
            return False
        elif device_status == HTTPStatus.UNAUTHORIZED:
            return False
        elif device_status == HTTPStatus.FORBIDDEN:
            return False
        elif device_status == HTTPStatus.NOT_FOUND:
            return False
        elif device_status == HTTPStatus.INTERNAL_SERVER_ERROR:
            return False
        elif device_status == HTTPStatus.NOT_IMPLEMENTED:
            return False

    def get_model_name(self):

        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        device_info = self.__send_request('get','/System/deviceinfo')
        all_device_info = xmltodict.parse(device_info.text)
        return all_device_info['DeviceInfo']['model']
        
    
    def get_device_capabilities(self, stream=const.MAIN):  #MAIN - основной поток камеры. SUB - субпоток
        
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        device_capabilities = self.__send_request('get', f'/Streaming/channels/{stream}/capabilities')
        device_capabilities = xmltodict.parse(device_capabilities.text)
        # берем из полученной xml только нужные параметры
        capabilities = device_capabilities['StreamingChannel']['Video']
        width = capabilities['videoResolutionWidth']['@opt'].split(',')
        height = capabilities['videoResolutionHeight']['@opt'].split(',')
        resolutions = [[w + 'x' + h] for w, h in zip(width, height)]  # чтобы разрешение было в понятном виде
        fps = capabilities['maxFrameRate']['@opt'].split(',')
        codecs = capabilities['videoCodecType']['@opt'].split(',')
        audio_codecs = device_capabilities['StreamingChannel']['Audio']['audioCompressionType']['@opt'].split(',')
        useful_capabilities = { 'resolutions' : resolutions,
                                 'codecs' : codecs,
                                'fps' : fps,
                                'audio_codecs' : audio_codecs
                                }
        return useful_capabilities
    
    def set_device_settings(self, codec, resolution, fps, stream=const.MAIN):
        
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        width, height = resolution.split('x')
        default_settings = xmltodict.parse(settings.device_settings)
        inside_xml_video = default_settings['StreamingChannel']['Video']
        inside_xml_video['videoCodecType'] = codec
        inside_xml_video['videoResolutionWidth'] = width 
        inside_xml_video['videoResolutionHeight'] = height
        inside_xml_video['maxFrameRate'] = fps
        our_settings = xmltodict.unparse(default_settings).replace('\n','')   # unparse возвращает xml c \n в запросе. Такой запрос камера не принимает
        self.__send_request('put', f'/Streaming/channels/{stream}/', our_settings)
        return 'Настройки успешно применились'
        
    def set_image_settings(self):
        pass

    def set_network_settings(self):
        pass

    def set_datetime_manual(self, user_date_time):
        
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        datetime_settings = xmltodict.parse(settings.time_settings)
        datetime_settings['Time']['localTime'] = user_date_time
        our_time_settings = xmltodict.unparse(datetime_settings)
        self.__send_request('put', f'/System/time', our_time_settings)
        return our_time_settings
            
    def set_datetime_by_ntp(self):
        pass

    def set_motion_detector(self):
        pass

    def upgrade_firmware(self):
        pass

    def restore_to_default(self):

        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        self.__send_request('put', '/System/factoryReset')
        return "Устройство сбрасывается до заводских настроек. Не перезагружайте камеру."
        
    def reboot(self):

        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')    
        self.__send_request('put','/System/reboot')
        return "Устройство перезагружается"
        
    def get_events(self):
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')   
        events = self.__send_request('get', '/Event/notification/alertStream', stream=True)
        for event in events.iter_lines():
            decoded_event = event
            print(decoded_event)
      
       

    def get_device_config(self):
       
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')   
        device_config = self.__send_request('get','/System/configurationData')
        with open('configuration_data', 'wb') as config:
            config.write(device_config.content)
        return 'Конфигурация скопирована'
        

    def set_device_config(self):
        pass

    def get_screenshot(self):
        pass


if __name__ == "__main__":
    a = Hikvision(settings.ipaddr, settings.user, settings.paswd)
    #print(a.set_device_settings('H.264', '1280x720', '2000'))
    a.get_events()
    #print(a.get_model_name())
    #print(settings.time_settings)
    #print(a.set_datetime_manual('2021-07-04T16:06:12'))