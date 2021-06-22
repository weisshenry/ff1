import sys, os,time, shutil
import numpy as np
import pdb
 
accCsv= 'ca21.csv'
expCsv= 'ex21.csv'
chkTxt=  'check21.txt'
kywd=['BRITTANY','WAL-MART','TELEPHO','PAULDING',\
      'Prime Video','S & S','DEB SCHROEDER',"CHERRY'S",\
      'BRICKNER CONS', 'OMIG','TRACTOR SUPPLY','SCHROEDER AND CO',\
      'GLANDORF WAREHOUSE','KODY KUHLMAN','WATER SOLUTIONS',\
      'PUTNAM COUNTY TREA']

def findit(glin,amt,dat,txt):
   k = len(glin)
   #pdb.set_trace()
   gotit=0
   ww = 99
   for i in range(len(kywd)):
      xx = txt.find(kywd[i])      
      if xx > -1:
         gotit =1         
         ww = i
         print(' found keyword %s ' %(kywd[i]))
         break
   if gotit==0:
       print(' did not find keyword')
       #pdb.set_trace()
       return 0;   
   for lina in glin:
      linb = lina.rstrip()
      itm = linb.split(',')
      try:      
         amt2 = float(itm[2])      
      except:
         amt2= 0.0      
      dat2 = itm[0]
      txt2 = itm[1]
      yy = txt2.find(kywd[ww])     
      #if ((yy > -1) and (dat2==dat) and (amt2==amt)):
      if ((yy > -1) and (dat2==dat)):     
         return 1
      elif yy > -1:
         print(' dat2 %s  dat %s  txt2 %s '%(dat2,dat,txt2))
   print(' no match for %s ' %(txt))   
   #pdb.set_trace()   
   return 0        

def proces1(fx,gx,hx):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(gx,'r') 
   h1 = open(hx,'w') 
   flin = f1.readlines()
   glin = g1.readlines()
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
         print('xx %s %s ' %(dat,txt))   
         #pdb.set_trace()         
         jj =0
         if (len(dat) > 7):
            jj = findit(glin,amt,dat,txt) 
            print(' ret')
            #pdb.set_trace()
         if jj:         
            h1.write('  %s %9.2f  %s\n' %(dat,float(amt),txt))  
         elif (len(dat) > 7):
            h1.write('--%s %9.2f  %s\n' %(dat,float(amt),txt)) 
            #pdb.set_trace()
         else: 
            h1.write('  %s\n' %(linb))          
   f1.close()   
   g1.close() 
   h1.close()   
   return 

if __name__ == "__main__":
   print(' start')      
   proces1(accCsv,expCsv,chkTxt)    
   print('   end ')   
   sys.exit()  
 

