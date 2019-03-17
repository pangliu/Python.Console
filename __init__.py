from flask import Flask, render_template, Blueprint, url_for, request
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_bootstrap import Bootstrap
from flask import json
import ut
import helper_api
from form import FormDeviceConfig, FormDeviceRestart, FormDeviceApkUpgrade
from helper_mysql import SqlHelp

from helper_google_sheet import GetGoogleSheet
from api_model import ApiModel

# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials


# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# scope = "https://spreadsheets.google.com/feeds"
# scope = "https://www.googleapis.com/auth/spreadsheets.readonly"


app = Flask(__name__)

app.config["SECRET_KEY"] = "12345678"
Bootstrap(app)
nav = Nav(app)

nav.register_element('my_navbar', Navbar(
    'pythonConsole',
    View('Home page', '.index')))


# 首頁 HomePage
@app.route('/')
def index():
    print('index')
    google_sheet_data = GetGoogleSheet.get_gs_list()
    host_info_data = helper_api.get_all_device_info(google_sheet_data)
    if host_info_data is None:
        return render_template('index.html', host_info=host_info_data)
#   將 model 設定為全域變數
    global model
    model = ApiModel(host_info_data)
    return render_template('index.html', host_info=host_info_data)

# python_server 的 api_log 列表頁面
@app.route('/server_log/<server_name>/')
def server_log(server_name):
    host_info = model.get_host_info_by_server_name(server_name)
    print(host_info)
    api_logs = helper_api.query_api_logs(host_info)
#     print(model.get_host_url_by_server_name('python001'))
#   假資料
    test_data = ut.Utils.get_json_file('./utils/api_log.json')
    return render_template(
        'server_log.html',
        server_name=server_name,
        api_logs=api_logs)

# 更新 server device 頁面
@app.route('/server_api/<server_name>/', methods=['GET', 'POST'])
def server_api(server_name):
    print('server_api')
    form_server_update_apk = FormDeviceApkUpgrade()
    return render_template(
        'server_api.html',
        form_server_update_apk=form_server_update_apk,
        server_name=server_name)

# 呼叫更新 apk 的 api
@app.route('/server_apk_upgrade', methods=['POST'])
def server_apk_upgrade():
    print('server_apk_upgrade')
    form_server_update_apk = FormDeviceApkUpgrade()
    if request.method == 'POST':
        server_name = request.form.get('server_name')
        print('server_name: ' + str(server_name))
        serial_array = request.form.getlist('serial_number')
        file_name_array = request.form.getlist('file_name_text')
        type_array = request.form.getlist('type_text')
        url_array = request.form.getlist('url_text')
        # 包裝取得要 post 的參數
        data_json = ut.Utils.get_upgrade_json(serial_array, file_name_array, type_array, url_array)
        # 透過 server_name 取得 server domain
        host_url = model.get_host_url_by_server_name(server_name)
        resp = helper_api.server_apk_upgrade(data_json, host_url)
        print('resp: ' + str(resp))
    return render_template(
        'server_api.html',
        form_server_update_apk=form_server_update_apk,
        server_name=server_name,
        update_resp=resp)

# device_log 頁面
@app.route('/device_log', methods=['GET'])
def device_log():
    server_name = request.args.get('server_name')
    serial_no = request.args.get('serial_no')
    host_url = request.args.get('host_url')
#     host_info = model.get_host_info_by_server_name(server_name)
    host_info = {
        'server_name':server_name, 
        'serial_no':serial_no,
        'host_url':host_url}
    print(host_info)
    resp = helper_api.query_device_logs(host_info)
    return render_template(
        'device_log.html',
        serial_no=serial_no,
        server_name=server_name,
        host_url=host_url,
        device_logs=resp)

# device_api 頁面
@app.route('/device_api', methods=['GET'])
def device_api():
    print("device_api")
    server_name = request.args.get('server_name')
    serial_no = request.args.get('serial_no')
    host_url = request.args.get('host_url')
    print('server_name: ' + str(server_name))
    print('serial_no: ' + str(serial_no))
    print('host_url: ' + str(host_url))
    form_device_config = FormDeviceConfig()
    form_device_restart = FormDeviceRestart()
    return render_template(
        'device_api.html',
        form_device_config=form_device_config,
        form_device_restart=form_device_restart,
        server_name=server_name,
        serial_no=serial_no,
        host_url=host_url)

# 呼叫更新手機 config api
@app.route('/device_config_update', methods=['POST'])
def device_config_update():
    print("device_confing")
    form_device_config = FormDeviceConfig()
    form_device_restart = FormDeviceRestart()
    if request.method == 'POST':
        phone = request.form.get('phone_number')
        host_url = request.form.get('host_url')
        serial_no = request.form.get('serial_number')
        print('phone: ' + str(phone))
        print('host_url: ' + str(host_url))
        print('serial_no: ' + str(serial_no))
        update_resp = helper_api.device_config_update(serial_no, phone, host_url)
        print(update_resp)
        return render_template(
            'device_api.html',
            form_device_config=form_device_config,
            form_device_restart=form_device_restart,
            serial_no=serial_no,
            host_url=host_url,
            update_resp=update_resp)

# 呼叫重啟手機 api
@app.route('/device_restart', methods=['POST'])
def device_restart():
    print("device_restart")
    form_device_config = FormDeviceConfig()
    form_device_restart = FormDeviceRestart()
    if request.method == 'POST':
        serial_no = request.form.get('serial_number')
        redo_job = request.form.get('redo_job')
        host_url = request.form.get('host_url')
        print('serial_no: ' + str(serial_no))
        print('redo_job: ' + str(redo_job))
        restart_resp = helper_api.device_restart(serial_no, redo_job, host_url)
        print(restart_resp)
        return render_template(
            'device_api.html',
            form_device_config=form_device_config,
            form_device_restart=form_device_restart,
            serial_no=serial_no,
            host_url=host_url,
            restart_resp=restart_resp)

if __name__ == '__main__':
    app.run(debug=True)