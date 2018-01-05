from DAL.eventDAL import EventDAL
from DAL.eventDAL import SccDAL
from DAL.eventDAL import EventMonitorDAL

class EventBLL:
    def __init__(self):
        self.event = EventDAL()

    def get_event_monitor_list(self):
        return self.event.get_event_monitor_list()

    def get_running_event_monitor_list(self):
        return self.event.get_running_event_monitor_list()

    def get_waiting_event_monitor_list(self):
        return self.event.get_waiting_event_monitor_list()

    def get_completed_event_monitor_list(self):
        return self.event.get_completed_event_monitor_list()

    def get_event_monitor(self, pk):
        return self.event.get_event_monitor(pk)

class EventMonitorBLL:
    def __init__(self):
        self.event_monitor = EventMonitorDAL()

    def put(self, pk, data):
        rsp = self.event_monitor.put(pk, data)
        return rsp

    def get(self, pk=None):
        if pk:
            rsp = self.event_monitor.get(pk)
        else:
            rsp = self.event_monitor.get()
        return rsp

class SccBLL:
    def __init__(self):
        self.scc = SccDAL()
    def post(self, data):
        return self.scc.post(data)
