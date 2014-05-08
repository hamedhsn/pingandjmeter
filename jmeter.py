'''
Created on 17-Jan-2014

@author: hsn
'''
'''Script for running the non-gui version of jmeter on a specified host'''
import os
import platform
import argparse

host=''

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-s','--host', help='Host address', required=True)
parser.add_argument('-c','--pingcnt', help='number of ping operation', required=False,default=3)
parser.add_argument('-t','--testplan',help='name of the test plane',required=False,default='10th10opse10sec.jmx')
parser.add_argument('-n',action="store_true",default=False)
args = vars(parser.parse_args())

print args
if not(args['host']):
    print "Please Enter the host: "

'''run a ping'''
if platform.system()=='Windows':
    os.system('ping -n '+str(args['pingcnt'])+' '+str(args['host'])+' >tmp.txt')
elif platform.system()=='Linux':
    os.system('ping -c '+str(args['pingcnt'])+' '+str(args['host'])+' >tmp.txt')

'''retrieve the average ping and write in tmp file'''
lines=open('tmp.txt','r').readlines()
if platform.system()=='Windows':
    #print lines[-1].split(" ")[-1][:-3];
    avgping= lines[-1].split(" ")[-1][:-3];
    open("tmp.txt", "w").writelines(avgping) #write the average ping output in tmp file 
elif platform.system()=='Linux':
    #print lines[-1].split("/")[4];
    avgping= lines[-1].split("/")[4];
    open("tmp1.txt", "w").writelines(avgping) #write the average ping output in tmp file
    
''' open jmx file and add new host ip'''    
#if not(args['testplan']):
#    lines=open('10th10opse10sec.jmx','r+').readlines()
#else:
lines=open(str(args['testplan']),'r+').readlines()
i=0
for line in lines:
    if line.startswith('          <stringProp name="cassandraServers">'):
        ip=line.split('>')[1].split('<')[0][:-5]
        lines[i]=line.replace(ip, str(args['host']))
        break
    i+=1
    #156.62.231.244:9160
print lines[31]
print "average latency is:"
os.system('cat tmp1.txt')
open("10th10opse10sec.jmx", "w").writelines(lines)

if not(args['n']):
    os.system('./bin/jmeter -t 10th10opse10sec.jmx')
else:
    os.system('./bin/jmeter -n -t 10th10opse10sec.jmx')

