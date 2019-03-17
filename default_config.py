# The default_config module automatically gets imported by Appconfig, if it
# exists. See https://pypi.python.org/pypi/flask-appconfig for details.

# Note: Don't *ever* do this in a real app. A secret key should not have a
#       default, rather the app should fail if it is missing. For the sample
#       application, one is provided for convenience.
SECRET_KEY = 'devkey'


class Config():
    # pc for python
    TAG_PC_NAME = 'python_host_log'  
    TAG_VERSION = '0.0.1'  # 20190212
    TAG_DEV = 1
    TAG_STAGE = 2
    TAG_ENORNMOMENT = TAG_STAGE

class ApiConfig():
    SIGN_KEY = '18luck'
    # DEVICE_CONFIG_UPDATE_URL = 'http://localhost:5021/deviceConfig'
    # DEVICE_RESTART_URL = 'http://localhost:5021/restartDevice'
    # HOST_INFO_URL = 'http://localhost:5021/hostInfo'
    # DEVICE_INFO_URL = 'http://localhost:5021/deviceInfo'
    # SERVER_APK_UPGRADE_URL = 'http://localhost:5021/upgrade'
    
    # 安裝 jenkins 主機的 domain
    ALL_DEVICE_INFO_URL = 'localhost:5000'

class SqlConfig():
    HOST = '127.0.0.1'
    ACCOUNT = 'root'
    PASSWORD = ''
    DB_NAME = Config.TAG_PC_NAME