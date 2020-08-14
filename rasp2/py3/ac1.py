import os
import sys
import time
import datetime
import board
import busio
import digitalio
import adafruit_mma8451
import pdb


if __name__ == "__main__":
   i2c = busio.I2C(board.SCL, board.SDA) 
   time.sleep(1)
   sensor = adafruit_mma8451.MMA8451(i2c)
   sensor.range = adafruit_mma8451.RANGE_2G
   a=[];b=[];c=[]
   for i in range(20):
      x,y,z= sensor.acceleration
      a.append(x);b.append(y);c.append(z)
   print(' hello')
   for i in range(20):
      print('%f ' %(c[i]))
   #pdb.set_trace()   
   sys.exit()
   