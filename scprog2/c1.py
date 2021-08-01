#   a1.py  -->  input:  all accts in st1
#              output:  out1/CashAll_21.txt  all bank transactions
#   b1.py  -->  input:  all accts in st1
#              output:  accounted for ca21.txt
#              output:  unaccounted for out2/CashExct.txt 
#   c1.py  -->  input:  ca21.txt  Sorted import from all bank statements
#                       ex21.txt  Paper trail - manually compiled
#              Output:  check21.txt  Issues on ca21.txt which should be 
#                       entered on paper trail. 
# glin = list of all date-desc-amts to find in the master list of keywords 
# from ca21.txt glin needs 'cleaned' of comments, so only has date-desc-amts
import sys, os,time, shutil
import numpy as np
import pdb
 
ca21Ttxt= 'ca21.txt'    # INPUT
ex21Txt= 'ex21.txt'    # INPUT
check21= 'check21.txt' # Output
kywd=['BRITTANY','WAL-MART','TELEPHO','PAULDING',\
      'Prime Video','S & S','DEB SCHROEDER',"CHERRY'S",\
      'BRICKNER CONS', 'OMIG','TRACTOR SUPPLY','SCHROEDER AND CO',\
      'GLANDORF WAREHOUSE','KODY KUHLMAN','WATER SOLUTIONS',\
      'PUTNAM COUNTY TREA','GREG BROWN','POWER HOUSE',\
      'ALLEN SCHROEDER',"ELLERBROCK'S PLUMB", 'OHIO SANITARY', 'VAN WERT CARTS']

def findit(glin,amt,dat,txt):
   k = len(glin)   
   gotit=0
   ww = 99
   for i in range(len(kywd)):
      xx = txt.find(kywd[i])      
      if xx > -1:
         gotit =1         
         ww = i
         #print(' found keyword %s ' %(kywd[i]))
         break
   if gotit==0:
       #print(' did not find keyword')      
       return 0;   
   for lina in glin:
      linb = lina.rstrip()
      itm = linb.split(',')
      try:      
         amt2 = float(itm[2])      
      except:
         amt2= 0.0      
      dat2 = itm[0]
      try:
         txt2 = itm[1]
      except:
         print('ERR: %s ' %(linb))
         pdb.set_trace()      
      yy = txt2.find(kywd[ww])     
      #if ((yy > -1) and (dat2==dat) and (amt2==amt)):
      if ((yy > -1) and (dat2==dat)):     
         return 1      
   print(' no match for %s ' %(txt))       
   return 0 

def cleaned(glin):
   gline = []
   for i in range(len(glin)): 
      glinx = glin[i].rstrip()   
      itm = glinx.split(',')     
      lx = len(itm)  
      x = itm[0].find('/')
      if ((x > -1) and (lx > 2)):
         gline.append(glinx)  
   print('   before: %d  after: %d ' %(len(glin),len(gline)))    
   return gline      

def proces1(ca21Ttxt,ex21Txt,check21):
   print('   Input: %s, %s  Output:  %s' %(ca21Ttxt,ex21Txt,check21))  
   f1= open(ca21Ttxt,'r')
   g1 = open(ex21Txt,'r') 
   h1 = open(check21,'w') 
   flin = f1.readlines()
   glin = g1.readlines()  
   glin = cleaned(glin)
   for lina in flin:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm)           
      if (lx > 2): 
         try:
           amt = float(itm[2])      
         except:
           amt =0.0
         dat = itm[0]        
         txt = itm[1]                 
         jj =0
         if (len(dat) > 7):
            jj = findit(glin,amt,dat,txt)            
         if jj:         
            h1.write('  %s %-60s %10.2f \n' %(dat,txt,float(amt)))  
         elif (len(dat) > 7):
            h1.write('--%s %-60s %10.2f \n' %(dat,txt,float(amt)))             
         else: 
            h1.write('  %s\n' %(linb))          
   f1.close()   
   g1.close() 
   h1.close()   
   return 

if __name__ == "__main__":
   print('   start')      
   proces1(ca21Ttxt,ex21Txt,check21)    
   print('   end ')   
   sys.exit()  
 

