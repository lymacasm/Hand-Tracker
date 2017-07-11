import sys
import time
import threading
from imu import IMU

global_roll = 0
global_pitch = 0

def orientation_update_thread(imu):
    accel_threshold = 0.2
    gyro_threshold = 10

    global_roll = imu.getRollAccel()
    global_pitch = imu.getPitchAccel()
    gyro_last = imu.getGyroDps()
    time_queue = [time.time()]
    count = 0
    while(True):
        if (count % 7) == 0:
            print "roll=%s, pitch=%s" % (global_roll, global_pitch)
            pass
        time.sleep(0.008)
        accel_g = imu.getAccelG()
        gyro_dps = imu.getGyroDps()
        time_queue.append(time.time())
        accel_mag = imu.magVector(accel_g)
        new_roll = 0
        new_pitch = 0
        if abs(accel_mag - 1) < accel_threshold:
            new_roll = imu.getRollAccel()
            new_pitch = imu.getPitchAccel()
        else:
            new_roll = global_roll +  (time_queue[-1] - time_queue[-2]) * gyro_dps['x']
            new_pitch = global_pitch - (time_queue[-1] - time_queue[-2]) * gyro_dps['y']
        global_roll = global_roll*0.4 + new_roll*0.6
        global_pitch = global_pitch*0.4 + new_pitch*0.6
        time_queue.pop(0)
        count += 1
       

def IMU_init(imu):
    imu.setAccelRangeG(8)
    imu.setGyroRangeDps(2000)

def main(argv):
    imu = IMU()
    IMU_init(imu)
    '''
    timer_start = time.time()
    for i in range(0,1000):
        imu.getAccel()
    print "Frequency of Accel is %s Hz" % (3*1000 / (time.time() - timer_start))

    timer_start = time.time()
    for i in range(0,1000):
        imu.getGyro()
    print "Frequency of Gyro is %s Hz" % (3*1000 / (time.time() - timer_start))
    '''
    t = threading.Thread(target=orientation_update_thread, args = (imu,))
    t.daemon = True
    t.start()
    while(True):
        #print "x=%s, y=%s, z=%s" % (imu.getAccelX(), imu.getAccelY(), imu.getAccelZ())    
        #print "roll=%s pitch=%s" % (imu.getRollAccel(), imu.getPitchAccel())
        #print "x=%s, y=%s, z=%s" % (imu.getGyroXDps(), imu.getGyroYDps(), imu.getGyroZDps())
        time.sleep(100)

if __name__ == "__main__":
    main(sys.argv)
