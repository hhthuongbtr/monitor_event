import time
import threading
from setting.MySQL_Database import Database
from setting.settings import DATA_EXPIRE_TIME
from setting.DateTime import DateTime
from utils.service import Service

'''
1 = check_ping
2 = check_source
'''
if __name__ == "__main__":
    rows = None
    try:
        mdb = Database()
        rows = mdb.execute_query("select * from event_monitor_service")
    except Exception as e:
        raise ValueError(e)
    date_time = DateTime()
    now = date_time.get_now()
    expire_time = now + DATA_EXPIRE_TIME * 60
    if rows:
        while expire_time > now:
            for row in rows:
                event_check_id = row[0]
                event_name = row[1]
                start_date = row[2]
                end_date = row[3]
                encoder = row[4]
                service_check_id = row[5]
                service_check_name = row[6]
                ip_monitor = row[7]
                source_main = row[8]
                source_backup = row[9]
                status = row[10]
                if (now >= start_date) and (now <= end_date):
                    #print start_date
                    #print now
                    #print end_date
                    list_t=[]
                    service_check = Service(event_check_id, event_name, start_date, end_date, encoder, service_check_id, service_check_name, ip_monitor, source_main, source_backup, status)
                    if service_check_id == 1:
                        t = threading.Thread(target=service_check.check_ping)
                        list_t.append(t)
                        t.start()
                    elif service_check_id == 2:
                        t = threading.Thread(target=service_check.check_source)
                        list_t.append(t)
                        t.start()
                    '''wait for list job finish'''
                    for t in list_t:
                        t.join()
                 #End for loo
            time.sleep(1)
            now = date_time.get_now()
        #End while
    else:
        time.sleep(60)
    time.sleep(1)

