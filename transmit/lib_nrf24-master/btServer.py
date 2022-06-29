import threading
import bluetooth
from asyncio import subprocess
from subprocess import call
import subprocess
import sys

class myBluetooth:
    '''
    #### Description:
    This is a singleton class that is using PyBluez, It is used to send data to mobile 
    app and receive data from it. It start server to listen for an RFCOMM connection
    from the mobile app to connect (Note: any device that use bluetooth and RFCOMM 
    and try to connect to this server will be accepted)
    #### Methods:
    - Blocking, and Non-Blocking receive
    - send 
    - Blocking start RFCOMM server listen method
    '''
    def __init__(self):
        self.client_sock = None
        self.server_sock = None
        self.mutex = threading.Lock()
        self.data = None
        self.receive_thread = None
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
        take care it is a blocking method till connection occurs
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
        '''
        The send method in normal case is not a blocking function, but if the other side
        are not reading what is sending and the sending buffer is overflowed, it will be blocked
        here untill the other side read the data. So make sure that the other side is reading
        '''
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


    def __receive(self):
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

    def receive_NonBlocking(self):
        # if the receive thread is None or not alive then make one and start it
        if(self.receive_thread == None or not self.receive_thread.is_alive()):
            self.receive_thread = threading.Thread(target=self.__receive)
            self.receive_thread.start()
        return self.data

    def receive_Blocking(self):
        self.__receive()
        return self.data


class BluetoothException(Exception):
    pass
class BluetoothIOError(IOError):
    pass