# recon1.py  Reconcile all accounts
import sys, os,time, shutil
from datetime import datetime
import numpy as np
from dateutil import parser
import re
#import pudb
import pdb
vb = False

#acctReco='../out1/Reconciled.txt'       # reconciled
#acctSort='../out1/Reconciled_sort.txt'  # sorted

def sortit1(acctReco,acctSort):
   print('   Start - reconciled accounts')  
   #pdb.set_trace()
   gx = open(acctReco,'r')
   hx = open(acctSort,'w')
   linesa = gx.readlines()
   gx.close() 
   la = len(linesa)
   #pdb.set_trace()
   linesb =[]
   for i in range(3,la):
      linesb.append(linesa[i])
   linesb = sorted(linesb, key=lambda x: x[4:12])   
   #linesb.sort()   
   for i in range(3):
      hx.write(linesa[i])          
   for i in range(la-3):
      hx.write(linesb[i])     
   hx.close()  
   return 0  
   
# if __name__ == "__main__":
   # print(' start')
   # recon1(acctReco,acctSort)
   # print(' end')
   # sys.exit()

