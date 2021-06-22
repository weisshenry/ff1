# top1.py  Process accounts
# Notes:  save expenses.odt as a csv file
#    field delim:  space     string delim: " 
#  expenses fmt:  date  info  amt   (info needs 2 words <-bug)
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
   g3.write('      Cash All Activity 2021 \n\n')
   g3.close()   
   proc('cashflow','Cashflow',allCash,2)  
   proc('guesth','Guesthouse 9206',allCash,2)  
   proc('main','Mainhouse 0501',allCash,2)  
   proc('con','Construction 0509',allCash,2)  
   proc('farm','Farm 0584',allCash,2)    
   print('   end part1, start recon')   
   sys.exit()  
 

