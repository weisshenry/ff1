# conv1 
# convert .ods (OpenDocument spreadsheet) to .csv file
# 12/20/20 HWeiss
import sys, os,time, shutil
import numpy as np
import csv
import pyexcel_ods as pe
import pdb

DG = 1
acctOds= './in1/expenses21.ods'
acctCsv= './in1/expenses21.csv'

def conv1():
   g1 = open(acctCsv,'w')
   rrr = pe.get_data(acctOds)
   sss = dict(rrr) #convert ordered dict to dict
   for key,value in rrr.items(): 
      ttt = value  #convert dict to list (of lists)
   if DG:
      print('   records %d ' %(len(ttt)))   
   for i in range(len(ttt)): 
      uuu=ttt[i]   
      if(len(ttt[i]) == 1):
          g1.write('\n"   %s"\n' %(uuu[0])) 
      if(len(ttt[i]) == 2):
          g1.write('\n"   %s"\n' %(uuu[1]))          
      if(len(ttt[i]) > 2):
         if(DG):      
            print('%d --%s %s %s ' %(i,uuu[0],uuu[1],uuu[2])) 
         #pdb.set_trace()
         vvv = str(uuu[0]) # formatting date yyyy_mm_dd
         www = list(vvv)   # to mm/dd/yy
         xxx = list(vvv)
         if len(www) < 10:
            print(' %d record: %s %s %s Missing date' %(i,uuu[0],uuu[1],uuu[2]))
            sys.exit()            
         www[0] = xxx[5]                    
         www[1] = xxx[6]
         www[2] ='/'
         www[3] = xxx[8]
         www[4] = xxx[9]
         www[5] ='/'   
         www[6] = xxx[2]
         www[7] = xxx[3]         
         yyy = "".join(www)
         yyy = yyy[:-2]   # delete last 2 chars        
      if   (len(ttt[i]) ==3):   
         g1.write('%s "%s" %5.2f \n' %(yyy,uuu[1],float(uuu[2]))) 
         #pdb.set_trace()         
      elif (len(ttt[i]) ==4):   
         g1.write('%s "%s" %5.2f "%s" \n' %(yyy,uuu[1],float(uuu[2]),uuu[3]))
         #pdb.set_trace()         
      elif (len(ttt[i]) > 4):   
         g1.write('%s "%s" %5.2f "%s" "%s" \n' %(yyy,uuu[1],float(uuu[2]),uuu[3],uuu[4]))   
         #pdb.set_trace()
   g1.close()
   return 
 

