---- cat r1.py  ----
# Import modules
import os, time,sys
import pdb

if __name__ == '__main__':
  print('  start ');
  time.sleep(15)
  os.system('./t1.sh')
  time.sleep(15)
  tx = open('./out1.txt','r')
  line1 = tx.readlines()
  x = len(line1)
  #print(' lines %d ' %(x))
  #pdb.set_trace()
  for i in range(x):
     linx = line1[i].rstrip()
     #print(linx)
     y = linx.find('IPCAM')
     if y > 0:
        break;
  z = len(linx)
  cmd = './ip3.sh  '+linx[z-3:z-1]
  #cmd = './ip3.sh  20 '
  os.system(cmd)
  #print(cmd)
  #pdb.set_trace()
  print('   end')
  sys.exit()
