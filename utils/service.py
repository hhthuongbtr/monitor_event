import re, os, sys, signal
import time
import json
import requests # pip install requests
import threading
from setting.settings import LIMIT_PING_TIME
from setting.DateTime import DateTime
import subprocess # pip install subprocess.run


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

class Service:
    def __init__(self,event_check_id, event_name, start_date, end_date, encoder, service_check_id, service_check_name, ip_monitor, source_main, source_backup, status):
        self.event_check_id = event_check_id
        self.event_name = event_name
        self.start_date = start_date
        self.end_date = end_date
        self.encoder_name = encoder
        self.service_check_id = service_check_id
        self.service_check_name = service_check_name
        self.ip_monitor = ip_monitor
        self.source_main = source_main
        self.source_backup = source_backup
        self.status = status

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
        if not self.ip_monitor:
            return UNKNOWN, message
        cmd = "ping -c 1 -w %d %s"%(LIMIT_PING_TIME, self.ip_monitor)
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
            'queueServiceName'  : self.service_check_name,
            'settingTime'       : now,
            'queueHost'         : self.encoder_name + '-' + self.event_name, 
            'msg'               : msg,
            'AlertStatus'       : AlertStatus
            })
        data = json.dumps(args)
        print data
        return 0

    '''
    Check ping
    '''
    def check_ping(self):
        status = 0
        msg = ''
        ishost = 'true'
        check = self.ping_host()
        status = check[0]
        msg = check[1]
        #If change status
        if status != self.status:
            date_time = DateTime()
            now = date_time.get_now_as_human_creadeble()
            #Recheck status again.
            time.sleep(2)
            recheck = self.ping_host()
            restatus = recheck[0]
            #if status is still change, update database
            if status == restatus:
                self.status = status
                AlertStatus = self.get_alert_status(status)
                msg = "%s - %s"%(AlertStatus, msg)
                self.push_notification(now, ishost, AlertStatus, msg)
        return 0

    def check_source(self):
        print 'hahaha'
        return 0
