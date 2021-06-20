# top1.py  Process accounts
# Notes:  save expenses.odt as a csv file
#    field delim:  space     string delim: " 
#  expenses fmt:  date  info  amt   (info needs 2 words <-bug)
import sys, os,time, shutil
import numpy as np
import conv1
import pdb

db=0 
banktop = './st1/'                # bank csv files
acctTxt= './out1/BankAccts2021.txt'

def proces(fx,acctTxt):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(acctTxt,'a') 
   f1lines = f1.readlines()
   for lina in f1lines:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm) 
      xx = linb.find('<Date>')      
      if ((lx > 3) and (xx == -1)) : 
         if itm[4] =='':
           amt = float(itm[3])      
         else: 
           amt = float(itm[4])           
         #g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][0:40]))
         g1.write('%10.2f -- %s\n' %(amt,linb[0:100]))
      else:
         xx = linb.find('<Date>')        
         if ((len(linb) > 2) and (xx == -1)):
            g1.write('--%s\n' %(linb))
   f1.close()   
   g1.close()      
   return 

def topproc(nam,nam1,acctTxt):
   gx= open(acctTxt,'a')
   gx.write('\n              '+nam1+' Account Activity 2021  \n\n')
   gx.close()
   for i in range(12,9,-1):
      xnam =banktop+nam+str(i)+'.csv'    
      if os.path.isfile(xnam):            
         proces(xnam,acctTxt)
   for i in range(9,0,-1): 
      xnam =banktop+nam+'0'+str(i)+'.csv'     
      if os.path.isfile(xnam):            
         proces(xnam,acctTxt)
   return   

if __name__ == "__main__":
   print(' start')  
   conv1.conv1()   
   if not os.path.exists('out1'):
      os.mkdir('out1')    
   gx= open(acctTxt,'w')
   gx.close()     
   topproc('cashflow','Cashflow',acctTxt)  
   topproc('guesth','Guesthouse 9206',acctTxt)
   topproc('main','Mainhouse 0501',acctTxt)   
   topproc('con','Construction 0509',acctTxt) 
   topproc('farm','Farm 0584',acctTxt)     
   print('   end part1, start recon')   
   sys.exit()  
 

