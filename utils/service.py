import re, os, sys, signal
import time
import json
import requests # pip install requests
import threading
from setting.settings import LIMIT_PING_TIME
from utils.DateTime import DateTime
import subprocess # pip install subprocess.run
from DAL.eventDAL import EventMonitorDAL


# Exit statuses recognized by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

def _runcmd(cmd, input=None):
    if input is not None:
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             close_fds=True, preexec_fn=os.setsid)
    else:
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             close_fds=True, preexec_fn=os.setsid)

    stdoutdata, stderrdata = p.communicate(input)
    return p.returncode, stderrdata, stdoutdata


"""
Data instant event_json_object
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
class Service:
    def __init__(self, event_json_object):
        self.my_event = event_json_object

    def get_alert_status(self, status):
        if status == 0:
            return 'OK'
        elif status == 1:
            return 'WARNING'
        elif status == 2:
            return 'CRITICAL'
        elif status == 3:
            return 'UNKNOWN'
        else:
            return 'NoStatus'

    def ping_host(self):
        message = ''
        if not self.my_event["ip_monitor"]:
            return UNKNOWN, message
        cmd = "ping -c 1 -w %d %s"%(LIMIT_PING_TIME, self.my_event["ip_monitor"])
        #and then check the response...
        returncode, stderrdata, stdoutdata = _runcmd(cmd = cmd)
        message = stdoutdata
        if returncode == 0:
            message = 'OK'
            return OK, message
        return CRITICAL, message

    def push_notification(self, now, ishost, AlertStatus, msg):
        args = []
        date_time = DateTime()
        args.append({
            'ishost'            : ishost,
            'queueServiceName'  : self.my_event["service_check_name"],
            'settingTime'       : now,
            'queueHost'         : self.my_event["encoder"] + '-' + self.my_event["event_name"], 
            'msg'               : msg,
            'AlertStatus'       : AlertStatus
            })
        data = json.dumps(args)
        print data
        return 0

    def update_status(self, status):
        event_monitor = EventMonitorDAL()
        date_time = DateTime()
        now = date_time.get_now()
        data = {"status": int(status), "last_update": now}
        rsp = event_monitor.put(self.my_event["id"], data)


    '''
    Check ping
    change: return 1
    notchange: return 0
    '''
    def check_ping(self):
        status = 0
        msg = ''
        ishost = 'true'
        check = self.ping_host()
        status = check[0]
        msg = check[1]
        print msg
        if status != self.my_event["status"]:
            self.my_event["status"] = status
            AlertStatus = self.get_alert_status(status)
            msg = "%s - %s"%(AlertStatus, msg)
            date_time = DateTime()
            now = date_time.get_now_as_human_creadeble()
            self.push_notification(now, ishost, AlertStatus, msg)
            self.update_status(status)
            return 1
        return 0

    def check_source(self):
        print 'hahaha'
        return 0
