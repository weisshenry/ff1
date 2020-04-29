# topAcct1.py  Process accounts
import sys, os,time, shutil
from datetime import datetime
import numpy as np
from dateutil import parser
import re
#import pudb

filex='../st1/expenses20.csv'
filet='../st1/expenses20.txt'

def cleanit(filea,fileb): 
   fx = open(filea,'rb')
   gx = open(fileb,'w+b')
   dat = fx.read() 
   datx = bytearray(dat)
   lx = 0
   lx = len(dat)  
   for i in range(lx):
      if (datx[i] ==0x96):
         datx[i] = 0x20 
      if (datx[i] ==0x92):
         datx[i] = 0x20    
   gx.write(datx)
   fx.close() 
   gx.close()
   return lx

def findit(amt,dd):
   #print(' start of findit %s' %(amt))      
   try:      
      fx = open(filet,'r') 
      lines = fx.readlines()
      fx.close()      
   except:
      print('  File %s not found ' %(filet))      
      return -2     
   la = len(lines)     
   for i in range(la):         
      lina = lines[i]
      lina = lina.rstrip()
      x1 = lina.find(amt)          
      if x1 > -1:               
         match = re.findall('\d{2}/\d{2}/\d{2}', lina)        
         dx = datetime.strptime(match[0],"%m/%d/%y")                         
      if ((x1>-1) and (len(match)==1)):
         #print('  got it ')                   
         return 1
   #print(' end of findit search')   
   return 0
    
def recon1():
   print('   Start - reconciled accounts')   
   lx = cleanit(filex,filet)
   if (lx < 5):
       print(' Error: %s not found' %(fielex))
       return -1
   fnam2='Accounts2020t.txt'  # reconciled 
   hx = open(fnam2,'w')
   hx.write('        Accounts reconciled 2020 \n\n')
   fnam1='Accounts2020s.txt'
   gx = open(fnam1,'r')
   lines = gx.readlines()
   lx = len(lines)
   ct =0   
   errx =0
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
         #print('  going to finditx')         
         x = findit(amt,dd)
         ct = ct+1
         if x > 0:
            hx.write('.  %s\n' %(linb))
         elif x==0:
            hx.write('-->%s\n' %(linb))
         else:
            errx = 1         
      except:
         continue 
      if errx==1:
         break      
   hx.close()        
   gx.close()
   if errx==1: 
      print('  Error processing records %s ' %(filet))  
      return -2
   else:      
      print('   Processed %d records' %(ct))   
   return 0  
 

