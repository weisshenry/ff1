# topAcct1.py  Process accounts
# Notes:  save expenses.odt as a csv file
#    field delim:  space     string delim: " 
#  expenses fmt:  date  info  amt   (info needs 2 words <-bug)
import sys, os,time, shutil
import numpy as np
import pdb
import cashFlow1
import proces1
import recon1
db=0 
fnam= './out1/Accounts2020.txt'
fnams='./out1/Accounts2020_sorted.txt' 
fnamR='./out1/Reconciled.txt'  # reconciled

def topproc(nam,nam1,fnam,fnams):
   gx= open(fnam,'a')
   gx.write('\n              '+nam1+' Account Activity 2020  \n\n')
   gx.close()
   gy= open(fnams,'a')
   gy.write('\n              '+nam1+' Account Activity 2020 shortform \n\n')
   gy.close()
   for i in range(12,9,-1):
      xnam ='../st1/'+nam+str(i)+'.csv'
      if (db):
         print('     input file %s' %(xnam))
      if os.path.isfile(xnam):            
         proces1.proces(xnam,fnam,fnams)
   for i in range(9,0,-1): 
      xnam ='../st1/'+nam+'0'+str(i)+'.csv'
      if (db):
         print('     input file %s' %(xnam))
      if os.path.isfile(xnam):            
         proces1.proces(xnam,fnam,fnams)

   return   

if __name__ == "__main__":
   print(' start')     
   gx= open(fnam,'w')
   gx.close()   
   gy= open(fnams,'w')
   gy.close()
   cashFlow1.topcash(fnam,fnams)
   topproc('guesth','Guesthouse',fnam,fnams)
   topproc('main','Mainhouse',fnam,fnams)   
   topproc('con','Construction',fnam,fnams) 
   topproc('farm','Farm',fnam,fnams)     
   print('  end part1, start recon') 
   ret = recon1.recon1(fnams,fnamR)   
   if ret < 0:
      print('  error recon %d' %(ret))
   sys.exit()  
 

