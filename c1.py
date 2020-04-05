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
         dsc = dsc.ljust(21)
         try:         
            amt = float(itm[3])  
            act = itm[5]
            x1 = act.find('0501')
            x2 = act.find('9206')
            x3 = act.find('0584')
            x4 = act.find('0509')
            x5 = act.find('2638')
            if x1 > -1:
               g1.write('%s %s %8.2f To acct: 0501\n' %(itm[0],dsc,amt))
            elif x2 > -1:   
               g1.write('%s %s %8.2f To acct: 9206\n' %(itm[0],dsc,amt))
            elif x3 > -1:   
               g1.write('%s %s %8.2f To acct: 0584\n' %(itm[0],dsc,amt))
            elif x4 > -1:   
               g1.write('%s %s %8.2f To acct: 0509\n' %(itm[0],dsc,amt))
            elif x5 > -1:   
               g1.write('%s %s %8.2f To loan: 2638\n' %(itm[0],dsc,amt))
            else:   
               g1.write('%s %s %8.2f To acct: %s\n' %(itm[0],dsc,amt,itm[5][0:58]))
         except:
            print('-%s') 
            #g1.write('-%s %s %s %s \n' %(itm[0],itm[3],itm[4],itm[5]))
      else: 
         #g1.write('---%s \n' %(linb))      
         print(' ')
   f1.close() 
   #g1.write('--end process %s \n' %(fnam))
   g1.close()   
   print('  end')     

if __name__ == "__main__":
   print(' start')
   gx= open('r1.txt','w')
   gx.close()
   fa = '../st2/cashflow3.csv'  
   proces(fa);
   fb = '../st2/cashflow2.csv'
   proces(fb);
   fc = '../st2/cashflow1.csv'
   proces(fc);
   print('  end')   
   sys.exit()  
 

