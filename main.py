import json
import time
import os
import threading
from setting.settings import DATA_EXPIRE_TIME
from utils.DateTime import DateTime
from utils.service import Service
from BLL.eventBLL import EventBLL
from DAL.eventDAL import EventMonitorDAL

"""
1 = check_ping
2 = check_source
[
    {
        status: null,
        end_date: "1513275458",
        event_name: "EDM 17/12",
        pid: null,
        ip_monitor: "10.0.216.216",
        encoder: "Ateme",
        service_check_name: "check_ping",
        source_backup: "225.1.5.138:30120",
        source_main: "225.1.5.136:30120",
        active: 1,
        id: 1,
        service_check_id: 1,
        last_update: "1512716188",
        start_date: "1513129949"
    } 
]

"""
class Handle:
    def __init__(self, event_json_object):
        self.my_event = event_json_object

    def update_data(self):
        event = EventBLL()
        data = event.get_event_monitor(self.my_event['id'])
        if is_json(data):
            data = json.loads(data)
            if len(data):
                data = data['monitor'][0]
                self.my_event = data
            else:
                event_monitor = EventMonitorDAL()
                json_data = {"pid": 0}
                rsp = event_monitor.put(self.my_event["id"], json_data)
                time.sleep(2)
                raise ValueError(data)
        else:
            event_monitor = EventMonitorDAL()
            json_data = {"pid": 0}
            rsp = event_monitor.put(self.my_event["id"], json_data)
            time.sleep(2)
            raise ValueError(data)
        

    def service_check(self):
        pid = os.getpid()
        event_monitor = EventMonitorDAL()
        self.my_event["pid"] = int(pid)
        data = {"pid": int(pid)}
        rsp = event_monitor.put(self.my_event["id"], data)
        date_time = DateTime()
        now = date_time.get_now()
        #print str(now) + " >= " + str(self.my_event["start_date"]) + " and " + str(now) + " <= " + str(self.my_event["end_date"])
        while (now >= int(self.my_event["start_date"]) and now <= int(self.my_event["end_date"]) and self.my_event['active']):
            change = None
            data_expire_time = now + DATA_EXPIRE_TIME * 60
            service_check = Service(self.my_event)
            if self.my_event['service_check_id'] == 1:
                while data_expire_time > now:
                    change = service_check.check_ping()
                    time.sleep(1)
                    now = date_time.get_now()
                    """Waiting update data to server and reload data"""
                    if change:
                        time.sleep(1)
                        break
            elif self.my_event['service_check_id'] == 2:
                while data_expire_time > now:
                    change = service_check.check_source()
                    time.sleep(1)
                    now = date_time.get_now()
                    """Waiting update data to server and reload data"""
                    if change:
                        time.sleep(1)
                        break
            now = date_time.get_now()
            self.update_data()
        #Up date PID affter expire time
        json_data = {"pid": 0}
        rsp = event_monitor.put(self.my_event["id"], json_data)
        return 0

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except:
        return False
    return True

if __name__ == "__main__":
    try:
        '''
        get list event from api
        '''
        event = EventBLL()
        event_running_list = event.get_running_event_monitor_list()
    except Exception as e:
        time.sleep(30)
        raise ValueError(e)
    if is_json(event_running_list):
        '''
        Decode event as json fortmat
        if data not as json fortmat: sleep 60s and raise error
        '''
        event_running_list = json.loads(event_running_list)
        now = event_running_list['now']
        event_running_list = event_running_list['monitor_running_list']
        flag = False
        for event_running in event_running_list:
            if (not event_running["pid"]) or (now >= (int(event_running["last_update"]) + 300)):
                handle = Handle(event_running)
                handle.service_check()
                flag = True
                break
        if flag:
            time.sleep(1)
        else:
            time.sleep(60)
    else:    
        print "Bug: load data " + str(event_running_list)
        time.sleep(60)