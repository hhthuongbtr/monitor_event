import requests # pip install requests
import json
from requests.exceptions import ConnectionError
from utils.DateTime import DateTime

class ApiUrl:
    def __init__(self):
        self.url = "http://10.0.0.205:8000/event/"
        self.monitor = self.url + "monitor/"
        self.running = self.url + "running/"
        self.waiting = self.url + "waiting/"
        self.completed = self.url + "completed/"
        self.event_monitor = self.url + "event_monitor/"

    def get(self, url):
        try:
            rsp = requests.get(url, timeout=2)
        except ConnectionError as e:
            return e
        if rsp.status_code == 200:
            return rsp.text
        elif rsp.status_code == 502:
            return "Bad gateway. Check your proxy or wweb services"
        else:
            return "Unknow"

    def put(self, url, data):
        rsp = requests.put(url, json = data, timeout = 2)
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
    def put(self, pk, data):
        api_url = ApiUrl()
        url = api_url.event_monitor + str(pk) + "/"
        rsp = api_url.put(url, data)
        return rsp

    def get(self, pk=None):
        api_url = ApiUrl()
        if pk:
            url = api_url.event_monitor + str(pk) + "/"
        else:
            url = api_url.event_monitor
        rsp = api_url.get(url)
        return rsp

