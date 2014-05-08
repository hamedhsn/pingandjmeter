'''
Created on 31-Jan-2014

This code goes through the file that each line contains some server belong to a cluster and crete a new file for each cluster 
@author: hsn
'''
def modify():
    lines=open('cluster1.txt','r+').readlines()
    
    for line in (lines):
        w=line.split(' ')
        for ipno,ip in enumerate(w):
            print ipno,ip
            if (ipno==0):
                a=open(ip+'.txt','w')
            else:
                a.write('%'+ip+'\n')
        
def createcluster():           
    lines=open('cluster.txt','r+').readlines()
    clno=8
    for linno,line in enumerate(lines):
        if linno%40==0:
            a=open('wr'+str(clno)+'.txt','w')
            clno+=1
        a.write('%'+line)
        
if __name__ == '__main__':
    #modify()
    createcluster()
    