import csv
import json

class Utils():
    def __init__(self):
        pass

    @staticmethod
    def get_json_file(json_file):
        data = 'load data fail'
        with open(json_file) as f:
             data = json.load(f)
        return data
    
    @staticmethod
    def get_upgrade_json(serial_no, file_name, type_text, url):
        data = []
        for index in range(len(serial_no)):
            # sereial_obj = {'serial_no': serial_no[index]}
            url_array = []
            json_obj = {
                'file_name':file_name[index],
                'type':type_text[index],
                'url':url[index]}
            url_array.append(json_obj)
            data_array = {'url':url_array, 'serial_no':serial_no[index]}
            data.append(data_array)
        data_obj = {'data':data}
        return data_obj

    @staticmethod
    def get_all_host_info_params(gs_data):
        param_server_name = ''
        param_host_url = ''
        for item in gs_data:
            server_name = item['server_name']
            if param_server_name:
                param_server_name = param_server_name + ',' + server_name
            else:
                param_server_name = server_name
            host_url = item['host_url']
            if param_host_url:
                param_host_url = param_host_url + ',' + host_url
            else:
                param_host_url = host_url
        print('param_server_name: ' + param_server_name)
        print('param_host_url: ' + param_host_url)
        params = {'hostList':param_host_url, 'hostNameList':param_server_name}
        return params
    
    # 將 google sheet 回傳的資料格式 pars 為 jsonObject 格式
    # ex: {'python001':'127.0.0.1:5000'}
    @staticmethod
    def handle_host_data(gs_data):
        host_obj = {}
        for item in gs_data:
            if item['server_name'] and item['host_url']:
                server_name = item['server_name']
                host_url = item['host_url']
                host_obj[server_name] = host_url
        return host_obj

    # 合併從 server 取得的 host_info 與 google_sheet 取得的 url
    @staticmethod
    def transfor_host_info_json(host_info, gs_data):
        print('transfor_host_info_json')
        # print(host_info)
        # print(gs_data)
        for info in host_info:
            # 用 host_info 的 name 當作 key 取得 gs_data 中的 host_url
            host_name = info['hostName']
            host_url = gs_data[host_name]
            if host_url:
                print(host_url)
                info['hostUrl'] = host_url
            else:
                info['hostUrl'] = None
        # print(host_info)
        return host_info