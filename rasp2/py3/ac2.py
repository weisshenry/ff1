# at 200 Hz, eliminate duplicates
import os
import sys
import time
import math
import datetime
import board
import busio
import digitalio
import adafruit_mma8451
import pdb

NMB = 1000

if __name__ == "__main__":
   i2c = busio.I2C(board.SCL, board.SDA) 
   t1 = time.time()
   time.sleep(1)
   t2= time.time()
   print('  time %f ' %(t2-t1)) 
   sensor = adafruit_mma8451.MMA8451(i2c)
   sensor.range = adafruit_mma8451.RANGE_2G
   sensor.data_rate = adafruit_mma8451.DATARATE_200HZ
   a=[];b=[];c=[]
   t3 = time.time()  
   for i in range(NMB):
      x,y,z= sensor.acceleration
      a.append(x);b.append(y);c.append(z)
   t4= time.time()
   print('  time %f ' %(t4-t3))  
   for i in range(5):
      print('%f ' %(c[i]))
   fx= open("ca1.txt",'w') 
   x=0;y=0;z=0;
   ct =0
   ct2 = 0
   for i in range(NMB):  
      if ((x==a[i]) and (y==b[i]) and (z==c[i])):
         ct= ct+1;         
      else:  
         fx.write('%d ,%f, %f, %f \n' %(ct2,a[i],b[i],c[i]))
         #fx.write('%d , %f \n' %(ct2,a[i]))
         ct2 = ct2+1;
         x =a[i];y=b[i];z=c[i]         
   fx.close()
   print(' dups  %d ' %(ct))   
   #pdb.set_trace()   
   sys.exit()
   