from scapy.all import *
from scapy.layers.http import HTTPRequest
import json

def process_packet(packet):
    packet.haslayer(HTTPRequest)


if __name__ == '__main__':
    sniff(iface='Wi-Fi',prn=process_packet)