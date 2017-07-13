import sys
import time
import threading
from sensors import Sensors

def main(argv):
    sensors = Sensors()
    while(True):
        time.sleep(0.1)
        print "orientation=%s, roll=%s" % (sensors.orientation, sensors.roll)
        #print "accelMag=%s, gyroMag=%s" % (sensors.imu.magVector(sensors.imu.getAccelG()), sensors.imu.magVector(sensors.imu.getGyroDps()))

if __name__ == "__main__":
    main(sys.argv)
