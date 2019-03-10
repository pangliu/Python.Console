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