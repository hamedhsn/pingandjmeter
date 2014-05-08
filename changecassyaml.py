'''
Created on 30-Jan-2014

This piece of code will retrive the ip address of the node and configure the yaml based on that ip

@author: hsn
'''
import os

def cassplnodes():
    os.system('hostname -i >tmp.txt')
    ip=(open('tmp.txt','r').readline()).rstrip()
    lines=open('apache-cassandra-2.0.4/conf/cassandra.yaml','r+').readlines()
    for lineno,line in enumerate(lines):
        if line.startswith('listen_address:'):
            lisadd=line.split(':')[1][1:]
            print lisadd
            lines[lineno]=line.replace(lisadd, ip)+'\n'
        if line.startswith('rpc_address:'):
            lisadd=line.split(':')[1][1:]
            print lisadd
            lines[lineno]=line.replace(lisadd, ip)+'\n'
        if line.startswith('          - seeds:'):
            lisadd=line.split(':')[1][1:]
            print lisadd
            lines[lineno]=line.replace(lisadd, '"'+ip+'"')+'\n'



    open("apache-cassandra-2.0.4/conf/cassandra.yaml", "w").writelines(lines)
    
if __name__ == "__main__":
    cassplnodes()