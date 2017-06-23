import sys
import time
from imu import IMU

def IMU_init(imu):
    imu.setAccelRangeG(8)
    imu.setGyroRangeDps(1000)

def main(argv):
    imu = IMU()
    IMU_init(imu)
    
    timer_start = time.time()
    for i in range(0,1000):
        imu.getAccel()
    print "Frequency of Accel is %s Hz" % (1000 / (time.time() - timer_start))

    timer_start = time.time()
    for i in range(0,1000):
        imu.getGyro()
    print "Frequency of Gyro is %s Hz" % (1000 / (time.time() - timer_start))

    timer_start = time.time()
    for i in range(0,1000):
        imu.getMag()
    print "Frequency of Mag is %s Hz" % (1000 / (time.time() - timer_start))

if __name__ == "__main__":
    main(sys.argv)
