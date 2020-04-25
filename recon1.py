# topAcct1.py  Process accounts
import sys, os,time, shutil
from datetime import datetime
import numpy as np
from dateutil import parser
import re
#import pudb

def findit(amt,dd):
   #print(' start of findit %s' %(amt))
   #pu.db
   fnam3='../st1/expenses20.txt' 
   try:
      fx = open(fnam3,'r') 
   except:
      print('  File %s not found ' %(fnam3))
      sys.exit()      
   lines = fx.readlines()
   fx.close()
   la = len(lines)   
   for i in range(la):         
      lina = lines[i]
      lina = lina.rstrip()
      x1 = lina.find(amt) 
      #pu.db      
      if x1 > -1:               
         match = re.findall('\d{2}/\d{2}/\d{2}', lina)        
         dx = datetime.strptime(match[0],"%m/%d/%y")                         
      if ((x1>-1) and (len(match)==1)):
         #print('  got it ')                   
         return 1
   #print(' end of findit search') 
   #pdb.set_trace()   
   return 0
    
def recon1():
   print('   Start - reconciled accounts')   
   fnam2='Accounts2020t.txt'  # reconciled 
   hx = open(fnam2,'w')
   fnam1='Accounts2020s.txt'
   gx = open(fnam1,'r')
   lines = gx.readlines()
   lx = len(lines)
   ct =0   
   for i in range(lx):
      lina = lines[i]
      linb = lina.rstrip() 
      amt = linb[21:31]
      amt = amt.rstrip()
      amt = amt.lstrip()
      amt = amt[1:len(amt)]
      date=linb[0:8] 
      try:
         dd = datetime.strptime(date,"%m/%d/%y")       
         famt = float(amt)       
         #print('  going to findit')
         x = findit(amt,dd)
         ct = ct+1
         if x:
            hx.write('.  %s\n' %(linb))
         else:
            hx.write('-->%s\n' %(linb))            
      except:
         continue 
   hx.close()        
   gx.close()    
   print('   Processed %d records' %(ct))   
   sys.exit()  
 

