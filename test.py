import json
import requests
from DAL.eventDAL import EventMonitorDAL

evm = EventMonitorDAL()
data = {"pid": 222}
evm.put(1, data)
