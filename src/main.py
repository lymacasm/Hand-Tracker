import sys
import time
import threading
from comm import sendToHost
from sensors import Sensors

def main(argv):
    sensors = Sensors()
    orientation = "None"
    speed = 0
    speed_thresh = 5
    while(True):
        time.sleep(0.05)
        
        #sendToHost("%s,%d" % (sensors.orientation, sensors.avg_bend))
        if sensors.orientation != orientation or abs(sensors.speed - speed) > speed_thresh:
            orientation = sensors.orientation
            speed = sensors.speed
            sendToHost("%s,%d" % (orientation, speed))
            print "orientation=%s, speed=%s" % (sensors.orientation, sensors.speed)
        #print "accelMag=%s, gyroMag=%s" % (sensors.imu.magVector(sensors.imu.getAccelG()), sensors.imu.magVector(sensors.imu.getGyroDps()))

if __name__ == "__main__":
    main(sys.argv)
