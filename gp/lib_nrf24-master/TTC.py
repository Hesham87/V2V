import math
class TimeToCollision():
    def TTC(self, V_lead, V_follow, accel_lead, distance):
        V_relative = V_lead - V_follow  # is the initial velocity of the leading vehicle wrt the following vehicle
        V_lead_final = math.sqrt(math.pow(V_relative, 2) + (2 * accel_lead * distance))
        t1 = abs((- V_relative - V_lead_final) / accel_lead)
        t2 = (- V_relative + V_lead_final) / accel_lead
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
    
    def warningLv(self, V_lead, V_follow, accel_lead, distance, decceleration = -4):
        ttc = self.TTC(V_lead, V_follow, accel_lead, distance)
        tts = self.TTS(V_follow, decceleration)
        warningRatio =  tts/ttc
        if warningRatio > 0.5 and warningRatio <0.7:
            return 1
        elif warningRatio > 0.7 and warningRatio <0.8:
            return 2
        elif  warningRatio > 0.8:
            return 3
        else:
            return 0