#API
USER = 'monitor'
PASSWD = 'iptv13579'
REGION = 'HCM'
URL = 'http://10.0.200.99:8888/'
URL_EVENT = URL + 'event/'
URL_MONITOR = URL_EVENT + 'monitor/'
URL_RUNNING = URL_EVENT + REGION + '/running/'
URL_WAITING = URL_EVENT + REGION + '/waiting/'
URL_COMPLETED = URL_EVENT + REGION + '/completed/'
URL_EVENT_MONITOR = URL_EVENT + 'event_monitor/'
URL_SCC = 'http://10.0.200.99:8888/scc/'

#limit ping time
LIMIT_PING_TIME = 1
#Set time reload data (minutes)
DATA_EXPIRE_TIME = 0.5