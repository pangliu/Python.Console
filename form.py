from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import Required, Email

class FormDeviceConfig(Form):
    serial_number = TextField(u'serial no', validators=[Required()])
    phone_number = TextField(u'phone number', validators=[Required()])
    host_url = TextField(u'host_url', validators=[Required()])
    submit = SubmitField(u'POST')

class FormDeviceRestart(Form):
    serial_number = TextField(u'serial no', validators=[Required()])
    redo_job = TextField(u'redo_job', validators=[Required()])
    host_url = TextField(u'host_url', validators=[Required()])
    restart_submit = SubmitField(u'POST')

class FormDeviceApkUpgrade(Form):
    server_name = TextField(u'server_name', validators=[Required()])
    serial_number = TextField(u'serial_no', validators=[Required()])
    file_name_text = TextField(u'file_name', validators=[Required()])
    type_text = TextField(u'type', validators=[Required()])
    url_text = TextField(u'url', validators=[Required()])
    upgrade_submit = SubmitField(u'POST')