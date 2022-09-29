import http
from scapy.all import *
from scapy.layers.http import HTTPRequest
import json
from datetime import datetime
from time import strftime

def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        for key in http_data:
            http_data[key] = ''
        for header in http_data:
            if header == 'SourceIP':
                http_data['SourceIP'] = packet[IP].src
                continue
            if header == 'SourcePort':
                http_data['SourcePort'] = packet[IP].sport
                continue
            if header == 'UtcTime':
                http_data['UtcTime'] = str(datetime.now())
                break
            value = 'packet[HTTPRequest].'+header
            if eval(value) is not None:
                command = value+'.decode("utf-8")'
                http_data[header] = eval(command)
        if packet.haslayer(Raw):
            http_data['Payload'] = packet[Raw].load.decode()
        with open('scapy_logs.json','a') as scapy_logs:
            scapy_logs.write(json.dumps(http_data)+'\n')
        print(http_data)

if __name__ == '__main__':
    global http_data
    http_data = {'SourceIP': '','SourcePort': '', 'Method': '', 'Path': '', 'Http_Version': '' ,'Accept': '', 'Accept_Encoding': '', 'Accept_Language': '', 'Cache_Control': '',  'Connection':'', 'Content_Length': '','Content_Type': '', 'Cookie': '','Host':'', 'Origin': '', 'Referer': '', 'Upgrade_Insecure_Requests': '','User_Agent':'', 'UtcTime':''}
    sniff(iface='Wi-Fi',prn=process_packet)