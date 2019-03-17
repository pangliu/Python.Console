import requests
import json
from default_config import ApiConfig
from helper_rsa import RsaHelper
from Crypto.Hash import MD5
import hashlib
import ut


def device_config_update(serial_no, phone_number, host_url):
    config_content = {'phone':phone_number}
    parameter = {'serialNo': serial_no, 'configContent':json.dumps(config_content)}
    print('params: ' + str(parameter))
    api_url = 'http://{}/deviceConfig'.format(host_url)
    print(api_url)
    response = requests.post(api_url, parameter)
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        return '連線異常'

def device_restart(serial_no, redo_job, host_url):
    # 驗證 signMsg
    sign_msg = 'redoJob=' + redo_job + '&serialNo=' + serial_no + '&key=' + ApiConfig.SIGN_KEY
    md5Obj = hashlib.md5()
    md5Obj.update(sign_msg.encode("utf-8"))
    header = md5Obj.hexdigest()
    my_headers = {'signMsg': header, 'Content-Type':'application/x-www-form-urlencoded'}
    parameter = {'serialNo': serial_no, 'redoJob': redo_job}
    api_url = 'http://{}/restartDevice'.format(host_url)
    response = requests.post(api_url, headers=my_headers, data=parameter)
    if response.status_code == requests.codes.ok:
        return response.text
    else:
        return '連線異常'

# 更新 server 上的 devices
def server_apk_upgrade(data_json, host_url):
    print('server_apk_upgrade')
    api_url = 'http://{}/upgrade'.format(host_url)
    print('api_url: ' + api_url)
    # signMsg 驗證
    apk_url_str = json.dumps(data_json)
    rsa_apk_url = RsaHelper.rsa_encrypt(apk_url_str)
    sign_msg = 'apkURL=' + rsa_apk_url + '&key=' + ApiConfig.SIGN_KEY
    md5Obj = hashlib.md5()
    md5Obj.update(sign_msg.encode("utf-8"))
    header = md5Obj.hexdigest()
    my_headers = {'signMsg': header, 'Content-Type':'application/x-www-form-urlencoded'}
    parameter = {'apkURL':rsa_apk_url}
    response = requests.post(api_url, headers=my_headers, data=parameter)
    return response.text

# 到 jenkins 主機取得所有資訊列表
def get_all_device_info(gs_data):
    print('get_all_device_info')
    params = ut.Utils.get_all_host_info_params(gs_data)
    api_url = 'http://{}/getAllDeviceInfo'.format(ApiConfig.ALL_DEVICE_INFO_URL)
    response = requests.get(api_url, params=params)
    if response.status_code == requests.codes.ok:
        resp_json = json.loads(response.text)
        if resp_json['code'] == '200':
            resp = resp_json['data']
        else:
            resp = resp_json['resMsg']
    else:
        resp = None
    # 假資料
    test_resp = ut.Utils.get_json_file('./utils/test_all_host_info.json')
    resp = test_resp['data']

    if resp is not None:
        gs_obj = ut.Utils.handle_host_data(gs_data)
        resp = ut.Utils.transfor_host_info_json(resp, gs_obj)

    return resp

# 取得 server api log
def query_api_logs(host_data):
    server_name = host_data['server_name']
    host_url = host_data['host_url']
    api_url = 'http://{}/queryApiLogs'.format(host_url)
    params = {'host_name':server_name}
    print('api_url: ' + str(api_url))
    print('params: ' + str(params))
    response = requests.get(api_url, params=params)
    if response.status_code == requests.codes.ok:
        resp_json = json.loads(response.text)
        if resp_json['code'] == '200':
            resp = {'api_logs': resp_json['data']}
        else:
            resp = resp_json['resMsg']
    else:
        resp = None
    # 假資料
    # test_resp = ut.Utils.get_json_file('./utils/test_query_server_log.json')
    # resp = {'api_logs': test_resp['data']}
    return resp

def query_device_logs(host_data):
    print('query_device_logs')
    server_name = host_data['server_name']
    host_url = host_data['host_url']
    serial_no = host_data['serial_no']
    api_url = 'http://{}/queryDeviceLogs'.format(host_url)
    params = {'host_name':server_name, 'serial_no': serial_no}
    print('api_url: ' + str(api_url))
    print('params: ' + str(params))
    response = requests.get(api_url, params=params)
    if response.status_code == requests.codes.ok:
        resp_json = json.loads(response.text)
        if resp_json['code'] == '200':
            # resp = resp_json['data']
            resp = {'device_logs': resp_json['data']}
        else:
            resp = resp_json['resMsg']
    else:
        resp = None
    # 假資料
    # test_resp = ut.Utils.get_json_file('./utils/test_query_device_log.json')
    # resp = {'device_logs': test_resp['data']}
    return resp

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
    data = 'serialNo=' + seraril_no + '&key=' + ApiConfig.SIGN_KEY
    md5Obj = hashlib.md5()
    md5Obj.update(data.encode("utf-8"))
    header = md5Obj.hexdigest()
    my_headers = {'signMsg': header}
    parameter = {'serialNo': seraril_no}
    response = requests.get(ApiConfig.DEVICE_INFO_URL, headers=my_headers, params=parameter)
    if response.status_code == requests.codes.ok:
        resp_json = json.loads(response.text)
        if resp_json['resCode'] == '000':
            resp = RsaHelper.rsa_decrypt(resp_json['response'])
        else:
            resp = resp_json['resMsg']
    else:
        resp_decode = None
    return resp
