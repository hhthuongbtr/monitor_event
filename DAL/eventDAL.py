import requests # pip install requests
import json
from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
from utils.DateTime import DateTime
from setting import settings

class ApiUrl:
    def __init__(self):
        self.url = settings.URL_EVENT
        self.monitor = settings.URL_MONITOR
        self.running = settings.URL_RUNNING
        self.waiting = settings.URL_WAITING
        self.completed = settings.URL_COMPLETED
        self.event_monitor = settings.URL_EVENT_MONITOR
        self.scc = settings.URL_SCC

    def get(self, url):
        try:
            rsp = requests.get(url, auth=HTTPBasicAuth(settings.USER, settings.PASSWD), timeout=5)
        except ConnectionError as e:
            return e
        if rsp.status_code == 200:
            return rsp.text
        elif rsp.status_code >= 500:
            return "Check your proxy or web services"
        else:
            return rsp.status_code

    def put(self, url, data):
        try:
            rsp = requests.put(url, json = data, auth=HTTPBasicAuth(settings.USER, settings.PASSWD), timeout=5)
        except ConnectionError as e:
            return e
        if rsp.status_code == 202:
            return rsp.text
        elif rsp.status_code >= 500:
            return "Check your proxy or web services"
        else:
            return rsp.status_code

    def post(self, url, data):
        try:
            rsp = requests.post(url, json = data, auth=HTTPBasicAuth(settings.USER, settings.PASSWD), timeout=5)
        except ConnectionError as e:
            return e
        if rsp.status_code == 202:
            return rsp.text
        elif rsp.status_code >= 500:
            return "Check your proxy or web services"
        else:
            return rsp.status_code

class EventDAL:
    def __init__(self):
        self.api_url = ApiUrl()

    def get_event_monitor_list(self):
        return self.api_url.get(self.api_url.monitor)

    def get_running_event_monitor_list(self):
        return self.api_url.get(self.api_url.running)

    def get_waiting_event_monitor_list(self):
        return self.api_url.get(self.api_url.waiting)

    def get_completed_event_monitor_list(self):
        return self.api_url.get(self.api_url.completed)

    def get_event_monitor(self, pk):
        return self.api_url.get(self.api_url.monitor + str(pk) + "/")

class EventMonitorDAL:
    def __init__(self):
        self.api_url = ApiUrl()

    def put(self, pk, data):
        url = self.api_url.event_monitor + str(pk) + "/"
        rsp = self.api_url.put(url, data)
        return rsp

    def get(self, pk=None):
        if pk:
            url = self.api_url.event_monitor + str(pk) + "/"
        else:
            url = self.api_url.event_monitor
        rsp = self.api_url.get(url)
        return rsp

class SccDAL:
    def __init__(self):
        self.api_url = ApiUrl()

    def post(self, data):
        return self.api_url.post(self.api_url.scc, data)
        