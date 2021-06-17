# recon1.py  Reconcile all accounts
import sys, os,time, shutil
from datetime import datetime
import numpy as np
from dateutil import parser
import re
#import pudb
import pdb
vb = False

expCsv='./in1/expenses21.csv'
expTxt='./out2/expenses21.txt'       #exact copy of expenses20.csv
expAnt='./out1/expenseAnnotated.txt' #annotated

def prntstk(stk,expTxt,expAnt):
   sm =0
   mx = open(expTxt,'r')
   px = open(expAnt,'w')
   linb = mx.readlines()  
   mx.close()
   for i in range(len(linb)):
      k = stk[i]
      x = k.find('a')
      linc = linb[i]
      lind = linc.rstrip()      
      mat=re.match('\d{2}[/]\d{2}[/]\d{2}', lind) 
      if mat is not None:        #found valid date             
               linf, ling =  splitstr(lind)    # split on 1st quotes
               sth = linf.replace('"',' ')     # 1st quoted str
               ttt = re.findall('\".*?\"',ling)# 2nd quoted str                
               nnn =re.findall('-?\d*\.?\d+',ling) #find numbers
               y = len(ttt)                            
               if nnn is not None:                   
                  if y == 0:  
                     linh =('%-10s %-38s %10s' %(mat[0],sth,nnn[0]))
                  else:       # found 2nd quoted str
                     vvv = ttt[0].replace('"','')
                     linh =('%-10s %-38s %10s  %-10s' %(mat[0],sth,nnn[0],vvv)) 
                     #pdb.set_trace()            
      else:
         linh = lind  
      #print('%s' %(linh))  
      #pdb.set_trace()      
      if x > -1:
         px.write('  '+linh+'\n')
      else: 
         px.write('--'+linh+'\n')   
      #pdb.set_trace()
   px.close()          
   return
   
def splitstr(strg):
   x1 = strg.find('"')
   x2 =strg.find('"', strg.find('"') + 1)
   lina = strg[x1:x2+1]
   x3 = len(strg)
   linb = strg[x2+1:x3]
   return lina,linb
    
