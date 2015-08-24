import argparse
import math
import json
import os.path
import socket
import threading
import json

from pprint import pprint
from pythonosc import osc_message
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import osc_packet
from pprint import pprint
from time import sleep

server_ip = "127.0.0.1"
server_port = 8000

def send_message( address, message ):
    client = udp_client.UDPClient( server_ip, server_port )
#     msg = osc_message_builder.OscMessageBuilder(address=address)
    msg = osc_message_builder.OscMessageBuilder()
    msg.address = address
    msg.add_arg( message )
    client.send( msg.build() )
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000, help="The port the OSC server is listening on")
    args = parser.parse_args()
    
    server_ip = args.ip
    server_port = args.port

    switch = 0
    
    while True:
        if switch == 0:
            send_message( '/room1/lightswitch1', 'off' )
            switch = 1
        else:
            send_message( "/room1/lightswitch1", "on" )
            switch = 0
    
        sleep( 5 )
