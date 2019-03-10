import requests
import json
from default_config import ApiConfig


def device_config_update(serial_no, phone_number):
    # print('device_config' + serial_no + ' + ' + phone_number)
    config_content = {'phone':phone_number}
    # print(json.dumps(config_content))
    parameter = {'serialNo': serial_no, 'configContent':json.dumps(config_content)}
    response = requests.post(ApiConfig.DEVICE_CONFIG_UPDATE_URL, parameter)
    return response.text

def device_restart(serial_no, redo_job):
    parameter = {'serialNo': serial_no, 'redoJob': redo_job}
    response = requests.post(ApiConfig.DEVICE_RESTART_URL, parameter)
    return response.text
