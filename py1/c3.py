#   a1.py  -->  input:  all accts in st1
#              output:  out1/CashAll_(YY).txt  all bank transactions
#   b1.py  -->  input:  all accts in st1
#              output:  accounted for ca(YY).txt
#              output:  unaccounted for out2/CashExct.txt 
#   c1.py  -->  input:  ca(YY).txt  Sorted import from all bank statements
#                       ex(YY).txt  Paper trail - manually compiled
#              Output:  check(YY).txt  Issues on ca(YY).txt which should be 
#                       entered on paper trail. 
# glin = list of all date-desc-amts to find in the master list of keywords 
# from ca21.txt glin needs 'cleaned' of comments, so only has date-desc-amts
import sys, os,time, shutil, glob
import numpy as np
import pdb
 
ca21Ttxt= './out1/ca22.txt'        # INPUT
ex21Txt= './st2/ex22.txt'         # INPUT
check21= './out1/check22.txt'      # Output
kywd=[ \
   # 1099 Work
     'BRITTANY KUHLMAN','KODY KUHLMAN','DEB SCHROEDER',\
     'MARTY KUHLMAN','DAVE SCHROEDER','LOGAN SCHROEDER',\
   #utilities:   
     'GLANDORF TELEPHO','PAULDING',\
     'Prime Video','S & S',"CHERRY'S",'OHIO SANITARY',\
     'EXXONMOBIL','CASEYS',\
   #contractors    
     'ALLEN SCHROEDER',"ELLERBROCK'S PLUMB",'MATIJEVICH FLOOR',\
     'BRICKNER CONS','GREG BROWN','POWER HOUSE','BIOHABITATS',\
   #commerical supplies, etc
     'WAL-MART', 'VAN WERT CARTS','TRACTOR SUPPLY','GLANDORF LUMBER',\
     'GLANDORF WAREHOUSE','WATER SOLUTIONS','K & L READY',\
     'MANUFACTURERS PLUM','TJMAXX','TAWA TREE','TRUE VALUE',\
     'SIGNATURE DESI','FORTMANS CRESCEN','CONTINENTAL WOOD',\
     'OVERSTOCK.COM','PUTNAM LAWN','MNRD-LIMA','Amazon Prime',\
     'BUCKEYE EXTERMINAT', \
   #govt, CPA, INSUR etc
     'PUTNAM COUNTY TREA','SCHROEDER AND CO','OMIG','OHIO MUTUAL INS',\
   #misc - checks,     
     'TLR18004','TLR18005','TLR18009','TLR18010',\
     '1005 CHECK','1007 CHECK','1008 CHECK','RETURN ITEM',\
     '1014 CHECK','TLR18006','TLR18004','V104014', 'MED*HCT','2G1AA',\
     '1009 CHECK','1013 CHECK','1011 CHECK','1012 CHECK']

def findit(glin,amt,dat,txt):
   k = len(glin)   
   gotit=0
   ww = 99
   for i in range(len(kywd)):
      xx = txt.find(kywd[i])      
      if xx > -1:
         gotit =1         
         ww = i
         #print(' found keyword %s ' %(kywd[i]))
         break
   if gotit==0:
       #print(' did not find keyword')      
       return 0;   
   ctr = 0    
   mtr =0
   for lina in glin: #lines in ex(YY).txt
      ctr = ctr +1
      linb = lina.rstrip()
      itm = linb.split(',')
      try:      
         amt2 = float(itm[2])      
      except:
         amt2= 0.0      
      dat2 = itm[0]     
      try:
         txt2 = itm[1]
      except:
         print('ERR: %s ' %(linb))
         pdb.set_trace()      
      yy = txt2.find(kywd[ww])
      if ((yy > -1) and (dat2==dat)): 
         if ((yy > -1) and (dat2==dat) and (amt2==-amt)):  
            mtr = ctr; 
            return 1            
         #else:            
         #   print('     %s %s amt %8.2f %8.2f %s %d' %(txt,dat,-amt,amt2,kywd[ww],ctr))              
   print(' no  %s %s amt %8.2f %8.2f %s %d' %(txt,dat,-amt,amt2,kywd[ww],mtr)) 
   #pdb.set_trace()
   #print(' %s \n\n' %(linb))    
   return 0 

def cleaned(glin):
   gline = []
   for i in range(len(glin)): 
      glinx = glin[i].rstrip()   
      itm = glinx.split(',')     
      lx = len(itm)  
      x = itm[0].find('/')
      if ((x > -1) and (lx > 2)):
         gline.append(glinx)  
   #print('   before: %d  after: %d ' %(len(glin),len(gline)))    
   return gline      

def proces1(ca21Ttxt,ex21Txt,check21):
   print('   Input: %s, %s  Output:  %s' %(ca21Ttxt,ex21Txt,check21))  
   f1= open(ca21Ttxt,'r')
   ct =0
   #for filex in glob.glob("st2/*.txt"):
   #    ct = ct +1
   #    print('   Using input: %s' %(filex))
   #if ct==1:
   #   g1=open(filex,'r') 
   #else:
   #   print('   Error: Too many/few files in dir st2')
   #   sys.exit()      
   #pdb.set_trace()
   g1 = open(ex21Txt,'r') 
   h1 = open(check21,'w') 
   h1.write('       --- File %s ---  check of ca(YY).txt  ' %(check21))
   flin = f1.readlines()
   glin = g1.readlines()  
   glin = cleaned(glin)
   for lina in flin:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm)           
      if (lx > 2): 
         try:
           amt = float(itm[2])      
         except:
           amt =0.0
         dat = itm[0]                  
         txt = itm[1]                 
         jj =0
         if (len(dat) > 7):
            jj = findit(glin,amt,dat,txt)                      
         if jj:         
            h1.write('  %s %-60s %10.2f \n' %(dat,txt,float(amt)))  
         elif (len(dat) > 7):
            h1.write('--%s %-60s %10.2f \n' %(dat,txt,float(amt)))             
         else: 
            h1.write('  %s\n' %(linb))          
   f1.close()   
   g1.close() 
   h1.close()   
   return 

if __name__ == "__main__":
   print('   start') 
   print('   Note: If NO MATCH appears, add the expense to ex21.txt ')   
   proces1(ca21Ttxt,ex21Txt,check21)    
   print('   end ')   
   sys.exit()  
 

