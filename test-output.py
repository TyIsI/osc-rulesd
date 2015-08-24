import argparse
import math
import json
import os.path
import socket
import threading
import socketserver
from pprint import pprint
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_packet

DEBUG = True

class MyOSCHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        client_address = self.client_address[0]
        
        packet = osc_packet.OscPacket(data)
        for osc_msg in packet.messages:
            print( "Received from [" + client_address + "/" + osc_msg.message.address + "]: '" + osc_msg.message.params[0] + "'" )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=9999, help="The port to listen on")
    args = parser.parse_args()
    
    server = socketserver.UDPServer( ( args.ip, args.port ), MyOSCHandler )
    print("Serving on {}".format(server.server_address))
    server.serve_forever()