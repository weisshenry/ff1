# recon1.py  Reconcile all accounts
import sys, os,time, shutil
from datetime import datetime
import numpy as np
from dateutil import parser
import re
#import pudb
import pdb
vb = False

expCsv='./out1/expenses20.csv'
expTxt='./out1/expenses20.txt'       #exact copy of expenses20.csv
expAnt='./out1/expenseAnnotated.txt' #annotated

def prntstk(stk,expTxt,expAnt):
   mx = open(expTxt,'r')
   px = open(expAnt,'w')
   linb = mx.readlines()  
   mx.close()
   for i in range(len(linb )):
      k = stk[i]
      x = k.find('a')
      linc = linb[i]
      lind = linc.rstrip()      
      mat=re.match('\d{2}[/]\d{2}[/]\d{2}', lind) 
      if mat is not None:                      
            sss = re.findall('\".*?\"',lind)           
            if sss is not None:                           
               nnn =re.findall('\d*\.?\d+',lind)
               if nnn is not None:
                   try:
                      stg = sss[0]  
                   except:
                      print('gotit')
                      pdb.set_trace()                      
                   sth = stg.replace('"',' ')  
                   y = len(nnn)                   
                   linf =('%-10s %-50s %10s' %(mat[0],sth,nnn[y-1]))
                   # x1 = sth.find('Schroeder')
                   # if x1 > -1:
                      # print('gotit')
                      # pdb.set_trace()
                   #linf = mat[0]+'  '+stg+'  '+nnn[3]
                   if vb:
                      print('-->%s' %(linf))
      else:
         linf = lind      
      if x > -1:
         px.write('   '+linf+'\n')
      else: 
         px.write('...'+linf+'\n')   
      #pdb.set_trace()
   px.close()          
   return
   

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

def cleanit(expCsv,expTxt):
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
   return lx

def findit(amt,dd,stk):
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
         match = re.findall('\d{2}/\d{2}/\d{2}', lina)        
         dx = datetime.strptime(match[0],"%m/%d/%y")                         
      if ((x1>-1) and (len(match)==1)):
         #print('  got it ') 
         valx = str(i)+'a'
         s1 = stk.index(valx)
         stk[s1]= str(i)+'b'         
         return 1, stk
   #print(' end of findit search')   
   return 0,stk
    
#acctSort='./out1/Accounts2020_sorted.txt' 
#acctRecon='./out1/Reconciled.txt'  # reconciled
def recon1(acctSort,acctRecon):
   print('   Start - reconciled accounts')  
   hx = open(acctRecon,'w')
   hx.write('   Reconciled.txt  \n')
   hx.write('All expenses on bank accounts should be on paper trail.\n')
   hx.write('Step3: Any --> needs to be added to Expenses.csv (paper trail) \n\n')   
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
   for i in range(lx):
      lina = lines[i]
      linb = lina.rstrip() 
      amt = linb[21:31]
      amt = amt.rstrip()
      amt = amt.lstrip()
      amt = amt[1:len(amt)]
      date=linb[0:8]      
      try:
         dd = datetime.strptime(date,"%m/%d/%y")       
         famt = float(amt)       
         #print('  going to finditx')         
         x,stk = findit(amt,dd,stk)
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
   prntstk(stk,expTxt,expAnt)
   if errx==1: 
      print('  Error processing records %s ' %(expTxt))  
      return -2
   else:      
      print('   Processed %d records' %(ct)) 
   annotat1(expTxt)  # annotate expenses after they are processed   
   annotat2(expAnt)  # annotate expenses after they are processed      
   return 0  
   
def annotat1(expTxt):  
   ax = open(expTxt,'r') 
   lines = ax.readlines()
   ax.close() 
   bx = open(expTxt,'w')
   bx.write('Step1: Check that this file is an exact copy of expenses.csv\n\n')
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
   bx.write('Step2: This is list of all expenses from paper trail\n')
   bx.write('       Any line with ... means this expense was also in bank statements. \n')
   bx.write('       Check why any w/o a dot are only from our paper trail.\n')
   bx.write('       These expenses probably came from personal accounts. \n\n')
   la = len(lines)     
   for i in range(la):         
      bx.write(lines[i])
   bx.close
   return 

