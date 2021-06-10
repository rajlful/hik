import logging

logger = logging.getLogger('camera_return')
logger.setLevel(logging.DEBUG)
file_log = logging.FileHandler('hikisapi_log.txt')
file_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log.setFormatter(formatter)
logger.addHandler(file_log)
logger.debug(f'Response')


event_logger = logging.getLogger('camera_events')
event_logger.setLevel(logging.INFO)
file_events_log = logging.FileHandler('events_log.txt')
file_events_log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_events_log.setFormatter(formatter)
event_logger.addHandler(file_events_log)
event_logger.info(f'Event')