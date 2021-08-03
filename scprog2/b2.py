# b2.py  Process accounts
#  expenses fmt:  date  info  amt   (info needs 2 words <-bug)
import sys, os,time, shutil
import numpy as np
import pdb

db=0 
banktop = './st1/'                #  input: bank csv files
ca21Txt= 'ca21.txt'               # output: ca21.txt ( per 'find' )

def proces0(fx,ca21Txt):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(ca21Txt,'a')    # accounted for, found  
   f1lines = f1.readlines()
   for lina in f1lines:
      linb = lina.rstrip()
      itm = linb.split(',')     
      lx = len(itm) 
      xx = linb.find('<Date>')
      w1 = linb.find('TO ACC')
      w2 = linb.find('TRANSFER TO LOAN')
      w6 = not(( w1 > -1) or (w2 > -1))
      y1 = linb.find('CHECK')  
      if (y1 > -1): 
          #pdb.set_trace()                   
          g1.write('%s, %s %-55s, %12.2f\n' %(itm[0],itm[1],itm[2],float(itm[3])))      
      elif ((xx == -1) and (len(linb) >2)):
         if ((lx > 3) and (xx == -1)) : 
            if itm[4] =='':
               amt = float(itm[3])      
            else: 
               amt = float(itm[4]) 
            if ((amt < 0) and (w6)):     
                g1.write('%s, %-60s, %12.2f\n' %(itm[0],itm[5][0:60],amt))                                 
   f1.close()   
   g1.close()        
   return  

def proces1(fx,ca21Txt,opt):
   print('      %s' %(fx))   
   f1= open(fx,'r')
   g1 = open(ca21Txt,'a') 
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
            g1.write('%s, %-60s, %12.2f\n' %(itm[0],itm[5][0:60],amt))              
         elif (opt ==2):  # for all cash transactions           
            g1.write('%s, %-60s, %12.2f \n' %(itm[0],linb[10:100],amt))                  
   f1.close()   
   g1.close()     
   return 

# finds the st1/ bank statements per nam, nam1
def proc(nam,nam1,opt): 
   gv= open(ca21Txt,'a')
   gv.write('\n   ,          '+nam1+' Account Activity 2021  ,\n\n')
   gv.close()
   for i in range(12,9,-1):
      xnam =banktop+nam+str(i)+'.csv'    
      if os.path.isfile(xnam): 
         if opt==0:      
            proces0(xnam,ca21Txt) 
         else:
            proces1(xnam,ca21Txt,opt)         
   for i in range(9,0,-1): 
      xnam =banktop+nam+'0'+str(i)+'.csv'     
      if os.path.isfile(xnam):            
         if opt==0:      
            proces0(xnam,ca21Txt) 
         else:
            proces1(xnam,ca21Txt,opt) 
   return   

if __name__ == "__main__":
   print(' start')     
   gv= open(ca21Txt,'w');   gv.close()       
   proc('cashflow','Cashflow',0)  
   proc('guesth','Guesthouse 9206',1)
   proc('main','Mainhouse 0501',1)   
   proc('con','Construction 0509',1) 
   proc('farm','Farm 0584',1)     
   print('   end part1, start recon')   
   sys.exit()  
 

