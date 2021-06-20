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
acctTxt= './out1/CashAcct21.txt'
exptTxt= './out1/CashExpt21.txt'
allCash= './out1/CashAll_21.txt'

def proces0(fx,gx):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(gx,'a')    
   g2 = open(exptTxt,'a')  
   f1lines = f1.readlines()
   for lina in f1lines:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm) 
      xx = linb.find('<Date>')
      w1 = linb.find('XX0501')   
      w2 = linb.find('XX0509')
      w3 = linb.find('XX2638')
      w4 = linb.find('XX0584')
      w5 = linb.find('TRANSFER TO LOAN')
      w6 = not(( w1 > -1) or (w2 > -1) or (w3 > -1) or (w4 > -1) or (w5 > -1))
      y1 = linb.find('GLANDORF TELE')
      y2 = linb.find('PAULDING PUT')
      y3 = linb.find("CHERRY'S PRO")
      y4 = linb.find('S & S SAN')
      y5 = linb.find('OMIG')
      y6 = linb.find('TRACTOR SUPPLY')
      y7 = linb.find('Prime Video')
      y8 = linb.find('WAL-MART')
      y9 = linb.find('PUTNAM COUNTY')
      y10 = linb.find('VAN WERT')
      z1 = ((y1 > -1) or (y2 > -1) or (y3 > -1) or (y4 > -1) or (y5  > -1))
      z2 = ((y6 > -1) or (y7 > -1) or (y8 > -1) or (y9 > -1) or (y10 > -1))
      z3 = z1 or z2
      if ((xx == -1) and (len(linb) >2)):
         if ((lx > 3) and (xx == -1)) : 
            if itm[4] =='':
               amt = float(itm[3])      
            else: 
               amt = float(itm[4]) 
            if (amt < 0):    
               if (z3):          
                  g1.write('%s %8.2f  %s\n' %(itm[0],amt,itm[5][0:60]))              
               elif (w6) :
                  g2.write('%s %8.2f  %s\n' %(itm[0],amt,linb))                   
   f1.close()   
   g1.close()
   g2.close()   
   return  

def proces1(fx,gx,opt):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(gx,'a') 
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
   if opt:
      gx= open(acctTxt,'a')
      gx.write('\n              '+nam1+' Account Activity 2021  \n\n')
      gx.close() 
   for i in range(12,9,-1):
      xnam =banktop+nam+str(i)+'.csv'    
      if os.path.isfile(xnam): 
         if opt==0:      
            proces0(xnam,gfile) 
         else:
            proces1(xnam,gfile,opt)         
   for i in range(9,0,-1): 
      xnam =banktop+nam+'0'+str(i)+'.csv'     
      if os.path.isfile(xnam):            
         if opt==0:      
            proces0(xnam,gfile) 
         else:
            proces1(xnam,gfile,opt) 
   return   

if __name__ == "__main__":
   print(' start')  
   conv1.conv1()   
   if not os.path.exists('out1'):
      os.mkdir('out1')    
   g1= open(acctTxt,'w');   g1.close() 
   g2= open(exptTxt,'w')
   g2.write('      Cash flow unaccounted 2021 \n\n')
   g2.close()  
   g3= open(allCash,'w')
   g3.write('      Cash All Activity 2021 \n\n')
   g3.close()   
   proc('con','Construction',allCash,2) 
   proc('cashflow','Cashflow',allCash,2)     
   proc('cashflow','Cashflow',acctTxt,0)  
   proc('guesth','Guesthouse 9206',acctTxt,1)
   proc('main','Mainhouse 0501',acctTxt,1)   
   proc('con','Construction 0509',acctTxt,1) 
   proc('farm','Farm 0584',acctTxt,1)     
   print('   end part1, start recon')   
   sys.exit()  
 

