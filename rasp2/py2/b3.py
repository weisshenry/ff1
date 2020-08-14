import smbus
import time
import datetime
import os
import sys
import RPi.GPIO as GPIO
import ConfigParser
from collections import deque
from reg1 import *
import pdb

def my_callback(channel):
    bus = smbus.SMBus(1)
    axisData = bus.read_i2c_block_data(i2caddr, REG_OUT_X_MSB, 6)  
    runTimeConfigObject.NumInterrupts = runTimeConfigObject.NumInterrupts + 1
    #
    xAccel = ((axisData[0] << 8) | axisData[1]) >> 2
    yAccel = ((axisData[2] << 8) | axisData[3]) >> 2
    zAccel = ((axisData[4] << 8) | axisData[5]) >> 2
    plo = bus.read_byte_data(i2caddr, REG_PL_STATUS) & 0x7
    # Append data to the accelBuffer
    accelBuffer.append([str(datetime.datetime.now()), xAccel, yAccel, zAccel, plo])
    pass


class Accel():
    raspiBus = -1               # 
    raspiIntEnabled = 0         #
    raspiInfo = ""              #
    def __init__(self):        
        myBus = ""
        if GPIO.RPI_INFO['P1_REVISION'] == 1:
            myBus = 0
        else:
            myBus = 1
        self.raspiBus = myBus
        self.b = smbus.SMBus(myBus)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
        self.a = i2caddr
        self.high_res_mode = OVERSAMPLING_MODE
        self.sensor_range = RANGE_2_G
        self.raspiInfo = GPIO.RPI_INFO

    def init(self):
        self.writeRegister(REG_CTRL_REG2, self.readRegister(REG_CTRL_REG2) | FLAG_RESET)  # Reset        
        self.writeRegister(REG_CTRL_REG1, self.readRegister(REG_CTRL_REG1) & ~FLAG_ACTIVE)  # Put the device in Standby
        self.writeRegister(REG_CTRL_REG1, self.readRegister(REG_CTRL_REG1) & ~FLAG_F_READ)  # No Fast-Read (14-bits), Fast-Read (8-Bits)
        self.writeRegister(REG_CTRL_REG1, self.readRegister(REG_CTRL_REG1) | FLAG_ODR_50_HZ)  # Data Rate
        self.writeRegister(REG_XYZ_DATA_CFG, self.readRegister(REG_XYZ_DATA_CFG) | FLAG_XYZ_DATA_BIT_FS_4G)  # Full Scale Range 2g, 4g or 8g
        self.writeRegister(REG_CTRL_REG1, self.readRegister(REG_CTRL_REG1) | FLAG_LNOISE)  # Low Noise
        self.writeRegister(REG_CTRL_REG2, self.readRegister(REG_CTRL_REG2) & ~FLAG_SLPE)  # No Auto-Sleep
        self.writeRegister(REG_CTRL_REG2, self.readRegister(REG_CTRL_REG2) | FLAG_SMODS_HR)  # High Resolution
        self.writeRegister(REG_PL_CFG, self.readRegister(REG_PL_CFG) | FLAG_PL_CFG_PL_EN)  # P/L Detection Enabled

        # Setup interrupts
        if CFG_INTERRUPT == 1:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback)          
            self.raspiIntEnabled = 1    # Interrupt enabled successfully          
            my_callback(0)              # Force 1st sensor read
            # Configure register for interrupt
            self.writeRegister(REG_CTRL_REG4, 0x00)  # Reset all interrupt enabled flags
            self.writeRegister(REG_CTRL_REG4, self.readRegister(REG_CTRL_REG4) | FLAG_INT_EN_DRDY) 
            # Data Ready  Enabled
            self.writeRegister(REG_CTRL_REG5, 0x00)  # Reset all interrupt config flags
            self.writeRegister(REG_CTRL_REG5, self.readRegister(REG_CTRL_REG5) | FLAG_INT_CFG_DRDY)
            # Data Ready to INT1 pin            
            accelBuffer = deque()      # Initialize the accelBuffer
        # Activate the sensor
        self.writeRegister(REG_CTRL_REG1, self.readRegister(REG_CTRL_REG1) | FLAG_ACTIVE)  

    def writeRegister(self, regNumber, regData):      
        try:
            self.b.write_byte_data(self.a, regNumber, regData)
            time.sleep(0.01)
        except IOError:
            print("Error detected in function writeRegister() [IOError = " + str(IOError) + "]")
            sys.exit()

    def readRegister(self, regNumber):
        try:
            return self.b.read_byte_data(self.a, regNumber)
        except IOError:
            print("Error detected in function readRegister() [IOError = " + str(IOError) + "]")
            sys.exit()

    def block_read(self, offset, length):
        try:
            return self.b.read_i2c_block_data(i2caddr, offset, length)
        except IOError:
            print("Error detected in function block_read() [IOError = " + str(IOError) + "]")
            sys.exit()

    def get_orientation(self):
        orientation = self.b.read_byte_data(self.a, REG_PL_STATUS) & 0x7
        return orientation

    def getAxisValue(self):
        # Make sure F_READ and F_MODE are disabled.
        f_read = self.b.read_byte_data(self.a, REG_CTRL_REG1) & FLAG_F_READ
        assert f_read == 0, 'F_READ mode is not disabled. : %s' % (f_read)
        f_mode = self.b.read_byte_data(self.a, REG_F_SETUP) & FLAG_F_MODE_FIFO_TRIGGER
        assert f_mode == 0, 'F_MODE mode is not disabled. : %s' % (f_mode)

        self.xyzdata = self.block_read(REG_OUT_X_MSB, 6)
        if self.high_res_mode is not None:
            x = ((self.xyzdata[0] << 8) | self.xyzdata[1]) >> 2
            y = ((self.xyzdata[2] << 8) | self.xyzdata[3]) >> 2
            z = ((self.xyzdata[4] << 8) | self.xyzdata[5]) >> 2
            precision = PRECISION_14_BIT  # Precision 14 bit data
        else:
            x = (self.xyzdata[0] << 8)
            y = (self.xyzdata[1] << 8)
            z = (self.xyzdata[2] << 8)
            precision = PRECISION_08_BIT  # Precision 08 bit data
        max_val = 2 ** (precision - 1) - 1
        signed_max = 2 ** precision
        #
        x -= signed_max if x > max_val else 0
        y -= signed_max if y > max_val else 0
        z -= signed_max if z > max_val else 0
        #
        x = round((float(x)) / RANGE_DIVIDER[self.sensor_range], 3)
        y = round((float(y)) / RANGE_DIVIDER[self.sensor_range], 3)
        z = round((float(z)) / RANGE_DIVIDER[self.sensor_range], 3)
        x= 2.0*x; y=2.0*y; z = 2.0*z
        return {"x": x, "y": y, "z": z}

    def debugShowRpiInfo(self):
        #print("Raspberry Info      = " + str(GPIO.RPI_INFO))
        print("Raspberry Info      = " + str(self.raspiInfo))

    def debugShowRegisters(self):
        print("REG_STATUS       (0x00):" + str(format(self.readRegister(REG_STATUS), '#04x')) + " | Binary: " + format(self.readRegister(REG_STATUS), 'b').zfill(8))
        print("REG_WHOAMI       (0x0d):" + str(format(self.readRegister(REG_WHOAMI), '#04x')) + " | Binary: " + format(self.readRegister(REG_WHOAMI), 'b').zfill(8))
        print("REG_F_SETUP      (0x09):" + str(format(self.readRegister(REG_F_SETUP), '#04x')) + " | Binary: " + format(self.readRegister(REG_F_SETUP), 'b').zfill(8))
        print("REG_XYZ_DATA_CFG (0x0e):" + str(format(self.readRegister(REG_XYZ_DATA_CFG), '#04x')) + " | Binary: " + format(self.readRegister(REG_XYZ_DATA_CFG), 'b').zfill(8))
        print("REG_CTRL_REG1    (0x2a):" + str(format(self.readRegister(REG_CTRL_REG1), '#04x')) + " | Binary: " + format(self.readRegister(REG_CTRL_REG1), 'b').zfill(8))
        print("REG_CTRL_REG2    (0x2b):" + str(format(self.readRegister(REG_CTRL_REG2), '#04x')) + " | Binary: " + format(self.readRegister(REG_CTRL_REG2), 'b').zfill(8))
        print("REG_CTRL_REG3    (0x2c):" + str(format(self.readRegister(REG_CTRL_REG3), '#04x')) + " | Binary: " + format(self.readRegister(REG_CTRL_REG3), 'b').zfill(8))
        print("REG_CTRL_REG4    (0x2d):" + str(format(self.readRegister(REG_CTRL_REG4), '#04x')) + " | Binary: " + format(self.readRegister(REG_CTRL_REG4), 'b').zfill(8))
        print("REG_CTRL_REG5    (0x2e):" + str(format(self.readRegister(REG_CTRL_REG5), '#04x')) + " | Binary: " + format(self.readRegister(REG_CTRL_REG5), 'b').zfill(8))
        print("REG_PL_STATUS    (0x10):" + str(format(self.readRegister(REG_PL_STATUS), '#04x')) + " | Binary: " + format(self.readRegister(REG_PL_STATUS), 'b').zfill(8))
        print ("debugRealTime    " + str(runTimeConfigObject.debugRealTime))
        print ("NumInterrupts    " + str(runTimeConfigObject.NumInterrupts))

    def debugShowOrientation(self):
        print("Position = %d" % (self.get_orientation()))

    def debugShowAxisAcceleration(self, xaccel, yaccel, zaccel):
        print("   x (m/s2)= %+.3f" % (xaccel))
        print("   y (m/s2)= %+.3f" % (yaccel))
        print("   z (m/s2)= %+.3f" % (zaccel))    

