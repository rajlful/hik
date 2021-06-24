import requests
from requests.auth import HTTPDigestAuth
import xmltodict
from http import HTTPStatus
import time
import sqlite3

import const
import settings
import hiklogger
from hikdb import Hikdb

class Hikvision:

    def __init__(self, ip_address, user='admin', paswd='Admin1337', port=80):
        
        self.ip_address = ip_address
        self.user = user
        self.paswd = paswd
        self.port = port
        self.HOST = f'http://{self.ip_address}:{self.port}/ISAPI'

    def __repr__(self):
        
        return f"<Device adress: {self.ip_address}, user: {self.user}, password: {self.paswd}, port: {self.port}>"

    def __send_request(self, method, path, data=None, timeout=None, stream=None):
                
        method = getattr(requests, method) 
        incoming_request = method(f'{self.HOST}{path}', auth=HTTPDigestAuth(self.user, self.paswd), data=data, timeout=timeout, stream=stream)
        return incoming_request

    def __set_md_setting(self, setting, value):
        
        if setting == 'enable_detector':
            current_settings = xmltodict.parse(settings.md_settings)
            current_settings['MotionDetection']['enabled'] = value
            our_settings = xmltodict.unparse(current_settings)
        
        elif setting == 'detector sensivity':
            current_settings = xmltodict.parse(settings.md_settings)  
            current_settings['MotionDetection']['MotionDetectionLayout']['sensitivityLevel'] = value
            our_settings = xmltodict.unparse(current_settings)
        
        self.__send_request('put', '/System/Video/inputs/channels/1/motionDetection', data=our_settings)
       
    def is_device_status_ok(self):
        
        device_status = self.__send_request('get', '/System/status').status_code
        hiklogger.logger.debug(f'Response {device_status}')
        return device_status == HTTPStatus.OK

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
    
    def get_network_settings(self):
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        network_settings = xmltodict.parse(self.__send_request('get', '/System/Network/interfaces/1/ipAddress').text)
        inside_network_settings = network_settings['IPAddress']
        return {'ip': inside_network_settings['ipAddress'], 
                'mask': inside_network_settings['subnetMask'], 
                'gateway': inside_network_settings['DefaultGateway']['ipAddress'], 
                'primary_dns': inside_network_settings['PrimaryDNS']['ipAddress']
                }

    def set_network_settings(self, ip_adress, mask, gateway, dns):
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        network_settings = xmltodict.parse(settings.network_settings)
        inside_network_settings = network_settings['NetworkInterface']['IPAddress']
        inside_network_settings['ipAddress'] = ip_adress
        inside_network_settings['subnetMask'] = mask
        inside_network_settings['DefaultGateway']['ipAddress'] = gateway
        inside_network_settings['PrimaryDNS']['ipAddress'] = dns
        our_network_settings = xmltodict.unparse(network_settings)
        self.__send_request('put', '/System/Network/interfaces/1/ipAddress', data=our_network_settings)
        return 'Настройки успешно применились'

    def get_rtsp_url(self):
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        device_ports = xmltodict.parse(self.__send_request('get', '/Security/adminAccesses').text)
        rtsp_port = device_ports['AdminAccessProtocolList']['AdminAccessProtocol'][3]['portNo']
        rtsp_url = f'rtsp://{self.user}:{self.paswd}@{self.ip_address}:{rtsp_port}/h264/ch01/main/av_stream'
        return rtsp_url

    def set_datetime_manual(self, user_date_time):
        
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        datetime_settings = xmltodict.parse(settings.time_settings)
        datetime_settings['Time']['localTime'] = user_date_time
        our_time_settings = xmltodict.unparse(datetime_settings)
        self.__send_request('put', f'/System/time', our_time_settings)
        return 'Время успешно изменено'
            
    def set_datetime_by_ntp(self):
        pass

    def enable_motion_detector(self, value):

        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        return self.__set_md_setting('enable_detector', value)  # value true = enabale, false = disable
    
    def set_md_sensitivity(self, sensitivity_level):

        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')
        return self.__set_md_setting('detector sensivity', sensitivity_level)

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
        adder_to_db = Hikdb('hik.db')
        last_event_time = 0
        for event in events.iter_lines():
            decoded_event = event.decode('utf-8')
            if "Motion alarm" in decoded_event:
                first_event_time = time.time()  
                delay = first_event_time - last_event_time # 1624022556
                if delay > const.DELAY_BETWEEN_EVENTS:
                    print("Motion alarm")
                    hiklogger.event_logger.info("Motion alarm detect")
                    adder_to_db.add_events(self.get_model_name(), "Motion alarm" )
                    last_event_time = first_event_time
                else:
                    continue    
            else:
                current_time = time.time()
                delay = current_time - last_event_time
                if delay > const.DELAY_BETWEEN_EVENTS and last_event_time !=0:
                    print("Motion stopped")
                    hiklogger.event_logger.info("Motion stopped")
                    adder_to_db.add_events(self.get_model_name(), "Motion stopped" )
                    last_event_time = 0

    def get_device_config(self):
       
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')   
        return self.__send_request('get','/System/configurationData')
        
    def save_device_config(self):    
        status = self.is_device_status_ok()
        if not status:
            raise ValueError('Error, more info in logs')   
        device_config = self.get_device_config()
        with open('configuration_data', 'wb') as config:
            config.write(device_config.content)
        return 'Конфигурация скопирована'
        
    def set_device_config(self):
        pass

    def get_screenshot(self):
        pass

    def create_db(self, name):
        pass

if __name__ == "__main__":
    a = Hikvision(settings.ipaddr, settings.user, settings.paswd)
    a.get_events()
   