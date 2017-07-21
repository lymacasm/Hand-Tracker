from imu import IMU
from SerialController import SerialController
import time
import threading

class Sensors(object):
    def __init__(self):
        self.imu = IMU()
        self.imu.setAccelRangeG(8)
        self.imu.setGyroRangeDps(2000)
		self.flex = SerialContoller()
		self.flex.initialize()
        self.roll = 0
        self.pitch = 0
        self._orientation = "None"
        self._thread = threading.Thread(target=self.__orientation_update_thread, args=())
        self._thread.start()

    def __orientation_update_thread(self):
        accel_threshold = 0.2
        gyro_threshold = 10
        
        self.roll = self.imu.getRollAccel()
        self.pitch = self.imu.getPitchAccel()
        gyro_last = self.imu.getGyroDps()
        time_queue = [time.time()]
        while(True):
            time.sleep(0.008)
            accel_g = self.imu.getAccelG()
            gyro_dps = self.imu.getGyroDps()
            time_queue.append(time.time())
            accel_mag = self.imu.magVector(accel_g)
            new_roll = 0
            new_pitch = 0
            if abs(accel_mag - 1) < accel_threshold:
                new_roll = self.imu.getRollAccel()
                new_pitch = self.imu.getPitchAccel()
            else:
                new_roll = self.roll + (time_queue[-1] - time_queue[-2]) * gyro_dps['x']
                new_pitch = self.pitch - (time_queue[-1] - time_queue[-2]) * gyro_dps['y']
            self.roll = self.roll*0.4 + new_roll*0.6
            self.pitch = self.pitch*0.4 + new_pitch*0.6
            time_queue.pop(0)
                
    @property
    def orientation(self):
        # Define centroids for each class
        up_center = -7
        right_center = -110
        left_center = 80
        down_center = 176

        # Define thresholds for each class
        up_threshold = 25
        right_threshold = 35
        left_threshold = 55
        down_threshold = 30

        if (up_center - up_threshold) < self.roll < (up_center + up_threshold):
            self._orientation = "Up"    
        elif (right_center - right_threshold) < self.roll < (right_center + right_threshold):
            self._orientation = "Right"
        elif (left_center - left_threshold) < self.roll < (left_center + left_threshold):
            self._orientation = "Left" 
        elif ((down_center - down_threshold) < self.roll <= 180) or (-180 < self.roll < (-360 + down_center + down_threshold)):
            self._orientation = "Down"

        return self._orientation
