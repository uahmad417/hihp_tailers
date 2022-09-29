import json
import xmltodict
import Evtx.Evtx as evtx
import configparser

def readconfig():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

def evtx_to_json():
    with evtx.Evtx(config['sysmon']['path']) as open_logs:
        events = list(open_logs.records())
        count = len(events)
        for record in events:
            json_log = json.loads(json.dumps(xmltodict.parse(record.xml())))
            event_data = json_log['Event']['EventData']['Data']
            for attribute in event_data:
                attribute[attribute.pop('@Name')] = attribute.pop('#text')
            with open('sysmon_logs.json','a') as sysmon_logs:
                sysmon_logs.write(json.dumps(json_log)+'\n')

if __name__ == '__main__':
    readconfig()
    evtx_to_json()