if __name__ == "__main__":
    class runTimeConfigObject(object):
        pass
    runTimeConfig = runTimeConfigObject()
    runTimeConfigObject.debugRealTime = 0   # 1 = Show realtime interrupt data
    runTimeConfigObject.executeSilently = 0 # 1 = Execute silently 
    runTimeConfigObject.NumInterrupts = 0   # keep Nbr sensor interpts in main loop
    
    MMA8451 = Accel()
    MMA8451.init()

    while True:  # forever loop
        if runTimeConfigObject.executeSilently == 0:
            #print ("\nCurrent Date-Time: " + str(datetime.datetime.now()))
            #print ("Raspberry Bus       = " + str(MMA8451.raspiBus))
            #print ("Raspberry Interrupt = " + str(MMA8451.raspiIntEnabled))
            #print ("Number of elemets   = " + str(len(accelBuffer)))
            #MMA8451.debugShowRpiInfo()
            #MMA8451.debugShowRegisters()
            MMA8451.debugShowOrientation()
            axes = MMA8451.getAxisValue()
            MMA8451.debugShowAxisAcceleration(axes['x'], axes['y'], axes['z'])    
        runTimeConfigObject.NumInterrupts = 0
        try:
            time.sleep(1.0)
        except KeyboardInterrupt:
            time.sleep(1.0)
            sys.exit()
    sys.exit()

