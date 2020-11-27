# Import modules
import os, time, sys 


if __name__ == '__main__':
  print('  start ')
  time.sleep(15)
  os.system('./t1.sh')
  tx = open('./out1.txt','r')
  line1 = tx.readline()
  x = len(line1)
  print(line1)
  print('its %s ' %(line1[38:x-2]))
  cmd = './ip3.sh  '+line1[38:x-2]
  os.system(cmd)
  print('   end')
  sys.exit()

  
  
