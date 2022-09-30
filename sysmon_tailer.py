import json
from threading import local
import xmltodict
import Evtx.Evtx as evtx
import configparser
from datetime import datetime
from dateutil import tz

def readconfig():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

def evtx_to_json():
    local_tz = tz.tzlocal()
    utc_tz = tz.tz.gettz('UTC')
    with evtx.Evtx(config['sysmon']['path']) as open_logs:
        events = list(open_logs.records())
        count = len(events)
        for record in events:
            json_log = json.loads(json.dumps(xmltodict.parse(record.xml())))
            event_data = json_log['Event']['EventData']['Data']
            for attribute in event_data:
                if attribute['@Name'] == 'UtcTime':
                    utc_timestamp = datetime.strptime(attribute['#text'],'%Y-%m-%d %H:%M:%S.%f')
                    utc_timestamp = utc_timestamp.replace(tzinfo=utc_tz)
                    local_timestamp = utc_timestamp.astimezone(local_tz)
                    local_timestamp = local_timestamp.replace(tzinfo=None)
                    attribute['#text'] = str(local_timestamp)
                attribute[attribute.pop('@Name')] = attribute.pop('#text')
            with open('sysmon_logs.json','a') as sysmon_logs:
                sysmon_logs.write(json.dumps(json_log)+'\n')

if __name__ == '__main__':
    readconfig()
    evtx_to_json()