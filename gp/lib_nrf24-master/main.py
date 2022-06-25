from simple_imu import imu
from transmit import transmit
from distance import Haversine_Formula
from threading import *
import time
from my_compass import heading
from my_gps import GPS
from btServer import myBluetooth
from bearing_angle import BearingAngle
import json
from TTC import TimeToCollision


def getFirstJson(jsons):
    # jsons = bt.receive()
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
    if flag2:
        return jsons[start_index:stop_index]  
    else:
        return None

def current_milli_time():
        return round(time.time() * 1000)

global rec_data

if __name__ == "__main__":
    trans = transmit()
    imu_data=imu()
    thread_imu=Thread(target=imu_data.velocity)
    thread_rec=Thread(target=trans.rec_func)
    thread_imu.start()
    # time.sleep(13)
    thread_rec.start()
    # gps = GPS()
    comp = heading()
    bt = myBluetooth()
    bt.startServer()
    bearing = BearingAngle()
    thread_bt_rec = Thread(target = bt.receive)
    bt_data = bt.getData()
    thread_bt_rec.start()
    ttc = TimeToCollision()
    while True:
        print(imu_data.getAccel())
        # coord = gps.get_coord()
        # trans.send_func(coord[0],coord[1],imu_data.getVelocity(),imu_data.getAccel(), comp.get_heading())
        message = {"myGps": str("lat: {}, lon: {}".format(30.0681095, 31.3190485)),
                       "speed": str(20), "myHeading": str(comp.get_heading())}
        js = json.dumps(message)
        # print(Haversine_Formula(lat1= float(coord[0]), lon1 = float(coord[1]), lat2 = 30.0681095, lon2 = 31.3190485))
        # print("__________________________________________________")
        # print("lat: {} , lon: {}".format(float(coord[0]), float(coord[1])))
        bt.send(js)
        bt_rec_data=None
        if(not(thread_bt_rec.is_alive())):
            bt_data = getFirstJson(bt.getData())
            # print(bt_data)
            bt_rec_data = json.loads(bt_data)
            if("mLat" in  bt_rec_data and "mLon" in bt_rec_data):
                trans.send_func(float(bt_rec_data["mLat"]),float(bt_rec_data["mLon"]),float(bt_rec_data["mSpeed"]),imu_data.getAccel(), comp.get_heading())

            thread_bt_rec = Thread(target = bt.receive)
            thread_bt_rec.start()
        

        if("mLat" in  bt_rec_data and "mLon" in bt_rec_data):   
            if(not(thread_rec.is_alive())):
                rec_data = trans.get_values()
            
                # print("longitude: {} --- latitude: {} ".format(float(coord[1]),float(coord[0])))
                if(bt_rec_data != None):
                    lane = bearing.is_same_lane(this_lat = float(bt_rec_data["mLat"]),this_lon = float(bt_rec_data["mLon"]), this_heading = comp.get_heading() ,that_lon = rec_data[0],that_lat =  rec_data[1], that_heading = rec_data[4])
                # print("Heading1:{}    Heading2: {}".format(comp.get_heading(),rec_data[4]))
                # print("IS SAME LANE : {}".format(lane))
                # message = {"myGps": str("lat: {}, lon: {}".format(coord[0], coord[1])),
                #            "speed": str(imu_data.getVelocity()), "myHeading": str(comp.get_heading()),
                #             "otherGps": str("lat: {}, lon: {}".format(rec_data[0], rec_data[1])),
                #             "bearingAngle": str(bearing.getBearing()), "otherHeading": str(rec_data[4]) }
                # js = json.dumps(message)
                # bt.send(js)
                print(rec_data)
                print(ttc.warningLv(rec_data[2], 8, rec_data[3], 15))
                print(Haversine_Formula(lat1= rec_data[1], lon1 = rec_data[0], lat2 = float(bt_rec_data["mLat"]), lon2 = float(bt_rec_data["mLon"])))
                thread_rec = Thread(target=trans.rec_func)
                thread_rec.start()
