from code import interact
import math
from multiprocessing.managers import RemoteError
import time
import sys
sys.path.insert(1, '/home/pi/transmit/compass/py-qmc5883l')
from py_qmc5883l import QMC5883L

class heading:
    sensor = QMC5883L()
    def __init__(self, sector_size = 18) -> None:
        self.SECTORS_COUNT = int(360 / sector_size)
        self.SECTOR_WIDTH = (2 * math.pi) / self.SECTORS_COUNT
    
    def get_heading(self):
        try:
            (x, y, z) = self.sensor.get_magnet_raw()

            if x is not None and y is not None:
                # Angle on the XY plane from magnetic sensor.
                angle = math.atan2(y, x)
                if angle < 0:
                    angle += 2 * math.pi
                # Needle angle, rounded to sector center.
                sector = int(angle / self.SECTOR_WIDTH)

                needle_angle = ((2 * math.pi) / self.SECTORS_COUNT) * sector
                # Hide compass needle at previous position.
                return math.degrees(angle)
        except IOError:
            print("I/o error")
            return -1


# if __name__ == "__main__":
#     head = heading()
#     while True:
#         print(head.get_heading())
#         time.sleep(2)