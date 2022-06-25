from concurrent.futures import thread
from threading import Lock
import threading

import bluetooth
from asyncio import subprocess
from subprocess import call
import subprocess
import sys

class myBluetooth:
    def __init__(self):
        self.client_sock = None
        self.server_sock = None
        self.mutex = threading.Lock()

    def __del__(self):
        try:
            self.client_sock.close()
        except:
            pass
        try:
            self.server_sock.close()
        except:
            pass
        print("")
        print("Bluetooth Shutdown")
        print("-"*100)
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(myBluetooth, cls).__new__(cls)
        return cls.instance

    def startServer(self):
        '''
        Start bluetooth server. 
        take care it is a blocking method till connection occur
        '''
        # check bluetooth is not blocked
        #subprocess.run(['sudo', 'rfkill', 'unblock', 'all'])
        #subprocess.run(['sudo', 'hciconfig', 'hci0', 'reset'])
       

        try:
             # make bluetooth discoverable
            subprocess.run(['sudo', 'hciconfig', 'hci0', 'piscan'])
            
            self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_sock.bind(("", bluetooth.PORT_ANY))

            self.server_sock.listen(1)

            port = self.server_sock.getsockname()[1]

            uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"

            bluetooth.advertise_service(self.server_sock, "rpiBluetoothServer", service_id=uuid,
                                        service_classes=[
                                            uuid, bluetooth.SERIAL_PORT_CLASS],
                                        profiles=[bluetooth.SERIAL_PORT_PROFILE]
                                        )
            print("-"*100)                           
            print("Waiting for connection on RFCOMM channel", port)
            self.client_sock, client_info = self.server_sock.accept()
            print("Accepted connection from", client_info)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            raise("start server Exception: "+str(e))    
    def send(self, bytes):
        try:
            if self.client_sock != None:
                self.mutex.acquire()
                self.client_sock.send(bytes)
                self.mutex.release()
            else:
                print("Bluetooth send method error" )
                print("check that you started the server before using this method")  
                raise (BluetoothException("Client Socket Null Exception"))
        except IOError as e:
            self.mutex.release()
            raise (BluetoothIOError("send method: IOError: "+str(e)))
        except BaseException as e:
            self.mutex.release()
            raise (BluetoothException("send method: exception: "+str(e)))


    data = None
    def getData(self):
        return self.data

    def receive(self):
        try:
            if self.client_sock != None:
                self.mutex.acquire()
                rec_data = self.client_sock.recv(1024)
                self.mutex.release()
                self.data = rec_data
            else:
                print("Bluetooth receive method return None!!!!\n \
                check you started server before use this method")
                print( BluetoothException("receive: Client Socket Null Exception"))
        except Exception as e:
            self.mutex.release()
            print()
            raise( BluetoothException("receive method: exception: "+ str(e)))
        except IOError as e:
            self.mutex.release()
            print()
            raise (BluetoothIOError("receive method: exception: "+ str(e)))

class BluetoothException(Exception):
    pass
class BluetoothIOError(IOError):
    pass