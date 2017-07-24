from smbus import SMBus
import math
import time

def twos_complement(val, bits):
    # Converts two's complement number to regular expression
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val 

class IMU:
    def __init__(self):
        self.bus = SMBus(1) # initialize I2C bus on I2C interface 1
        self._imu_addr_ = 0x68
        self._accel_config_ = 0x1C
        self._accel_limits_ = [2, 4, 8, 16]
        self._accel_x_ = 0x3B
        self._accel_y_ = 0x3D
        self._accel_z_ = 0x3F
        self._temp_ = 0x41
        self._gyro_config_ = 0x1B
        self._gyro_limits_ = [250, 500, 1000, 2000]
        self._gyro_x_ = 0x43
        self._gyro_y_ = 0x45
        self._gyro_z_ = 0x47
        self._int_bypass_ = 0x37
        self._mag_addr_ = 0x0C
        self._mag_x_ = 0x03
        self._mag_y_ = 0x05
        self._mag_z_ = 0x07
        self._mag_read_timeout_ = 1
        self._mag_st2_ = 0x09
        self._mag_st1_ = 0x02
        self._mag_cntl1_ = 0x0A

        # Enable bypass so we can talk to magnetometer
        bypass_config = self.bus.read_byte_data(self._imu_addr_, self._int_bypass_)
        bypass_config = bypass_config | 0x2
        self.bus.write_byte_data(self._imu_addr_, self._int_bypass_, bypass_config)

        # Configure magnetometer in continuous mode
        mag_config = self.bus.read_byte_data(self._mag_addr_, self._mag_cntl1_)
        mag_config = mag_config | 0x16 # 16 bit, Continuous mode 2
        self.bus.write_byte_data(self._mag_addr_, self._mag_cntl1_, mag_config)


    def getAccelX(self):
        # Returns raw x-component from accelerometer
        high_byte = self.bus.read_byte_data(self._imu_addr_, self._accel_x_)
        low_byte = self.bus.read_byte_data(self._imu_addr_, self._accel_x_ + 1)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getAccelY(self):
        # Returns raw y-component from accelerometer
        high_byte = self.bus.read_byte_data(self._imu_addr_, self._accel_y_)
        low_byte = self.bus.read_byte_data(self._imu_addr_, self._accel_y_ + 1)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getAccelZ(self):
        # Returns raw z-component from accelerometer
        high_byte = self.bus.read_byte_data(self._imu_addr_, self._accel_z_)
        low_byte = self.bus.read_byte_data(self._imu_addr_, self._accel_z_ + 1)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getGyroX(self):
        # Returns raw x-component from gyroscope
        high_byte = self.bus.read_byte_data(self._imu_addr_, self._gyro_x_)
        low_byte = self.bus.read_byte_data(self._imu_addr_, self._gyro_x_ + 1)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getGyroY(self):
        # Returns raw y-component from gyroscope
        high_byte = self.bus.read_byte_data(self._imu_addr_, self._gyro_y_)
        low_byte = self.bus.read_byte_data(self._imu_addr_, self._gyro_y_ + 1)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getGyroZ(self):
        # Returns raw z-component from gyroscope
        high_byte = self.bus.read_byte_data(self._imu_addr_, self._gyro_z_)
        low_byte = self.bus.read_byte_data(self._imu_addr_, self._gyro_z_ + 1)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getMagX(self):
        # Returns raw x-component from magnetometer
        timeout_start = time.time()
        while ( self.bus.read_byte_data(self._mag_addr_, self._mag_st1_) & 0x1 ) is 0:
            if (time.time() - timeout_start) > self._mag_read_timeout_:
                print "Mag read timeout"
                return 0
        low_byte = self.bus.read_byte_data(self._mag_addr_, self._mag_x_)
        high_byte = self.bus.read_byte_data(self._mag_addr_, self._mag_x_ + 1)
        ovrflow = self.bus.read_byte_data(self._mag_addr_, self._mag_st2_)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getMagY(self):
        # Returns raw y-component from magnetometer
        timeout_start = time.time()
        while ( self.bus.read_byte_data(self._mag_addr_, self._mag_st1_) & 0x1 ) is 0:
            if (time.time() - timeout_start) > self._mag_read_timeout_:
                print "Mag read timeout"
                return 0
        low_byte = self.bus.read_byte_data(self._mag_addr_, self._mag_y_)
        high_byte = self.bus.read_byte_data(self._mag_addr_, self._mag_y_ + 1)
        ovrflow = self.bus.read_byte_data(self._mag_addr_, self._mag_st2_)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)

    def getMagZ(self):
        # Returns raw z-component from magnetometer
        timeout_start = time.time()
        while ( self.bus.read_byte_data(self._mag_addr_, self._mag_st1_) & 0x1 ) is 0:
            if (time.time() - timeout_start) > self._mag_read_timeout_:
                print "Mag read timeout"
                return 0
        low_byte = self.bus.read_byte_data(self._mag_addr_, self._mag_z_)
        high_byte = self.bus.read_byte_data(self._mag_addr_, self._mag_z_ + 1)
        ovrflow = self.bus.read_byte_data(self._mag_addr_, self._mag_st2_)
        data_raw = (high_byte << 8) | low_byte
        return twos_complement(data_raw, 16)
        
    def getTemp(self):
        # Returns raw temperature
        return (self.bus.read_byte_data(self._imu_addr_, self._temp_) << 8) | \
               self.bus.read_byte_data(self._imu_addr_, self._temp_ + 1)

    def getAccel(self):
        # Returns dictionary with raw accelerometer readings in each direction
        x = self.getAccelX()
        #time.sleep(0.0001)
        y = self.getAccelY()
        #time.sleep(0.0001)
        z = self.getAccelZ()
        return {'x':x, 'y':y, 'z':z}

    def getGyro(self):
        # Returns dictionary with raw gyroscope readings in each direction
        x = self.getGyroX()
        #time.sleep(0.0008)
        y = self.getGyroY()
        #time.sleep(0.0008)
        z = self.getGyroZ()
        return {'x':x, 'y':y, 'z':z}

    def getMag(self):
        # Returns dictionary with raw magnetometer readings in each direction
        return {'x':self.getMagX(), 'y':self.getMagY(), 'z':self.getMagZ()}

    def getAccelRangeG(self):
        # Returns current setting for max value in g's (min is negative max)
        config_reg = self.bus.read_byte_data(self._imu_addr_, self._accel_config_)
        config_reg = (config_reg & 0x18) >> 3
        return self._accel_limits_[config_reg]

    def getGyroRangeDps(self):
        # Returns current setting for max value in dps (min is negative max)
        config_reg = self.bus.read_byte_data(self._imu_addr_, self._gyro_config_)
        config_reg = (config_reg & 0x18) >> 3
        return self._gyro_limits_[config_reg]

    def getMagRangeuT(self):
        # Non-configurable, just for consistency and conversions
        return 4912

    def setAccelRangeG(self, limit):
        # Sets the max accel value in g's (min is negative max)
        if limit not in self._accel_limits_:
            raise ValueError("Invalid value for limit argument. Must be one of %s" % self._accel_limits_)

        config_reg = self.bus.read_byte_data(self._imu_addr_, self._accel_config_)
        config_val = self._accel_limits_.index(limit)
        config_reg = (config_reg & ~0x18) | ((config_val & 0x3) << 3)
        self.bus.write_byte_data(self._imu_addr_, self._accel_config_, config_reg)
        return

    def setGyroRangeDps(self, limit):
        # Sets the max gyro value in dps (min is negative max)
        if limit not in self._gyro_limits_:
            raise ValueError("Invalid value for limit argument. Must be one of %s" % self._gyro_limits_)

        config_reg = self.bus.read_byte_data(self._imu_addr_, self._gyro_config_)
        config_val = self._gyro_limits_.index(limit)
        config_reg = (config_reg & ~0x18) | ((config_val & 0x3) << 3)
        self.bus.write_byte_data(self._imu_addr_, self._gyro_config_, config_reg)
        return

    def getAccelXG(self):
        # Returns x-component from accelerometer in g's
        val = float(self.getAccelX())
        limit = float(self.getAccelRangeG())
        return val * limit / 0x7FFF

    def getAccelYG(self):
        # Returns y-component from accelerometer in g's
        val = float(self.getAccelY())
        limit = float(self.getAccelRangeG())
        return val * limit / 0x7FFF

    def getAccelZG(self):
        # Returns z-component from accelerometer in g's
        val = float(self.getAccelZ())
        limit = float(self.getAccelRangeG())
        return val * limit / 0x7FFF

    def getGyroXDps(self):
        # Returns x-component from gyroscope in dps
        val = float(self.getGyroX())
        limit = float(self.getGyroRangeDps())
        return val * limit / 0x7FFF

    def getGyroYDps(self):
        # Returns y-component from gyroscope in dps
        val = float(self.getGyroY())
        limit = float(self.getGyroRangeDps())
        return val * limit / 0x7FFF

    def getGyroZDps(self):
        # Returns z-component from gyroscope in dps
        val = float(self.getGyroZ())
        limit = float(self.getGyroRangeDps())
        return val * limit / 0x7FFF

    def getMagXuT(self):
        # Returns x-component from magnetometer in uT
        val = float(self.getMagX())
        limit = float(self.getMagRangeuT())
        return val * limit / 0x7FF8

    def getMagYuT(self):
        # Returns y-component from magnetometer in uT
        val = float(self.getMagY())
        limit = float(self.getMagRangeuT())
        return val * limit / 0x7FF8

    def getMagZuT(self):
        # Returns y-component from magnetometer in uT
        val = float(self.getMagZ())
        limit = float(self.getMagRangeuT())
        return val * limit / 0x7FF8

    def getAccelG(self):
        # Returns accelerometer data in all directions in g's
        return {'x':self.getAccelXG(), 'y':self.getAccelYG(), 'z':self.getAccelZG()}

    def getGyroDps(self):
        # Returns gyroscope data in all directions in dps
        return {'x':self.getGyroXDps(), 'y':self.getGyroYDps(), 'z':self.getGyroZDps()}

    def getMaguT(self):
        # Returns magnetometer data in all directions in uT
        return {'x':self.getMagXuT(), 'y':self.getMagYuT(), 'z':self.getMagZuT()}

    def convertAccelToG(self, raw, limit):
        # Converts raw accelerometer data to g's. User is
        # responsible to remember the setting when data was collected.
        if limit not in self._accel_limits_:
            raise ValueError("Limit must be one of the following: %s" % self._accel_limits_)
        return float(raw) * float(limit) / 0x7FFF

    def convertAccelVecToG(self, raw_vector):
        limit = self.getAccelRangeG()
        x = self.convertAccelToG(raw_vector['x'], limit)
        y = self.convertAccelToG(raw_vector['y'], limit)
        z = self.convertAccelToG(raw_vector['z'], limit)
        return {'x':x, 'y':y, 'z':z}

    def convertGyroToDps(self, raw, limit):
        # Converts raw gyroscope data to dps. User is responsible
        # to remember the setting when data was collected.
        if limit not in self._gyro_limits_:
            raise ValueError("Limit must be one of the following: %s" % self._gyro_limits_)
        return float(raw) * float(limit) / 0x7FFF

    def convertGyroVecToDps(self, raw_vector):
        limit = self.getGyroRangeDps()
        x = self.convertGyroToDps(raw_vector['x'], limit)
        y = self.convertGyroToDps(raw_vector['y'], limit)
        z = self.convertGyroToDps(raw_vector['z'], limit)
        return {'x':x, 'y':y, 'z':z}

    def convertMagTouT(self, raw):
        # Converts raw magnetometer data to uT
        limit = float(self.getMagRangeuT())
        return float(raw) * limit / 0x7FF8

    def getRollAccel(self, accel_dict=None):
        Ry = 0
        Rz = 0
        if accel_dict is None:
            Ry = self.getAccelY()
            Rz = self.getAccelZ()
        else:
            Ry = accel_dict['y']
            Rz = accel_dict['z']
        return math.atan2(Ry, Rz) * 180 / math.pi

    def getPitchAccel(self, accel_dict=None):
        Rx = 0
        Rz = 0
        if accel_dict is None:
            Rx = self.getAccelX()
            Rz = self.getAccelZ()
        else:
            Rx = accel_dict['x']
            Rz = accel_dict['z']
        return math.atan2(Rx, Rz) * -180 / math.pi

    def magVector(self, vector):
        sqrd_sum = vector['x']*vector['x'] + vector['y']*vector['y'] + vector['z']*vector['z']
        return math.sqrt(sqrd_sum)
