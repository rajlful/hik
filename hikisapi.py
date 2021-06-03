import requests
from requests.auth import HTTPDigestAuth
import xmltodict
from http import HTTPStatus
import const
import settings

class Hikvision:

    def __init__(self, ipaddr, user='admin', paswd='Admin1337', port=80):
        
        self.ipaddr = ipaddr
        self.user = user
        self.paswd = paswd
        self.port = port
        self.HOST = f'http://{self.ipaddr}:{self.port}/ISAPI' 
    
    def __repr__(self):
        
        return f"<Device adress: {self.ipaddr}, user: {self.user}, password: {self.paswd}, port: {self.port}>"

    def __send_request(self, method, path, data=None):
                
        method = getattr(requests, method, data) 
        incoming_request = method(f'{self.HOST}{path}', auth=HTTPDigestAuth(self.user, self.paswd), data=data)
        return incoming_request
        
    def check_device_status(self):
        
        device_status = self.__send_request('get', '/System/status').status_code
        if device_status == HTTPStatus.OK:
            return HTTPStatus.OK
        elif device_status == HTTPStatus.BAD_REQUEST: 
            raise ConnectionError("Bad request")
        elif device_status == HTTPStatus.UNAUTHORIZED:
            raise ConnectionError("Unauthorized")
        elif device_status == HTTPStatus.FORBIDDEN:
            raise ConnectionError("Forbidden")
        elif device_status == HTTPStatus.NOT_FOUND:
            raise ConnectionError("Not Found")
        elif device_status == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise ConnectionError("Internal Server Error")
        elif device_status == HTTPStatus.NOT_IMPLEMENTED:
            raise ConnectionError("Not Implemented")

    def get_model_name(self):

        if self.check_device_status() == HTTPStatus.OK:
            device_info = self.__send_request('get','/System/deviceinfo')
            all_device_info = xmltodict.parse(device_info.text)
            return all_device_info['DeviceInfo']['model']
        else:
            return self.check_device_status()
    
    def get_device_capabilities(self, stream=const.MAIN):  #MAIN - основной поток камеры. SUB - субпоток
        
        if self.check_device_status() == HTTPStatus.OK:
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
        else:
            return self.check_device_status()   
    
    def set_device_settings(self, codec, resolution, fps, stream=const.MAIN):
        
        if self.check_device_status() == HTTPStatus.OK:
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
        else:
            return self.check_device_status() 

    def set_image_settings(self):
        pass

    def set_network_settings(self):
        pass

    def set_datetime_manual(self, user_date_time):
        
        if self.check_device_status() == HTTPStatus.OK:
            datetime_settings = xmltodict.parse(settings.time_settings)
            datetime_settings['Time']['localTime'] = user_date_time
            our_time_settings = xmltodict.unparse(datetime_settings)
            self.__send_request('put', f'/System/time', our_time_settings)
            return our_time_settings
        else:
            return self.check_device_status()
            
    def set_datetime_by_ntp(self):
        pass

    def set_motion_detector(self):
        pass

    def upgrade_firmware(self):
        pass

    def restore_to_default(self):

        if self.check_device_status() == HTTPStatus.OK:
            restoring = self.__send_request('put', '/System/factoryReset')
            if restoring.status_code == HTTPStatus.OK:
                return "Устройство сбрасывается до заводских настроек. Не перезагружайте камеру."
            else:
                return f"Что-то пошло не так. Камера вернула {restoring.status_code}"
        else:
            self.check_device_status() 

    def reboot(self):

        if self.check_device_status() == HTTPStatus.OK:    
            rebooting = self.__send_request('put','/System/reboot')
            if rebooting.status_code == HTTPStatus.OK:
                return "Устройство перезагружается"
            else:
                return f"Что-то пошло не так. Камера вернула {rebooting.status_code}"
        else:
            self.check_device_status() 
        
    
    def get_events(self):
       # events = requests.get(f'http://{self.ipaddr}:{self.port}/ISAPI/Event/notification/alertStream',
                            #auth=HTTPDigestAuth(self.user, self.paswd))
        #return events, events.status_code, events.text   тут все сложно
        pass

    def get_device_config(self):
       
        if self.check_device_status() == HTTPStatus.OK:    
            device_config = self.__send_request('get','/System/configurationData')
            with open('configuration_data', 'wb') as config:
                config.write(device_config.content)
            return 'Конфигурация скопирована'
        else:
            self.check_device_status() 
        

    def set_device_config(self):
        pass

    def get_screenshot(self):
        pass


if __name__ == "__main__":
    a = Hikvision(settings.ipaddr, settings.user, settings.paswd)
    #print(a.set_device_settings('H.264', '1280x720', '2000'))
    #print(a.get_device_capabilities())
    #print(a.get_model_name())
    #print(settings.time_settings)
    print(a.set_datetime_manual('2021-07-04T16:06:12'))