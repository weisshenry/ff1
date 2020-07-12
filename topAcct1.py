# topAcct1.py  Process accounts
# Notes:  save expenses.odt as a csv file
#    field delim:  space     string delim: " 
#  expenses fmt:  date  info  amt   (info needs 2 words <-bug)
import sys, os,time, shutil
import numpy as np
import pdb
import cashFlow1
import proces1
import recon2
db=0 
acctTxt= './out1/Accounts2020.txt'
acctSort='./out1/Accounts2020_sorted.txt' 
acctRecon='./out1/Reconciled.txt'  # reconciled

def topproc(nam,nam1,acctTxt,acctSort):
   gx= open(acctTxt,'a')
   gx.write('\n              '+nam1+' Account Activity 2020  \n\n')
   gx.close()
   gy= open(acctSort,'a')
   gy.write('\n              '+nam1+' Account Activity 2020 shortform \n\n')
   gy.close()
   for i in range(12,9,-1):
      xnam ='../st1/'+nam+str(i)+'.csv'
      if (db):
         print('     input file %s' %(xnam))
      if os.path.isfile(xnam):            
         proces1.proces(xnam,acctTxt,acctSort)
   for i in range(9,0,-1): 
      xnam ='../st1/'+nam+'0'+str(i)+'.csv'
      if (db):
         print('     input file %s' %(xnam))
      if os.path.isfile(xnam):            
         proces1.proces(xnam,acctTxt,acctSort)

   return   

if __name__ == "__main__":
   print(' start')     
   gx= open(acctTxt,'w')
   gx.close()   
   gy= open(acctSort,'w')
   gy.close()
   cashFlow1.topcash(acctTxt,acctSort)
   topproc('guesth','Guesthouse',acctTxt,acctSort)
   topproc('main','Mainhouse',acctTxt,acctSort)   
   topproc('con','Construction',acctTxt,acctSort) 
   topproc('farm','Farm',acctTxt,acctSort)     
   print('  end part1, start recon') 
   ret = recon2.recon1(acctSort,acctRecon)   
   if ret < 0:
      print('  error recon %d' %(ret))
   sys.exit()  
 

