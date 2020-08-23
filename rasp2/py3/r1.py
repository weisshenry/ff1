# r1 reprocss step 
# input ba1.txt 
import sys
import numpy as np
import scipy.integrate as it
from pandas import read_csv
import matplotlib.pyplot as plt
import pdb

if __name__ == "__main__":
   with open('ba1.txt') as fx:   
      linex = fx.readlines()  
   lx = len(linex)
   n = np.zeros([lx],dtype='float')
   a = np.zeros([lx],dtype='float')
   b = np.zeros([lx],dtype='float')
   c = np.zeros([lx],dtype='float')
   for i in range(lx):
      lina = linex[i]
      x = lina.split(',')
      n[i] = x[0]
      a[i] = x[1]
      b[i] = x[2]
      c[i] = x[3]      
      #print(' %d %f %f %f ' %(int(n),float(a),float(b),float(c)))
   #plt.plot(n,a)
   aa = np.zeros([lx],dtype='float')
   aa = b - np.median(b) -0.0005
   z = it.cumtrapz(aa,n,initial=0)
   plt.plot(n,z)
   plt.show()    
   sys.exit()   
      
     
     