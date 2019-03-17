
import json


class ApiModel:
    def __init__(self, host_info):
        self.host_info = host_info
        self.host_info_array = []
        for info in self.host_info:
            host_name = info['hostName']
            host_url = info['hostUrl']
            json_obj = {'server_name': host_name, 'host_url': host_url}
            self.host_info_array.append(json_obj)

    def get_host_url_by_server_name(self, server_name):
        for info in self.host_info:
            if info['hostName'] == server_name:
                return info['hostUrl']
        return None

    def get_host_info_by_server_name(self, server_name):
        for info in self.host_info_array:
            if info['server_name'] == server_name:
                return info
        return None
