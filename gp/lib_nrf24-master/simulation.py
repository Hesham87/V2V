

import json
import threading
from time import sleep
import btServer
import sys 


def sender(time,limit,increment,cSock,kname):
   
        count = 0
        while True:
            try:
                if kname != "myGps" and kname != "otherGps": 
                    spd =  {
                        kname:count
                        }
                    js = json.dumps(spd)
                
                    cSock.send(js)
                else:
                    s = {kname:"lat={}, lon={}".format(count,count)}
                    cSock.send(json.dumps(s))    
                sleep(time)
                if count>limit:
                    count = 0
                else:
                    count = count + increment
                if count <0:
                    count = limit
            except KeyboardInterrupt:
                sys.exit()
            except btServer.BluetoothException as e:
                break    
            except btServer.BluetoothIOError as e:
                break    
        

if __name__=="__main__":
    while True:
        try:
            bt = btServer.myBluetooth()
            bt.startServer()
            speed_thread =threading.Thread(target=sender,args=(0.02,300,1,bt,"speed",))
            heading_thread =threading.Thread(target=sender,args=(0.1,360,1,bt,"myHeading",))    
            ttc_thread =threading.Thread(target=sender,args=(0.15,10,-0.2,bt,"ttc",))    
            speed_thread.start()
            heading_thread.start()
            ttc_thread.start()
            

            otherHeading_thread =threading.Thread(target=sender,args=(0.02,360,1,bt,"otherHeading",))
            myGps_thread =threading.Thread(target=sender,args=(0.1,10,0.1,bt,"myGps",))    
            otherGps_thread =threading.Thread(target=sender,args=(0.15,10,0.1,bt,"otherGps",))
            bearingAngle_thread =threading.Thread(target=sender,args=(0.156,360,1,bt,"bearingAngle",))      
            otherHeading_thread.start()
            myGps_thread.start()
            otherGps_thread.start()
            bearingAngle_thread.start()
            otherHeading_thread.join()
            myGps_thread.join()
            otherGps_thread.join()
            bearingAngle_thread.join()
            speed_thread.join()
            heading_thread.join()
            ttc_thread.join()
        except btServer.BluetoothIOError as e :
            print("Exception in main:",end=" ")
            print(e)
            del bt    
        except Exception as e :
            print("Exception in main:",end=" ")
            print(e)
            del bt
        

### You can send all the data in the same time
# if __name__=="__main__":
#     bt = btServer.myBluetooth()
#     bt.startServer()

#     spd =  {
#             "speed":"200" ,
#             "ttc":"5" ,
#             "myHeading":"50",
#             "otherHeading":"60",
#             "myGps":"lat:0.5, lon:0.3",
#             "otherGps":"lat:0.2, lon:0.5",
#             "bearingAngle":"220"
#             }
#     js = json.dumps(spd)
#     bt.send(js)