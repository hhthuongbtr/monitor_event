from DAL.eventDAL import EventDAL

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