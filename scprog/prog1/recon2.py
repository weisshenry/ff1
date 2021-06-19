# recon1.py  Reconcile all accounts
import sys, os,time, shutil
from datetime import datetime
import numpy as np
from dateutil import parser
import re
import prntstk1
#import pudb
import pdb
vb = False

expCsv='./in1/expenses21.csv'
expTxt='./out2/expenses21.txt'       #exact copy of expenses20.csv
expAnt='./out1/expenseAnnotated.txt' #annotated   

def loadstk(expTxt):
   jx = open(expTxt,'r')
   lines = jx.readlines()
   jx.close()
   ln = len(lines)
   stk= []
   for i in range(ln):
      val = str(i)+'a'
      stk.append(val)
   return stk 

def checkExp(expTxt):
   fx = open(expTxt,'r')
   lines = fx.readlines()
   fx.close()  
   ln = len(lines)   
   for i in range(ln):
      lina = lines[i]
      linb= lina.rstrip()    
      itm = linb.split(' ')                
      lx = len(itm)
      if ((lx == 3) and (itm[0][0] != '"')):
         print('   Fix line %d   %s in expenses.' %(i,linb))
         pdb.set_trace()
         sys.exit()            
   return lx   

def cleanit(expCsv,expTxt):
   #pdb.set_trace()
   fx = open(expCsv,'rb')
   gx = open(expTxt,'w+b')
   dat = fx.read() 
   datx = bytearray(dat)
   lx = 0
   lx = len(dat)  
   for i in range(lx):
      if (datx[i] ==0x96):
         datx[i] = 0x20 
      if (datx[i] ==0x92):
         datx[i] = 0x20    
   gx.write(datx)
   fx.close() 
   gx.close()
   checkExp(expTxt)
   return lx

# findit:  stk[] is a list of line numbers of 'Expenses paper trail' appended w/ 'a'
#  1: input an 'amt' from the Accounts2020_sorted 
#     (collation of bank statements, all account except cash)
#  2: if amts are the same, 'got a potential hit'
#  3: change stk[i] <= str(i)+'b'
def findit(amt,dd,stk):
   gotit=0
   #print(' start of findit %s' %(amt))      
   try:      
      fx = open(expTxt,'r') 
      lines = fx.readlines()
      fx.close()      
   except:
      print('  File %s not found ' %(expTxt))      
      return -2, stk    
   la = len(lines)     
   for i in range(la):         
      lina = lines[i]
      lina = lina.rstrip()
      x1 = lina.find(amt)           
      if x1 > -1:   
         #pdb.set_trace()      
         match = re.findall('\d{2}/\d{2}/\d{2}', lina)        
         dr = match[0]         
         #pdb.set_trace()       
      if ((x1>-1) and (dd==dr)):               
         valx = str(i)+'a'
         s1 = stk.index(valx)
         stk[s1]= str(i)+'b'                     
         return 1, stk
   #print(' end of findit search')   
   return 0,stk
    
#acctSort='../out1/Accounts2020_sorted.txt' 
#acctRecon='../out1/Reconciled.txt'  # reconciled
def recon1(acctSort,acctRecon):
   print('   reconcile accounts')  
   #pdb.set_trace()
   hx = open(acctRecon,'w')
   hx.write('   Reconciled.txt  \n')
   hx.write('All expenses on bank accounts should be on paper trail.\n')
   hx.write('Any --> needs to be added to Expenses.csv (paper trail) \n\n')   
   lxx = cleanit(expCsv,expTxt)
   if (lxx < 5):
       print(' Error: %s not found' %(expCsv))
       return -1  
   stk = loadstk(expTxt)  
   gx = open(acctSort,'r')
   lines = gx.readlines()
   lx = len(lines)
   ct =0   
   errx =0
   #pdb.set_trace()
   for i in range(lx):
      lina = lines[i]
      linb = lina.rstrip() 
      #print('%s' %(linb))
      xxx = linb.find('BRICK')      
      amt = linb[21:31]
      amt = amt.rstrip()
      amt = amt.lstrip()
      amt = amt[1:len(amt)]
      date=linb[0:10]  # 0:8  <--                
      try:       
         dd = str(date)         
         dy = dd[0:6] +dd[8:10]        
         famt = float(amt)                        
         x,stk = findit(amt,dy,stk)         
         ct = ct+1
         if x > 0:
            hx.write('.  %s\n' %(linb))
         elif x==0:
            hx.write('-->%s\n' %(linb))
         else:
            errx = 1         
      except:
         continue 
      if errx==1:
         break      
   hx.close()        
   gx.close()
   prntstk1.prntstk(stk,expTxt,expAnt)
   if errx==1: 
      print('  Error processing records %s ' %(expTxt))  
      return -2
   else:      
      print('   Processed %d records' %(ct)) 
   annotat1(expTxt)  #          expenses after they are processed   
   annotat2(expAnt)  # annotate expenses after they are processed      
   return 0  
   
def annotat1(expTxt):  
   ax = open(expTxt,'r') 
   lines = ax.readlines()
   ax.close() 
   bx = open(expTxt,'w')
   bx.write('Check that this file is an exact copy of expenses.csv\n\n')
   la = len(lines)     
   for i in range(la):         
      bx.write(lines[i])
   bx.close
   return   
   
def annotat2(expAnt):  
   ax = open(expAnt,'r') 
   lines = ax.readlines()
   ax.close() 
   bx = open(expAnt,'w')
   bx.write('Expenses Annotated.txt  \n')
   bx.write('       This is list of all expenses from paper trail\n')
   bx.write('       Any line with -- means this expense was also in bank statements. \n')
   bx.write('       Check why any w/o a -- are only from our paper trail.\n')
   bx.write('       These expenses probably came from personal accounts. \n\n')
   la = len(lines)     
   for i in range(la):         
      bx.write(lines[i])
   bx.close
   return 

