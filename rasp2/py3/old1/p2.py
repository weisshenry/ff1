import sys
import numpy as np
import scipy.integrate as it
import matplotlib.pyplot as plt
import pdb

def rmv(vec1, vec2):
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3),\
           (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rot_mat = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rot_mat
    
def findavg(a,b,c):
   ax = np.mean(a)
   bx = np.mean(b)
   cx = np.mean(c)  
   return ax,bx,cx

def loadit(filex):
   with open(filex) as fx:   
      linex = fx.readlines()  
   lx = len(linex)
   n = np.zeros([lx],dtype='float')
   a = np.zeros([lx],dtype='float')
   b = np.zeros([lx],dtype='float')
   c = np.zeros([lx],dtype='float')
   for i in range(lx):
      lina = linex[i]
      x = lina.split(',')
      n[i] = x[0]
      a[i] = x[1]
      b[i] = x[2]
      c[i] = x[3]   
   return a,b,c

if __name__ == "__main__":
   a,b,c = loadit('ca1.txt')
   ax,bx, cx = findavg(a,b,c)
   print('avg=  %f %f %f '%(ax,bx,cx)) 
   lx = len(a)
   dd= np.zeros([lx,3],dtype='float')
   aa= np.zeros([1,3], dtype='float')
   bb= np.zeros([1,3], dtype='float') 
   
   aa[0,:]= [ 0, 0, -1] 
   bb[0,:]= [ ax,bx,cx] 
   ba = (1/np.linalg.norm(bb))
   bc = bb *ba
   mm = rmv(aa,bc)
   cc = np.matmul(mm,np.transpose(aa)) 
   print(' %f %f %f ' %(cc[0],cc[1],cc[2]))
   for i in range(lx):
      dd[i,:] = np.matmul(mm,np.transpose(dd[i,:]))
   am,bm,cm = findavg(dd[:,0],dd[:,1],dd[:,2])   
   print('avg= %f %f %f ' %(am,bm,cm))
   
   sys.exit()   
      
     
     