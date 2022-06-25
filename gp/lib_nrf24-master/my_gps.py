'''
GPS Interfacing with Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package

class GPS():
    def GPS_Info(self):
        self.nmea_time = []
        self.nmea_latitude = []
        self.nmea_longitude = []
        self.nmea_altitude = []
        self.nmea_time = self.NMEA_buff[0]                    #extract time from GPGGA string
        self.nmea_latitude = self.NMEA_buff[1]                #extract latitude from GPGGA string
        self.nmea_longitude = self.NMEA_buff[3]               #extract longitude from GPGGA string
        self.nmea_altitude = self.NMEA_buff[5]                #extract altitude from GPGGA string 
    
        
        

        
        lat = float(self.nmea_latitude)                  #convert string into float for calculation
        longi = float(self.nmea_longitude)               #convert string into float for calculation
        alti = float(self.nmea_altitude)                 #convert string into float for claculation

        
        self.lat_in_degrees = self.convert_to_degrees(lat)    #get latitude in degree decimal format
        self.long_in_degrees = self.convert_to_degrees(longi) #get longitude in degree decimal format
        self.alt_in_degrees = self.convert_to_degrees(alti)   #get altitude in degree decimal format


    # def GPS_Info():
    #     global NMEA_buff
    #     global lat_in_degrees
    #     global long_in_degrees
    #     global speed
    #     nmea_time = []
    #     nmea_latitude = []
    #     nmea_longitude = []
    #     nmea_altitude = []
    #     nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
    #     nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
    #     nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
    #     nmea_altitude = NMEA_buff[5]                #extract altitude from GPGGA string 
    
        
    #     print("NMEA Time: ", nmea_time,'\n')
    #     print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,"NMEA altitude:", nmea_altitude,'\n')
        

        
    #     lat = float(nmea_latitude)                  #convert string into float for calculation
    #     longi = float(nmea_longitude)               #convert string into float for calculation
    #     alti = float(nmea_altitude)                 #convert string into float for claculation

        
    #     lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
    #     long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
    #     alt_in_degrees = convert_to_degrees(alti)   #get altitude in degree decimal format

    # def GPS_velocity():
    #     global NMEA_buff_v
    #     nmea_speed = []
    #     nmea_speed = NMEA_buff_v[6]                 #extract speed from GPVTG string 

    #     print("NMEA speed ", nmea_speed, "\n")

        
    #convert raw NMEA string into degree decimal format   
    def convert_to_degrees(self, raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position
        


    gpgga_info = "$GPGGA,"
    gpvtg_info = "$GPVTG,"
    ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
    GPGGA_buffer = 0
    GPVTG_buffer = 0
    NMEA_buff = 0
    NMEA_buff_v = 0
    lat_in_degrees = 0
    long_in_degrees = 0
    alt_in_degrees = 0
    speed_in_km =0
    def get_coord(self):
        while True:
            try:
                received_data = (str)(self.ser.readline())                #read NMEA string received
                GPGGA_data_available = received_data.find(self.gpgga_info)   #check for NMEA GPGGA string
                if(GPGGA_data_available > 0):
                    self.GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
                    self.NMEA_buff = (self.GPGGA_buffer.split(','))               #store comma separated data in buffer
                    self.GPS_Info()                                          #get time, latitude, longitude
                    return (self.lat_in_degrees, self.long_in_degrees)
            except Exception:
                self.ser = serial.Serial ("/dev/ttyS0")
                continue



    # try:
    #     while True:
    #         received_data = (str)(ser.readline())                #read NMEA string received
    #         GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string
    #         GPVTG_data_available = received_data.find(gpvtg_info)   #check for NMEA GPVTG string  
    #         if (GPGGA_data_available>0 ):
    #             GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
    #             NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
    #             GPS_Info()                                          #get time, latitude, longitude
    #             print("lat in degrees:", lat_in_degrees," long in degree: ", long_in_degrees, "alt in degrees", alt_in_degrees,'\n')
    #             print("------------------------------------------------------------\n")
    #         if(GPVTG_data_available>0):
    #                 GPVTG_buffer = received_data.split("$GPVTG,",1)[1]  #store data coming afer "$GPVTG," string
    #                 NMEA_buff_v = (GPVTG_buffer.split(','))              #store comma seperated data in buffer 
    #                 GPS_velocity()                                    #get velocity

                
                            
    # except KeyboardInterrupt:
    #     webbrowser.open(map_link)        #open current position information in google map
    #     sys.exit(0)
# if __name__ == "__main__":
#     gps = GPS()
#     print(gps.get_coord())