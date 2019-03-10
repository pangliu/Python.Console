from flask import Flask, render_template, Blueprint, url_for, request
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_bootstrap import Bootstrap
from flask import json
import ut
import api_helper
from form import FormDeviceConfig, FromDeviceRestart

app = Flask(__name__)
# app.config.from_pyfile('devkey')

app.config["SECRET_KEY"] = "12345678"
Bootstrap(app)
nav = Nav(app)

nav.register_element('my_navbar', Navbar(
    'pythonConsole',
    View('Home page', '.index')))

@app.route('/')
def index():
    # resp = api_helper.device_config_update('NE1GAM4812612355', '13699412081')
    # print(resp)
    return render_template('index.html', hosts=ut.Utils.get_json_file('./utils/index.json'))

@app.route('/server_log/<serverName>/')
def server_log(serverName):
    return render_template(
        'server_log.html',
        serverName=serverName,
        apiLogs=ut.Utils.get_json_file('./utils/api_log.json'))

@app.route('/device_log/<serianlNo>')
def device_log(serianlNo):
    return render_template(
        'device_log.html',
        serianlNo=serianlNo,
        deviceLogs=ut.Utils.get_json_file('./utils/device_log.json'))


# @app.route('/device_api/<serianlNo>')
# def device_api(serianlNo):
#     print('serianlNo')
#     print(serianlNo)
#     return render_template('device_api.html', serianlNo=serianlNo, deviceLogs=ut.Utils.get_json_file('./utils/device_log.json'))

# @app.route('/device_config_update', methods=['GET', 'POST'])
# def device_config_update():
#     result = request.form1
#     print('device_config_update: ' + result)
#     serianlNo = "aaaaaa"
#     return render_template('device_api.html', serianlNo=serianlNo, deviceLogs=ut.Utils.get_json_file('./utils/device_log.json'))

@app.route('/device_api/<serianl_no>', methods=['GET', 'POST'])
def device_api(serianl_no):
    print("device_api")
    form_device_config = FormDeviceConfig()
    form_device_restart = FromDeviceRestart()
    return render_template(
        'device_api.html',
        form_device_config=form_device_config,
        form_device_restart=form_device_restart,
        serianl_no=serianl_no)

# 呼叫更新手機 config api
@app.route('/device_config_update', methods=['POST'])
def device_config_update():
    print("device_confing")
    form_device_config = FormDeviceConfig()
    form_device_restart = FromDeviceRestart()
    if request.method == 'POST':
        phone = request.form.get('phone_number')
        serianl_no = request.form.get('serial_number')
        print('phone: ' + phone)
        print('serianl_no: ' + serianl_no)
        update_resp = api_helper.device_config_update(serianl_no, phone)
        print(update_resp)
        return render_template(
            'device_api.html',
            form_device_config=form_device_config,
            form_device_restart=form_device_restart,
            serianl_no=serianl_no,
            update_resp=update_resp)

# 呼叫重啟手機 api
@app.route('/device_restart', methods=['POST'])
def device_restart():
    print("device_restart")
    form_device_config = FormDeviceConfig()
    form_device_restart = FromDeviceRestart()
    if request.method == 'POST':
        serianl_no = request.form.get('serial_number')
        redo_job = request.form.get('redo_job')
        print('serianl_no: ' + str(serianl_no))
        print('redo_job: ' + str(redo_job))
        restart_resp = api_helper.device_restart(serianl_no, redo_job)
        print(restart_resp)
        return render_template(
            'device_api.html',
            form_device_config=form_device_config,
            form_device_restart=form_device_restart,
            serianl_no=serianl_no,
            restart_resp=restart_resp)

if __name__ == '__main__':
    app.run(debug=True)