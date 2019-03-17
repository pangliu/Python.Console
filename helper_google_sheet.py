import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GetGoogleSheet:
    def get_gs_list():
        print('get_gs_list')
        try:
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('python-test-f2a1c4aaf2b0.json', scope)
            gs = gspread.authorize(credentials)
            sheet = gs.open("python-test").sheet1
            list_of_hashes = sheet.get_all_records()
            host_array = []
            for item in list_of_hashes:
                if item['server_name'] and item['host_url']:
                    # host_json = {item['server_name']:item['host_url']}
                    # server_name = item['server_name']
                    # host_url = item['host_url']
                    # host_array[server_name] = host_url
                    host_array.append(item)
        except:
            list_of_hashes = None
        print(host_array)
        return host_array