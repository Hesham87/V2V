import time
from tracemalloc import start
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_bno055
import numpy as np
import math

class imu:

    # To enable i2c-gpio, add the line `dtoverlay=i2c-gpio` to /boot/config.txt
    # Then reboot the pi

    # Create library object using our Extended Bus I2C port
    # Use `ls /dev/i2c*` to find out what i2c devices are connected

    def current_milli_time(self):
        return round(time.time() * 1000)

    acceleration = np.array([0,0,0], dtype=float)
    def getAccel(self):
        return math.sqrt(math.pow(self.acceleration[0], 2) + math.pow(self.acceleration[1], 2) + math.pow(self.acceleration[2], 2))

    Vx = 0
    Vy = 0
    Vz = 0
    resultantVelocity = 0
    def getVelocity(self):
        return self.resultantVelocity
    

    def velocity(self):
        i2c = I2C(1)  # Device is /dev/i2c-1
        sensor = adafruit_bno055.BNO055_I2C(i2c)
        startTime = self.current_milli_time()
        currentTime = startTime
        self.Vx = 0
        self.Vy = 0
        self.Vz = 0
        counter = 0
        avg_accel = np.zeros_like(np.array(sensor.linear_acceleration), dtype=float)
        time2 = 0
        accTime1 = 0
        accTime2 = 0
        accel_counter = 1
        avg_accel_peroidic = np.array([0,0,0], dtype=float)
        result_vel = 0
        while True:
            # print("Vx : {}".format(avg_accel))
            while (currentTime - startTime) / 1000 < 2:
                currentTime = self.current_milli_time()
                # accel = np.array(sensor.linear_acceleration, dtype=float)
                # if(math.isnan(accel[0]) == False and math.isnan(accel[1]) == False and math.isnan(accel[2]) == False):
                #     avg_accel += np.array(sensor.linear_acceleration, dtype=float)
                #     counter += 1
                # else:
                #     counter += 1
                accel = np.array(sensor.linear_acceleration, dtype=float)
                while math.isnan(accel[0]) == True or math.isnan(accel[1]) == True or math.isnan(accel[2]) == True:
                    accel = np.array(sensor.linear_acceleration, dtype=float)
                counter += 1

            if counter != 1:
                self.acceleration = avg_accel
                accTime1 = self.current_milli_time()
                accTime2 = self.current_milli_time()
                time2 = self.current_milli_time()

            avg_accel /= counter
            counter = 1
            accel = np.array(sensor.linear_acceleration, dtype=float)
            while math.isnan(accel[0]) == True or math.isnan(accel[1]) == True or math.isnan(accel[2]) == True:
                accel = np.array(sensor.linear_acceleration, dtype=float)
            self.Vx += ((accel[0] - avg_accel[0]) * ((self.current_milli_time() - time2) / 1000))
            self.Vy += ((accel[1] - avg_accel[1]) * ((self.current_milli_time() - time2) / 1000))
            self.Vz += ((accel[2] - avg_accel[2]) * ((self.current_milli_time() - time2) / 1000))
            
            # curr = self.current_milli_time()
            curr_v = math.sqrt(math.pow(self.Vx, 2) + math.pow(self.Vy, 2) + math.pow(self.Vz, 2))
            self.resultantVelocity = curr_v - ((self.current_milli_time() - time2) * result_vel)
            if (currentTime - startTime) / 1000 < 13:
                currentTime = self.current_milli_time()
                result_vel += (math.sqrt(math.pow(self.Vx, 2) + math.pow(self.Vy, 2) + math.pow(self.Vz, 2)) / 2750)
            # else:
            #     curr = self.current_milli_time()

            time2 = self.current_milli_time()
            test = (accTime2 - accTime1) / 1000
            if(test > 0.1):
                self.acceleration = avg_accel_peroidic/ accel_counter
                accel_counter = 1
                accTime1 = self.current_milli_time()
                accTime2 = self.current_milli_time()
                avg_accel_peroidic = np.zeros_like(avg_accel_peroidic, dtype= float) 
                # print("Vx : {}".format(self.Vx))
                # print("Vy : {}".format(self.Vy))
                # print("Vz : {}".format(self.Vz))

            else:
                accTime2 = self.current_milli_time()
                accel_counter += 1
                avg_accel_peroidic += accel
            # print("________________________________________________________________________")
            # print("average : {}".format(avg_accel))
            # print("Vx : {}".format(Vx))
            # print("Vy : {}".format(Vy))
            # print("Vz : {}".format(Vz))
            # print("________________________________________________________________________")
            # print("ax : {}".format(sensor.linear_acceleration[0]))
            # print("ay : {}".format(sensor.linear_acceleration[1]))
            # print("az : {}".format(sensor.linear_acceleration[2]))
            
            # print("Temperature: {} degrees C".format(temperature()))
            # print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
            # print("Magnetometer (microteslas): {}".format(sensor.magnetic))
            # print("Gyroscope (rad/sec): {}".format(sensor.gyro))
            # print("Euler angle: {}".format(sensor.euler))
            # print("Quaternion: {}".format(sensor.quaternion))
            # print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
            # print("Gravity (m/s^2): {}".format(sensor.gravity))
            # print()

# if __name__ == "__main__":
#     my_imu = imu()
#     while True:
#         print("Vx: {}".format(my_imu.Vx))
#         print("Vy: {}".format(my_imu.Vy))
#         print("Vz: {}".format(my_imu.Vz))