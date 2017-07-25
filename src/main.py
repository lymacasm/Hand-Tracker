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
        time.sleep(0.1)
        
        #sendToHost("%s,%d" % (sensors.orientation, sensors.avg_bend))
        if sensors.orientation != orientation or abs(sensors.speed - speed) > speed_thresh:
            orientation = sensors.orientation
            speed = sensors.speed
            sendToHost("%s,%d" % (orientation, speed))
        #print "orientation=%s, speed=%d, fings=%d, fing1=%d, fing2=%s" % (sensors.orientation, sensors.speed, sensors.fings, sensors.fing1, sensors.fing2)
        #print "accelMag=%s, gyroMag=%s" % (sensors.imu.magVector(sensors.imu.getAccelG()), sensors.imu.magVector(sensors.imu.getGyroDps()))
        #print "fing1=%s,fing2=%s,fing3=%s,fings=%s" % (sensors.fing0, sensors.fing1, sensors.fing2, sensors.fings)
        #print "fings=%d (%d,%d,%d)" % (sensors.fings, sensors.fing0, sensors.fing1, sensors.fing2)
        #print "roll=%s" % sensors.roll

if __name__ == "__main__":
    main(sys.argv)
