# topAcct1.py  Process accounts
import sys, os,time, shutil
import numpy as np
import pdb
import cashFlow1

def proces(fx,fnam):
   print(' start')
   f1= open(fx,'r')
   g1 = open(fnam,'a')  
   #pdb.set_trace()
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
         b1 = itm[2].find('BILL PAYMENT') 
         b2 = itm[2].find('INTERNET/PHONE TRSFR') 
         b3 = itm[2].find('SERVICE CHARGE') 
         b4 = itm[2].find('PREAUTHORIZED ') 
         b5 = itm[2].find('MOBILE DEPOSIT') 
         b6 = itm[2].find('INTEREST CREDIT') 
         b9 = itm[5].find('XXXXXXX4735')            
         if b1 > -1:
            itm[2] = itm[2].replace('BILL PAYMENT','BILL PAY') 
         elif b2 > -1:
            itm[2] = itm[2].replace('INTERNET/PHONE TRSFR','INTERNET') 
         elif b3 > -1:
            itm[2] = itm[2].replace('SERVICE CHARGE','SVC CHG') 
         elif b4 > -1:
            itm[2] = itm[2].replace('PREAUTHORIZED ','')    
         elif b5 > -1:
            itm[2] = itm[2].replace('MOBILE DEPOSIT','MOBILE DPT')  
         elif b6 > -1:
            itm[2] = itm[2].replace('INTEREST CREDIT','INTEREST')              
         if b9 > -1:
            itm[5] = 'CASHFLOW'                        
         itm[2] = itm[2].ljust(10)           
         if itm[4] == '':         
            amt = float(itm[3])  
         else:
            amt = float(itm[4])         
         ck  = itm[2]  
         g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][0:40]))            
   f1.close()   
   g1.close()   
   print('  end')  

def topproc(nam,nam1,fnam):
   gx= open(fnam,'a')
   gx.write('\n              '+nam1+' Account Activity 2020  \n\n')
   gx.close()
   fa = '../st3/'+nam+'03.csv'  
   proces(fa,fnam);
   fb = '../st3/'+nam+'02.csv' 
   proces(fb,fnam);
   fc = '../st3/'+nam+'01.csv' 
   proces(fc,fnam);
   return   

if __name__ == "__main__":
   print(' start')
   cashFlow1.topcash()
   fnam='Accounts2020.txt'
   gx= open(fnam,'w')
   gx.close()
   topproc('guesth','Guesthouse',fnam)
   topproc('main','Mainhouse',fnam)   
   topproc('con','Construction',fnam) 
   topproc('farm','Farm',fnam)     
   print('  end')   
   sys.exit()  
 

