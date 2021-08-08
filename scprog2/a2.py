# step1: Premier bank web site ----------------
#	1 All; 2 Transactions ;	3 Download
# step2:  
#   a1.py  -->  input:  all accts in st1
#              output:  out1/CashAll_21.txt  all bank transactions
#                       sanity check on cash transactions
#   b1.py  -->  input:  processes all accts in st1
#              output:  accounted for ca21.txt
#              output:  unaccounted for out2/CashExct.txt 
#   c1.py  -->  input:  ca21.txt  Sorted import from all bank statements
#                       ex21.txt  Paper trail - manually compiled
#              Output:  check21.txt  Issues on ca21.txt which should be 
#                       entered on paper trail. 
# step3: enter these into ex21, and rerun c1.py; need CSV format
# TODO report any empty bank statements
import sys, os,time, shutil
import numpy as np
import pdb

db=0 
banktop = './st1/'                # bank csv files
allCash= './out1/CashAll_21.txt'

def proces1(fx,gx,opt):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(gx,'a')  
   g1.write('\n\n %s \n' %(fx))   
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
         if ((opt ==1) and (amt < 0)):            
            g1.write('%s %8.2f  %s\n' %(itm[0],amt,itm[5][0:60]))             
         elif (opt ==2):  # for all cash transactions           
            g1.write('%s %9.2f  %s\n' %(itm[0],amt,linb[10:100]))           
   f1.close()   
   g1.close()     
   return 

def proc(nam,nam1,gfile,opt): 
   for i in range(12,9,-1):
      xnam =banktop+nam+str(i)+'.csv'    
      if os.path.isfile(xnam): 
         proces1(xnam,gfile,opt)         
   for i in range(9,0,-1): 
      xnam =banktop+nam+'0'+str(i)+'.csv'     
      if os.path.isfile(xnam):            
         proces1(xnam,gfile,opt) 
   return   

if __name__ == "__main__":
   print(' start')  
   if not os.path.exists('out1'):
      os.mkdir('out1') 
   g3= open(allCash,'w')
   g3.write('      Cash All Activity 2021 - out1/CashAll_21.txt  \n\n')
   g3.close()   
   proc('cashflow','Cashflow',allCash,2)  
   proc('guesth','Guesthouse 9206',allCash,2)  
   proc('main','Mainhouse 0501',allCash,2)  
   proc('con','Construction 0509',allCash,2)  
   proc('farm','Farm 0584',allCash,2)    
   print('   end part1, start recon')   
   sys.exit()  
 

