from elasticsearch import Elasticsearch
from elasticsearch import ElasticsearchException
import configparser
import json
def readconfig():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

def connect_elastic():
    global es
    es = Elasticsearch(config['elastic']['host'])

def upload_scapy():
    with open('../scapy_logs.json','r') as logs:
        scapy_logs = logs.readlines()
    for record in scapy_logs:
        es.index(index = config['elastic']['scapy_index'], body = record)

def upload_sysmon():
    with open('sysmon_logs.json','r') as logs:
        sysmon_logs = logs.readlines()
    for record in sysmon_logs:
        es.index(index = config['elastic']['sysmon_index'], body = record)
    return

if __name__ == '__main__':
    readconfig()
    try:
        connect_elastic()
        upload_scapy()
        upload_sysmon()
    except ElasticsearchException as err:
        print('Error occured: '+str(err))