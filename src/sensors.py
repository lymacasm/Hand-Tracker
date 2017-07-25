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
            time.sleep(0.001)

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
            filtered_accel = self.accel
            filtered_gyro = self.gyro
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
            fing_avg = float(self.fing1 + self.fing2) / 2.0
            self.__fing_avg_filter.add_data(fing_avg)
                
    @property
    def roll(self):
        return self.__roll_filter.median()

    @property
    def pitch(self):
        return self.__pitch_filter.median()

    @property
    def speed(self):
        max_speed = 100
        max_fings = 3350
        min_fings = 2350
        if self.fings > max_fings:
            return 0
        elif self.fings < min_fings:
            return max_speed
        else:
            speed = max_speed - (self.fings - min_fings) * max_speed / (max_fings - min_fings)
            return speed

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
    def accelx(self):
        return self.__accel_x_filter.mean()

    @property
    def accely(self):
        return self.__accel_y_filter.mean()

    @property
    def accelz(self):
        return self.__accel_z_filter.mean()

    @property
    def gyrox(self):
        return self.__gyro_x_filter.mean()

    @property
    def gyroy(self):
        return self.__gyro_y_filter.mean()

    @property
    def gyroz(self):
        return self.__gyro_z_filter.mean()

    @property
    def accel(self):
        return {"x":self.accelx, "y":self.accely, "z":self.accelz}

    @property
    def gyro(self):
        return {"x":self.gyrox, "y":self.gyroy, "z":self.gyroz}
 
    @property
    def orientation(self):
        # Define centroids for each class
        up_center = -12
        right_center = -90
        left_center = 87
        down_center = 173

        # Define thresholds for each class
        up_threshold = 47
        right_threshold = 25
        left_threshold = 50
        down_threshold = 30

        if (up_center - up_threshold) < self.roll < (up_center + up_threshold):
            self.__orientation = "Up"    
        elif (right_center - right_threshold) < self.roll < (right_center + right_threshold):
            self.__orientation = "Right"
        elif (left_center - left_threshold) < self.roll < (left_center + left_threshold):
            self.__orientation = "Left" 
        elif ((down_center - down_threshold) < self.roll <= 180) or (-180 < self.roll < (-360 + down_center + down_threshold)):
            self.__orientation = "Down"

        return self.__orientation
