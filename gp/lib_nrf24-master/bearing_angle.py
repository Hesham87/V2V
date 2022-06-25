import math

class BearingAngle():

    def __init__(self) -> None:
        self.bearing_angle_deg =0
    
    def getBearing(self):
        return self.bearing_angle_deg
    # all parameters are in degree not radian
    def is_same_lane(self,this_lat, this_lon, that_lat, that_lon, this_heading, that_heading):
        # convert angles from degree to radians
        this_lat = math.radians(this_lat)
        this_lon = math.radians(this_lon)
        that_lat = math.radians(that_lat)
        that_lon = math.radians(that_lon)

        # Bearing angle in Degree
        x = math.cos(that_lat) * math.sin(that_lon - this_lon)
        y = math.cos(this_lat) * math.sin(that_lat) - math.sin(this_lat) * \
            math.cos(that_lat) * math.cos(that_lon - this_lon)
        self.bearing_angle_deg = (math.atan2(x, y) * 180 / math.pi + 360) % 360
        print("Bearing angle: {}".format(self.bearing_angle_deg))
        # calculating the heading difference angle
        heading_difference = math.fabs(this_heading - that_heading)
        if heading_difference > 180:
            heading_difference = 360 - heading_difference

        # comparing the bearing angle with the headings
        angle_difference = math.fabs(this_heading - self.bearing_angle_deg)
        if angle_difference > 180:
            angle_difference = 360 - angle_difference

        # check whether the two cars are in the same lane or not
        same_lane = False
        if heading_difference < 10 and angle_difference > 5:
            same_lane = False
        elif angle_difference < 5 and heading_difference < 10:
            same_lane = True

        return same_lane