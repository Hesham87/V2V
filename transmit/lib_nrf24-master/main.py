from simple_imu import imu
from transmit import transmit
from distance import Haversine_Formula
from threading import *
import time
from btServer import myBluetooth
from bearing_angle import BearingAngle
import json
from TTC import TimeToCollision
import TTC
from data_manager import *
def getFirstJson(jsons):
    start_index = 0
    stop_index = 0
    size = len(jsons)
    begin_sign_int =  int.from_bytes(b'{', "big")
    end_sign_int =  int.from_bytes(b'}', "big")
    flag1=False
    flag2=False
    for i in range(0, size):
        c = jsons[i]
        if c == begin_sign_int:
            start_index = i
            flag1=True
        if c == end_sign_int and flag1:
            stop_index = i + 1
            flag2 = True
            break
        if c == 0:
            break
    if flag2:
        return jsons[start_index:stop_index]  
    else:
        return  "{\"empty\":\"empty\"}"

def current_milli_time():
        return round(time.time() * 1000)

global rec_data

if __name__ == "__main__":
    trans = transmit()
    imu_data=imu()
    thread_imu=Thread(target=imu_data.velocity)
    thread_rec=Thread(target=trans.rec_func)
    thread_imu.start()
    thread_rec.start()
    bt = myBluetooth()
    bt.startServer()
    ttc = TimeToCollision()
    bt_rec_data=None
    rec_data = None
    data_manager = DataManager()
    trans_send_thread = Thread(target=trans.send_func)
    startTime = imu_data.current_milli_time()
    i = 10
    ttc = 10
    inc = 0.3
    while True:
        bt_rec_data_bytes = bt.receive_NonBlocking()
            
        #### Check Tranceiver is receiving
        if(not(thread_rec.is_alive())):
                thread_rec = Thread(target=trans.rec_func)
                thread_rec.start()

        ### if we received from the bluetooth
        if bt_rec_data_bytes != None:
            bt_data = getFirstJson(bt_rec_data_bytes)
            bt_rec_data = json.loads(bt_data)
            #if( not(trans_send_thread.is_alive())):
                #trans_send_thread = Thread(target=trans.send_func )
                #trans_send_thread.start()
            if("mLat" in  bt_rec_data and "mLon" in bt_rec_data and "mSpeed" in bt_rec_data): 
                data_dict = {"longitude":float(bt_rec_data["mLon"]) ,\
                            "latitude":float(bt_rec_data["mLat"]), \
                            "velocity":float(bt_rec_data["mSpeed"]), \
                            "acceleration":imu_data.getAccel(), \
                            "heading":float(bt_rec_data["mHeading"]) }
              
                #trans.set_data_dict(data_manager.get_avg_data(data_dict))
                rec_data = trans.get_values()
                data_manager.update_data(data_manager.get_thresh_low_val(data_dict))
                data_dict = data_manager.get_avg_data(data_dict)
                    #print("received data = {}".format(rec_data))
                if rec_data != None:
                    distance = Haversine_Formula(lat1= rec_data[1], lon1 = rec_data[0], lat2 =data_dict["latitude"], lon2 = data_dict["longitude"])
                    #print("Haversine distance = {}".format(distance))
                
                    #if( float(bt_rec_data["mSpeed"])*3.6>1) : 
                    speed = float(data_dict["velocity"]) 
                        #else: 
                            #speed = 0
                    #warning = ttc.warningLv(rec_data[2],speed , rec_data[3], Haversine_Formula(lat1= rec_data[0], lon1 = rec_data[1], lat2 = float(bt_rec_data["mLat"]), lon2 = float(bt_rec_data["mLon"])))
                    #h_ttc = ttc.warningLv(rec_data[2],speed , rec_data[3], distance)
                    #a_ttc = TTC.get_myTTC(_distance=distance,_velocity = speed)
                    #warning = a_ttc
                    # message = {"ttc": warning, \
                    # "ttc_distance":distance,
                    # "ttc_a": a_ttc,
                    # "ttc_h":h_ttc,
                    # "speed_after": speed}
                    

                    #print(f"This data = {data_dict}")
                    #print(f"Warning TTC ={message}")
                        #print("H_TTC: {}".format(h_ttc))
                    # #print("A_TTC: {}".format(a_ttc))
                    # js = json.dumps(message)
                    # bt.send(js)