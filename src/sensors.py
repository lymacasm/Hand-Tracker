from imu import IMU
from SerialController import SerialController
from buffer_filter import BufferFilter
import time
import threading

class Sensors(object):
    __thread_started = False

    def __init__(self):
        self.imu = IMU()
        self.imu.setAccelRangeG(8)
        self.imu.setGyroRangeDps(2000)
        self.flex = SerialController()
        self.flex.initialize()
        timeout = self.flex.ser.timeout
        self.flex.ser.timeout = 1
        self.flex.ser.read(500)
        self.flex.ser.timeout = timeout
        self.__accel_x_filter = BufferFilter(3)
        self.__accel_y_filter = BufferFilter(3)
        self.__accel_z_filter = BufferFilter(3)
        self.__gyro_x_filter = BufferFilter(7)
        self.__gyro_y_filter = BufferFilter(7)
        self.__gyro_z_filter = BufferFilter(7)
        self.__roll_filter = BufferFilter(5)
        self.__pitch_filter = BufferFilter(5)
        self.__fing0_filter = BufferFilter(5)
        self.__fing1_filter = BufferFilter(5)
        self.__fing2_filter = BufferFilter(5)
        self.__fing_avg_filter = BufferFilter(3)
        self.__orientation = "None"
        self.__terminate_thread = False
        self.__thread = threading.Thread(target=self.__sensor_update_thread, args=())
        self.__thread.start()
        self.__thread_started = True

    def __del__(self):
        if self.__thread_started:
            self.__terminate_thread = True
            self.__thread.join(10)
            if self.__thread.isAlive():
                print "Unable to terminate thread."

    def __sensor_update_thread(self):
        accel_threshold = 0.2
        gyro_threshold = 10
        time_queue = [time.time()]
        while(not self.__terminate_thread):
            # Sleep a bit so we don't use up too much of processor
            time.sleep(0.008)

            # Update IMU readings
            self.__accel_x_filter.add_data(self.imu.getAccelX())
            self.__accel_y_filter.add_data(self.imu.getAccelY())
            self.__accel_z_filter.add_data(self.imu.getAccelZ())
            self.__gyro_x_filter.add_data(self.imu.getGyroX())
            self.__gyro_y_filter.add_data(self.imu.getGyroY())
            self.__gyro_z_filter.add_data(self.imu.getGyroZ())

            # Store the time of the IMU readings
            time_queue.append(time.time())

            # Apply median filter to IMU readings, and convert to appropriate units
            filtered_accel = \
                {'x':self.__accel_x_filter.median(), 'y':self.__accel_y_filter.median(), 'z':self.__accel_z_filter.median()}
            filtered_gyro = \
                {'x':self.__gyro_x_filter.median(), 'y':self.__gyro_y_filter.median(), 'z':self.__gyro_z_filter.median()}
            accel_g = self.imu.convertAccelVecToG(filtered_accel)
            gyro_dps = self.imu.convertGyroVecToDps(filtered_gyro)

            # Caculate pitch and roll
            roll = 0
            pitch = 0
            accel_mag = self.imu.magVector(accel_g)
            if abs(accel_mag - 1) < accel_threshold:
                roll = self.imu.getRollAccel(accel_g)
                pitch = self.imu.getPitchAccel(accel_g)
            else:
                roll = self.roll + (time_queue[-1] - time_queue[-2]) * gyro_dps['x']
                pitch = self.pitch - (time_queue[-1] - time_queue[-2]) * gyro_dps['y']
            self.__roll_filter.add_data(roll)
            self.__pitch_filter.add_data(pitch)
            time_queue.pop(0)

            # Update Flex sensor readings
            self.flex.readFingers()
            self.__fing0_filter.add_data(self.flex.fings[0])
            self.__fing1_filter.add_data(self.flex.fings[1])
            self.__fing2_filter.add_data(self.flex.fings[2])
            fing_avg = float(self.__fing0_filter.median() + self.__fing1_filter.median() + self.__fing2_filter.median()) / 3.0
            self.__fing_avg_filter.add_data(fing_avg)
                
    @property
    def roll(self):
        return self.__roll_filter.mean()

    @property
    def pitch(self):
        return self.__pitch_filter.mean()

    @property
    def speed(self):
        if self.fings > 3000:
            return 0
        else:
            return 100

    @property
    def fings(self):
        return self.__fing_avg_filter.mean()

    @property
    def fing0(self):
        return self.__fing0_filter.median()

    @property
    def fing1(self):
        return self.__fing1_filter.median()
    
    @property
    def fing2(self):
        return self.__fing2_filter.median()
 
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
