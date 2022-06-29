import math
class TimeToCollision():
    def TTC(self, V_lead, V_follow, accel_lead, distance):
        V_relative = V_lead - V_follow  # is the initial velocity of the leading vehicle wrt the following vehicle
        V_lead_final = math.sqrt(math.pow(V_relative, 2) + (2 * accel_lead * distance))
        t1 = abs((- V_relative - V_lead_final) / (accel_lead+0.00001))
        t2 = (- V_relative + V_lead_final) / (accel_lead + 0.00001)
        if  t1<0:
            return t2
        elif t2<0:
            return t1
        elif t1 < t2:
            return t1
        else:
            return t2
    
    def TTS(self, Velocity, decceleration = -4):
        return (-Velocity) / decceleration
    
    def DTS(self, velocity, decceleration = -4):
        reaction_time = 1.5
        return ((-velocity) / (2 * decceleration)) + (velocity * (reaction_time) + (0.5 * decceleration * math.pow(reaction_time, 2)))

    def warningLv(self, V_lead, V_follow, accel_lead, distance, decceleration = -4):
        ttc = self.TTC(V_lead, V_follow, accel_lead, distance)
        tts = self.TTS(V_follow, decceleration)
        #print(f"TTC = {ttc}, TTS = {tts}")
        warningRatio =  tts/ttc
        # warning_time = ttc #- tts
        # res = warning_time
        # return res
        if warningRatio > 0.5 and warningRatio < 0.7:
            return 10
        elif warningRatio > 0.7 and warningRatio < 0.8:
            return 6
        elif  warningRatio > 0.8:
            return 3
        else:
            return 100

def get_myTTC(_velocity,_distance):
    if(_velocity>0):
        _ttc = (_distance*0.7)/(_velocity*1.3)
    else:
        _ttc = 100
    return _ttc
        