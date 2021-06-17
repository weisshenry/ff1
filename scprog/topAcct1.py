# topAcct1.py  Process accounts
# Notes:  save expenses.odt as a csv file
#    field delim:  space     string delim: " 
#  expenses fmt:  date  info  amt   (info needs 2 words <-bug)
import sys, os,time, shutil
import numpy as np
sys.path.append('./prog1')
import pdb
import cashFlow1
import proces1
import recon2
import sortit1
import conv1

db=0 
banktop = './st1/'                # bank csv files
acctTxt= './out2/BankAccts2021.txt'
acctSort='./out1/BankAcct2021_sorted.txt' 
acctRecon='./out2/Reconciled.txt'  # reconciled
acctReconSort='./out1/Reconciled_sort.txt'  # sorted

def topproc(nam,nam1,acctTxt,acctSort):
   gx= open(acctTxt,'a')
   gx.write('\n              '+nam1+' Account Activity 2020  \n\n')
   gx.close()
   gy= open(acctSort,'a')
   gy.write('\n              '+nam1+' Account Activity 2020 shortform \n\n')
   gy.close()
   for i in range(12,9,-1):
      xnam =banktop+nam+str(i)+'.csv'
      if (db):
         print('     input file %s' %(xnam))
      if os.path.isfile(xnam):            
         proces1.proces(xnam,acctTxt,acctSort)
   for i in range(9,0,-1): 
      xnam =banktop+nam+'0'+str(i)+'.csv'
      if (db):
         print('     input file %s' %(xnam))
      if os.path.isfile(xnam):            
         proces1.proces(xnam,acctTxt,acctSort)

   return   

if __name__ == "__main__":
   print(' start')
   conv1.conv1()
   if not os.path.exists('out1'):
      os.mkdir('out1')   
   if not os.path.exists('out2'):
      os.mkdir('out2')  
   gx= open(acctTxt,'w')
   gx.close()   
   gy= open(acctSort,'w')
   gy.write('     Premier Bank Accounts:  2021  \n')
   gy.close()
   cashFlow1.topcash(acctTxt,acctSort)
   topproc('guesth','Guesthouse 9206',acctTxt,acctSort)
   topproc('main','Mainhouse 0501',acctTxt,acctSort)   
   topproc('con','Construction 0509',acctTxt,acctSort) 
   topproc('farm','Farm 0584',acctTxt,acctSort)     
   print('   end part1, start recon') 
   ret = recon2.recon1(acctSort,acctRecon)    
   if ret < 0:
      print('  error recon %d' %(ret))
   sortit1.sortit1(acctRecon,acctReconSort) 
   sys.exit()  
 

