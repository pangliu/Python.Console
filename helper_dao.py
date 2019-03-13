from datetime import datetime

TABLE_NAME = 'device_logs'
COLUMN_UUID = 'uuid'
COLUMN_SERIAL_NO = 'serial_no'
COLUMN_TASK_ID = 'task_id'
COLUMN_MISSION_TYPE = 'mission_type'
COLUMN_BANK_CODE = 'bank_code'
COLUMN_ADB_COMMAND = 'adb_command'
COLUMN_TEST_CASE_STATUS = 'test_case_status'
COLUMN_TEST_CASE_RESULT = 'test_case_result'
COLUMN_EXECUTE_TIME = 'execute_time'

def query_device_log_by_serial_no(db_connect, serial_no):
    """Query最新的一筆device log
    @serial_no : 手機的device id
    """
#     sql = ('SELECT * FROM device_logs WHERE serial_no = %s ORDER BY execute_time desc limit 1')
    sql = ('SELECT * FROM device_logs WHERE serial_no = %s LIMIT 10')
    cursor = db_connect.cursor()
    cursor.execute(sql, (serial_no,))
    log = None
    rows = cursor.fetchall()
    device_logs = []
    if rows is not None:
        for row in rows:
            date_time = datetime.strftime(row[8], '%Y-%m-%d %H:%M:%S')
            log = {
                    COLUMN_SERIAL_NO: row[1], 
                    COLUMN_TASK_ID: row[2],
                    COLUMN_MISSION_TYPE: row[3],
                    COLUMN_BANK_CODE: row[4],
                    COLUMN_ADB_COMMAND: row[5],
                    COLUMN_TEST_CASE_STATUS: row[6],
                    COLUMN_TEST_CASE_RESULT: row[7],
                    COLUMN_EXECUTE_TIME: date_time}
            device_logs.append(log)
#     print('log = {}'.format(log))
    cursor.close()
    return device_logs


