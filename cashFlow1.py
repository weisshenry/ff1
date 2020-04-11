# cashFlow1.py 
import sys, os,time, shutil
import pdb

def proCash(fnam):
   print(' start')
   f1= open(fnam,'r')
   g1 = open('CashAcct2020.txt','a')  
   f1lines = f1.readlines()
   #g1.write('--Process %s lines %d \n' %(fnam,len(f1lines)))
   for lina in f1lines:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm)
      #for i in range(lx):
      #   print(' %d %s ' %(i,itm[i]))
      if lx > 3:
         # prcess item 2        
         b1 = itm[2].find('INTERNET/PHONE TRSFR')
         b2 = itm[2].find('AUTO TRANSFER DP-LS') 
         b3 = itm[2].find('POS PURCHASE') 
         b4 = itm[2].find('BILL PAYMENT')   
         b5 = itm[2].find('WITHDRAWAL')         
         if b1 > -1:
            itm[2] = itm[2].replace('INTERNET/PHONE TRSFR','INTERNET')
         elif b2 > -1:
            itm[2] = itm[2].replace('AUTO TRANSFER DP-LS','TRANSFER')
         elif b3 > -1:
            itm[2] = itm[2].replace('POS PURCHASE','PURCHASE')
         elif b4 > -1:
            itm[2] = itm[2].replace('BILL PAYMENT','BILL PAY')
         elif b5 > -1:
            itm[2] = itm[2].replace('WITHDRAWAL','WITHDRWL')
         itm[2] = itm[2].ljust(10)
         #--check itm[3] if blank then a 'deposit'
         try:
            amt = float(itm[3])  
         except:
            continue         
         ck  = itm[2]
         #-- process item[5]       
         x1 = itm[5].find('0501')
         x2 = itm[5].find('9206')
         x3 = itm[5].find('0584')
         x4 = itm[5].find('0509')
         x5 = itm[5].find('2638')
         x6 = itm[5].find('POS PURCHASE TERMINAL')
         x7 = itm[5].find('MERCHANT PURCHASE TERMINAL')
         x8 = ck.find('CHECK')
         if x1 > -1:
               g1.write('%s %s %8.2f To acct: MainHouse\n' %(itm[0],itm[2],amt))
         elif x2 > -1:   
               g1.write('%s %s %8.2f To acct: GuestHouse\n' %(itm[0],itm[2],amt))
         elif x3 > -1:   
               g1.write('%s %s %8.2f To acct: Farm\n' %(itm[0],itm[2],amt))
         elif x4 > -1:   
             g1.write('%s %s %8.2f To acct: Construction\n' %(itm[0],itm[2],amt))
         elif x5 > -1:   
               g1.write('%s %s %8.2f To loan: 2638\n' %(itm[0],itm[2],amt))
         elif x6 > -1: 
               y1= len(itm[5]) 
               test = itm[5][x6+22:x6+30]              
               gotnum= 1
               for i in range(8):
                  if test[i] == ' ':
                     gotnum =0
                     break
               if gotnum:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][x6+31:x6+65]))
               else:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][x6+22:x6+65]))                  
         elif x7 > -1: 
               y1= len(itm[5]) 
               test = itm[5][x6+28:x6+36]               
               gotnum= 1
               for i in range(8):
                  if test[i] == ' ':
                     gotnum =0
                     break
               if gotnum:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][x6+37:x6+70]))
               else:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][x6+28:x6+70]))
         elif x8 > -1:   
               g1.write('%s %s %8.2f CK Numb: %s\n' %(itm[0],itm[2],amt,itm[1]))                  
         else:   
               g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],itm[2],amt,itm[5][0:58]))      
   f1.close() 
   #g1.write('--end process %s \n' %(fnam))
   g1.close()   
   print('  end') 
   return   

def topcash():
   print(' start')
   gx= open('CashAcct2020.txt','w')
   gx.write('              Cash Flow Account Activity 2020  \n\n')
   gx.close()
   fa = '../st3/cashflow03.csv'  
   proCash(fa);
   fb = '../st3/cashflow02.csv'
   proCash(fb);
   fc = '../st3/cashflow01.csv'
   proCash(fc);
   print('  end')   
   return
 

