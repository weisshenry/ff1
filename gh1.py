# ff process1
import sys, os,time, shutil
import numpy as np
import pdb

def proces(fnam):
   print(' start')
   f1= open(fnam,'r')
   g1 = open('g1.txt','a')  
   f1lines = f1.readlines()
   #g1.write('--Process %s lines %d \n' %(fnam,len(f1lines)))
   for lina in f1lines:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm)
      #for i in range(lx):
      #   print(' %d %s ' %(i,itm[i]))
      x1 = itm[0]=='<Date>'          
      if ((lx > 3) and (not x1)):                
         dsc = itm[2]
         b1 = dsc.find('BILL PAYMENT') 
         b2 = dsc.find('INTERNET/PHONE TRSFR') 
         b3 = dsc.find('SERVICE CHARGE') 
         b4 = dsc.find('PREAUTHORIZED ') 
         b9 = itm[5].find('XXXXXXX4735')            
         if b1 > -1:
            dsc = dsc.replace('BILL PAYMENT','BILL PAY') 
         elif b2 > -1:
            dsc = dsc.replace('INTERNET/PHONE TRSFR','INTERNET') 
         elif b3 > -1:
            dsc = dsc.replace('SERVICE CHARGE','SVC CHG') 
         elif b4 > -1:
            dsc = dsc.replace('PREAUTHORIZED ','')             
         if b9 > -1:
            itm[5] = 'CASHFLOW'                        
         dsc = dsc.ljust(10)           
         if itm[4] == '':         
            amt = float(itm[3])  
         else:
            amt = float(itm[4])         
         ck  = itm[2]  
         g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][0:40]))            
   f1.close()   
   g1.close()   
   print('  end')     

if __name__ == "__main__":
   print(' start')
   gx= open('g1.txt','w')
   gx.write('              Guesthouse Account Activity 2020  \n\n')
   gx.close()
   fa = '../st3/guesth03.csv'  
   proces(fa);
   fb = '../st3/guesth02.csv'
   proces(fb);
   fc = '../st3/guesth01.csv'
   proces(fc);
   print('  end')   
   sys.exit()  
 

