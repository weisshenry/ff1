# ff process1
import sys, os,time, shutil
import numpy as np
import pdb

def proces(fnam):
   print(' start')
   f1= open(fnam,'r')
   g1 = open('r1.txt','a')  
   f1lines = f1.readlines()
   #g1.write('--Process %s lines %d \n' %(fnam,len(f1lines)))
   for lina in f1lines:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm)
      #for i in range(lx):
      #   print(' %d %s ' %(i,itm[i]))
      if lx > 3:
         dsc = itm[2]
         b1 = dsc.find('INTERNET/PHONE TRSFR')
         b2 = dsc.find('AUTO TRANSFER DP-LS') 
         b3 = dsc.find('POS PURCHASE') 
         b4 = dsc.find('BILL PAYMENT')   
         b5 = dsc.find('WITHDRAWAL')         
         if b1 > -1:
            dsc = dsc.replace('INTERNET/PHONE TRSFR','INTERNET')
         elif b2 > -1:
            dsc = dsc.replace('AUTO TRANSFER DP-LS','TRANSFER')
         elif b3 > -1:
            dsc = dsc.replace('POS PURCHASE','PURCHASE')
         elif b4 > -1:
            dsc = dsc.replace('BILL PAYMENT','BILL PAY')
         elif b5 > -1:
            dsc = dsc.replace('WITHDRAWAL','WITHDRWL')
         dsc = dsc.ljust(10)
         try:         
            amt = float(itm[3])  
            ck  = itm[2]
            act = itm[5]
            x1 = act.find('0501')
            x2 = act.find('9206')
            x3 = act.find('0584')
            x4 = act.find('0509')
            x5 = act.find('2638')
            x6 = act.find('POS PURCHASE TERMINAL')
            x7 = act.find('MERCHANT PURCHASE TERMINAL')
            x8 = ck.find('CHECK')
            if x1 > -1:
               g1.write('%s %s %8.2f To acct: MainHouse\n' %(itm[0],dsc,amt))
            elif x2 > -1:   
               g1.write('%s %s %8.2f To acct: GuestHouse\n' %(itm[0],dsc,amt))
            elif x3 > -1:   
               g1.write('%s %s %8.2f To acct: Farm\n' %(itm[0],dsc,amt))
            elif x4 > -1:   
               g1.write('%s %s %8.2f To acct: Construction\n' %(itm[0],dsc,amt))
            elif x5 > -1:   
               g1.write('%s %s %8.2f To loan: 2638\n' %(itm[0],dsc,amt))
            elif x6 > -1: 
               y1= len(itm[5]) 
               test = itm[5][x6+22:x6+30]              
               gotnum= 1
               for i in range(8):
                  if test[i] == ' ':
                     gotnum =0
                     break
               if gotnum:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][x6+31:x6+65]))
               else:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][x6+22:x6+65]))                  
            elif x7 > -1: 
               y1= len(itm[5]) 
               test = itm[5][x6+28:x6+36]               
               gotnum= 1
               for i in range(8):
                  if test[i] == ' ':
                     gotnum =0
                     break
               if gotnum:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][x6+37:x6+70]))
               else:                     
                  g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][x6+28:x6+70]))
            elif x8 > -1:   
               g1.write('%s %s %8.2f CK Numb: %s\n' %(itm[0],dsc,amt,itm[1]))                  
            else:   
               g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][0:58]))
         except:
            k=1 
            #print('-%s %s %s %s \n' %(itm[0],itm[3],itm[4],itm[5]))
            #g1.write('-%s %s %s %s \n' %(itm[0],itm[3],itm[4],itm[5]))
      else: 
         #g1.write('---%s \n' %(linb)) 
         #print('---%s \n' %(linb))          
         k=1
   f1.close() 
   #g1.write('--end process %s \n' %(fnam))
   g1.close()   
   print('  end')     

if __name__ == "__main__":
   print(' start')
   gx= open('r1.txt','w')
   gx.write('              Cash Flow Account Activity 2020  \n\n')
   gx.close()
   fa = '../st3/cashflow03.csv'  
   proces(fa);
   fb = '../st3/cashflow02.csv'
   proces(fb);
   fc = '../st3/cashflow01.csv'
   proces(fc);
   print('  end')   
   sys.exit()  
 

