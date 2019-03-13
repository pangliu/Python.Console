import requests
import json
from default_config import ApiConfig
from helper_rsa import RsaHelper
from Crypto.Hash import MD5
import hashlib


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

def host_info():
    print('host_info')
    data = 'key=' + ApiConfig.SIGN_KEY
    md5Obj = hashlib.md5()
    md5Obj.update(data.encode("utf-8"))
    header = md5Obj.hexdigest()
    my_headers = {'signMsg': header}
    response = requests.get(ApiConfig.HOST_INFO_URL, headers=my_headers)
    if response.status_code == requests.codes.ok:
        print(response.text)
        resp_json = json.loads(response.text)
        if resp_json['resCode'] == '000':
            resp = RsaHelper.rsa_decrypt(resp_json['response'])
        else:
            resp = resp_json['resMsg']
    else:
        resp = None
    return resp

def device_info(seraril_no):
    print('device_info')
    data = 'serialNo=' + seraril_no + 'key=' + ApiConfig.SIGN_KEY
    md5Obj = hashlib.md5()
    md5Obj.update(data.encode("utf-8"))
    header = md5Obj.hexdigest()
    my_headers = {'signMsg': header}
    parameter = {'serialNo': seraril_no}
    response = requests.get(ApiConfig.DEVICE_INFO_URL, headers=my_headers, params=parameter)
    # print(response.text)
    if response.status_code == requests.codes.ok:
        resp_json = json.loads(response.text)
        if resp_json['resCode'] == '000':
            resp = RsaHelper.rsa_decrypt(resp_json['response'])
        else:
            resp = resp_json['resMsg']
    else:
        resp_decode = None
    return resp
