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

destinations = {}

def check_rules( source, address, message ):
    for rule in config['rules']:
        if rule['match']['address'] == address and rule['match']['message'] == message:
            if DEBUG:
                print("Match for message rule [" + rule['match']['address'] + " : " + rule['match']['message'] + "], pushing message(s)")
            for client in rule['push']:
                send_message( client['destination'], client['address'], client['message'] )

def preload_destinations():
    for destination in config['destinations']:
        if not destination['name'] in destinations:
            if DEBUG:
                print( "Adding client [" + destination['name'] + "]: " + destination['address'] + ":" + str( destination['port'] ) )
            destinations[destination['name']] = udp_client.UDPClient( destination['address'], destination['port'] ) 

def send_message( osc_destination, osc_address, osc_message ):
    msg = osc_message_builder.OscMessageBuilder()
    msg.address = osc_address
    msg.add_arg( osc_message )
    msg = msg.build()
    try:
        destinations[osc_destination].send( msg )
    except Exception:
        print( "Failed to send msg for [" + osc_destination + ":" + osc_address + "]: " + osc_message )

class MyOSCHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        client_address = self.client_address[0]
        
        packet = osc_packet.OscPacket(data)
        for osc_msg in packet.messages:
            check_rules( client_address, osc_msg.message.address, osc_msg.message.params[0] )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=8000, help="The port to listen on")
    args = parser.parse_args()
    
    if not os.path.isfile('config.json'):
        die('Missing config file config.json')
    
    with open('config.json') as data_file:
        config = json.load(data_file)
    
    preload_destinations()
    
    if DEBUG:
        print( "Destinations:" )
        print( destinations.keys() )
    
    server = socketserver.UDPServer( ( args.ip, args.port ), MyOSCHandler )
    if DEBUG:
        print("Serving on {}".format(server.server_address))
    server.serve_forever()