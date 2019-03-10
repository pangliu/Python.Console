from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import Required, Email

class FormDeviceConfig(Form):
    serial_number = TextField(u'serial no', validators=[Required()])
    phone_number = TextField(u'phone number', validators=[Required()])
    submit = SubmitField(u'POST')

class FromDeviceRestart(Form):
    serial_number = TextField(u'serial no', validators=[Required()])
    redo_job = TextField(u'redo_job', validators=[Required()])
    restart_submit = SubmitField(u'POST')