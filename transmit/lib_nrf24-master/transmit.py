import argparse
from datetime import datetime
from multiprocessing.reduction import recv_handle
from optparse import Values
import struct
import sys
import time
import traceback
import json
from typing import Type
import pigpio
from nrf24 import *

_init_float = float(-1)

class transmit:
    global parser, args, hostname, port, address , pi
   
   
    def __init__(self):
        self.rec_values = None
        self.TX_ADDR = "ADDR0"
        self.RX_ADDR = "1SNSR" 
        # float(_long_)}, {float(_lat_)}, {_velocity_},  {_acc_}, {_heading_}
        self._send_dict_prev = {"longitude":_init_float,"latitude":_init_float,"velocity":_init_float,"acceleration":_init_float,"heading":_init_float}
        self.send_dict = {"longitude":_init_float,"latitude":_init_float,"velocity":_init_float,"acceleration":_init_float,"heading":_init_float}
        #
        # A simple NRF24L receiver that connects to a PIGPIO instance on a hostname and port, default "localhost" and 8888, and
        # starts receiving data on the address specified.  Use the companion program "simple-sender.py" to send data to it from
        # a different Raspberry Pi.
        #
        #print("Python NRF24 Simple Receiver Example.")
        
        # Parse command line argument.
        self.parser = argparse.ArgumentParser(prog="simple-receiver.py", description="Simple NRF24 Receiver Example.")
        self.parser.add_argument('-n', '--hostname', type=str, default='localhost', help="Hostname for the Raspberry running the pigpio daemon.")
        self.parser.add_argument('-p', '--port', type=int, default=8888, help="Port number of the pigpio daemon.")
        self.parser.add_argument('address', type=str, nargs='?', default='1SNSR', help="Address to listen to (3 to 5 ASCII characters)")

        self.args = self.parser.parse_args()
        self.hostname = self.args.hostname
        self.port = self.args.port
        self.address = self.TX_ADDR

        # Verify that address is between 3 and 5 characters.
        if not (2 < len(self.address) < 6):
            print(f'Invalid address {self.address}. Addresses must be between 3 and 5 ASCII characters.')
            sys.exit(1)
        
        # Connect to pigpiod
        # print(f'Connecting to GPIO daemon on {self.hostname}:{self.port} ...')
        self.pi = pigpio.pi(self.hostname, self.port)
        if not self.pi.connected:
            print("Not connected to Raspberry Pi ... goodbye.")
            sys.exit()

        # Create NRF24 object.
        # PLEASE NOTE: PA level is set to MIN, because test sender/receivers are often close to each other, and then MIN works better.
        self.nrf = NRF24(self.pi, ce=25, payload_size=RF24_PAYLOAD.DYNAMIC, channel=100, data_rate=RF24_DATA_RATE.RATE_2MBPS, pa_level=RF24_PA.MIN)
        self.nrf.set_address_bytes(len(self.address))
        self.nrf.set_retransmission(0,0)
        
        # Listen on the address specified as parameter
        self.nrf.open_reading_pipe(RF24_RX_ADDR.P0, self.RX_ADDR)
        
        # Display the content of NRF24L01 device registers.
        # self.nrf.show_registers()
    
    def _is_data_changed(self):
        for key in self.send_dict:
            if self.send_dict[key] != self._send_dict_prev[key]:
                return True
        return False
    def _sync_prev_dict(self):
        for key in self.send_dict:
            self._send_dict_prev[key] = self.send_dict[key] 

    def _copy_dicts(self,src:dict,dst:dict ):
        for k in src:
            dst[k] = src [k]

    def set_data_dict(self,dict:dict):
        self._copy_dicts(dict,self.send_dict)
####sending function####
    def send_func(self):
        while True:
            #sending data
            self.nrf.open_writing_pipe(self.TX_ADDR)
            try:

                if self._is_data_changed():
                    print(f"\u001b[38;2;255;255;0msending:{self.send_dict['longitude']}, {self.send_dict['latitude']}, {self.send_dict['velocity']}, {self.send_dict['acceleration']}, {self.send_dict['heading']}\u001b[0m") 
                    payload = struct.pack("<fffff", float(self.send_dict['longitude']), float(self.send_dict['latitude']), self.send_dict['velocity'], self.send_dict['acceleration'], self.send_dict['heading']) 
                    # Send the payload to the address specified above.
                    self.nrf.reset_packages_lost()
                    self.nrf.send(payload)
                    
                    self._sync_prev_dict()
                    try:
                        self.nrf.wait_until_sent()
                    except TimeoutError:
                        print('Timeout waiting for transmission to complete.')

                    if self.nrf.get_packages_lost() == 0:
                        print(f"\u001b[38;2;0;255;0mSuccess: lost={self.nrf.get_packages_lost()}, retries={self.nrf.get_retries()}\u001b[0m")
                    else:
                        print(f"\u001b[38;2;255;0;0mError: lost={self.nrf.get_packages_lost()}, retries={self.nrf.get_retries()}\u001b[0m")
                    print("-"*90)

            except:
                traceback.print_exc()
                self.nrf.power_down()
                self.pi.stop()
        
    
    rec_values = None
    def get_values(self):
        return self.rec_values

    def set_values(self,var):
        self.rec_values=var

        
    ####recieving function####
    def rec_func(self):
            # Enter a loop receiving data on the address specified.
        try:
            # print(f'Receive from {self.address}')
            count = 0
            while True:
                self.nrf.open_reading_pipe(RF24_RX_ADDR.P0, self.RX_ADDR)
                # As long as data is ready for processing, process it.
                while self.nrf.data_ready():
                    # Count message and record time of reception.            
                    count += 1
                    now = datetime.now()
                    
                    # Read pipe and payload for message.
                    pipe = self.nrf.data_pipe()
                    payload = self.nrf.get_payload()    

                    # Resolve protocol number.
                    protocol = payload[0] if len(payload) > 0 else -1            

                    hex = ':'.join(f'{i:02x}' for i in payload)

                    # Show message received as hex.
                    # print(f"{now:%Y-%m-%d %H:%M:%S.%f}: pipe: {pipe}, len: {len(payload)}, bytes: {hex}, count: {count}")

                    # If the length of the message is 9 bytes and the first byte is 0x01, then we try to interpret the bytes
                    # sent as an example message holding a temperature and humidity sent from the "simple-sender.py" program.
                  
                    values = struct.unpack("<fffff", payload)
                    #print(f'Protocol: {values[0]}, temperature: {values[1]}, humidity: {values[2]}')
                    print(f"\u001b[38;2;0;255;0mreceived values: {values}\u001b[0m")
                    self.set_values(values)
                    return values
                    
                
                # Sleep 100 ms.
                #time.sleep(0.1)
        except:
            traceback.print_exc()
            self.nrf.power_down()
            self.pi.stop()   
    

    