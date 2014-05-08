# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 12:00:38 2014

@author: hsn
"""
import sys
import simplejsonrpc as jsonrpc
'''
#server = jsonrpc.Server("http://planetlab2.exp-math.uni-essen.de:5000/rpc")
#server = jsonrpc.Server("http://planetlab2.exp-math.uni-essen.de:5000")
server = jsonrpc.Server("http://planet1.unipr.it:5001")
print server.add(2333, 32)
#print server.test()
print server.jmeter('132.252.152.194')
#print server.foo()
'''
import threading, time


'''sample'''
#availableJmeters=['planet1.unipr.it','planetlab1.csg.uzh.ch']
#cassnodes={'132.252.152.194':0,'137.132.80.106':0}  #contains cassandra nodes and experiment number start from 0
#jmnodes = { 'planet1.unipr.it': 5001,'planetlab1.csg.uzh.ch': 5000 };
jmnodes={}

jmlocation='us'
casslocation='eu5'

lines=open(r'C:\cygwin64\etc\clusters','r+').readlines()
for lineindx,line in enumerate(lines):
    line=line.rstrip('\n') 
    if line.startswith('jmetereu'):
        if jmlocation=='eu':
            availableJmeters=line.split(' ')[1:]
            for indx,i in enumerate(availableJmeters):
                jmnodes[i]=5000+indx
    if line.startswith('jmeterus'):
        if jmlocation=='us':
            availableJmeters=line.split(' ')[1:]
            for indx,i in enumerate(availableJmeters):
                jmnodes[i]=5200+indx

'''eu'''
#availableJmeters=['planet1.unipr.it','planetlab1.csg.uzh.ch','plab-2.diegm.uniud.it','planetlab1.extern.kuleuven.be','planetlab2.mini.pw.edu.pl','planetlab-coffee.ait.ie','planetlab2.cs.vu.nl','roti.mimuw.edu.pl','planetlab2.lkn.ei.tum.de']
#cassnodes={'132.252.152.194':0,'137.132.80.106':0,'planetlab2.urv.cat':0,'planetlab-tea.ait.ie':0,'ple2.dmcs.p.lodz.pl':0,'ple2.cesnet.cz':0,'planet-lab-node1.netgroup.uniroma2.it':0,'ple6.ipv6.lip6.fr':0,'planet-lab-node2.netgroup.uniroma2.it':0,'onelab2.info.ucl.ac.be':0,'aguila2.lsi.upc.edu':0,'host4-plb.loria.fr':0,'planetlab2.cs.vu.nl':0,'planetlab1.informatik.uni-goettingen.de':0,'pl002.ece.upatras.gr':0,'planetlab2.ci.pwr.wroc.pl':0,'planetlab2.u-strasbg.fr':0,'dschinni.planetlab.extranet.uni-passau.de':0,'planetlab1.mta.ac.il':0,'planetlab-2.man.poznan.pl':0,'ple2.tu.koszalin.pl':0,'planetlab3.xeno.cl.cam.ac.uk':0,'planet2.inf.tu-dresden.de':0,'planetlab1.ionio.gr':0,'planetlab-13.e5.ijs.si':0,'planetlab1.virtues.fi':0,'onelab3.info.ucl.ac.be':0,'planetlab2.montefiore.ulg.ac.be':0,'planetlab1.informatik.uni-wuerzburg.de':0,'planck227ple.test.ibbt.be':0,'planetlab2.utt.fr':0,'planetlabpc1.upf.edu':0,'planetlab1.montefiore.ulg.ac.be':0}  #contains cassandra nodes and experiment number start from 0
jmnodes = { 'planetlab1.csg.uzh.ch': 5000,'planet1.unipr.it': 5001,'plab-2.diegm.uniud.it':5002,'planetlab1.extern.kuleuven.be':5003,'planetlab2.mini.pw.edu.pl':5004,'planetlab-coffee.ait.ie':5005,'planetlab2.cs.vu.nl':5006,'roti.mimuw.edu.pl':5007,'planetlab2.lkn.ei.tum.de':5008 };
'''north America'''
availableJmeters=[]
cassNodesBenchmarking=[]


lostConnNodes=[]
jmservers={}
isFinish=False

for i in (jmnodes.keys()):
    jmservers[i] = jsonrpc.Server("http://"+i+":"+str(jmnodes[i]))

    
class rec_data(threading.Thread):
     def __init__(self,server,jmeterHost,cassHost):
         threading.Thread.__init__(self)
         self.server=server
         self.cassHost=cassHost
         self.jmeterHost=jmeterHost

     def run(self):
         #print "start",self.server
         try:
             print "Jmeter Host:",jmeterHost
             print self.server.jmeter(self.cassHost,cassnodes[self.cassHost])    #run the jmeter on remote jmeter server on cassansdra node(cassHost)
             availableJmeters.append(self.jmeterHost)   #add the jmeter node to the list of nodes
             cassNodesBenchmarking.remove(self.cassHost)
             cassnodes[self.cassHost]+=1
         except:
             #print "Unexpected error:", sys.exc_info()[0]
             print "***NODES IS NOT AVAILABLE***:",self.jmeterHost
             #lostConnNodes.append(self.jmeterHost)
             cassNodesBenchmarking.remove(self.cassHost)
             pass

         #os.sytem("scp -i ~/.ssh/id_rsa resutltest.txt hs302@frank.eecs.qmul.ac.uk:JMETER/RES/round4/")
         #os.sytem("scp -i ~/.ssh/id_rsa qmulple_hsn_test_cloud@"+self.jmeterHost+":resulttest.txt ~/JMETER/RES/round4/"+self.cassHost+"-"+repeatNo+".txt")    #copy from node to frank

#         print "run test",self.s
#         res = self.s.recv(100)
#         while res:
#             print "rcv(%s)" % (repr(res),)
#             res = self.s.recv(100)

'''THIS THREAD CHECKS THE AVAILABILITY OF THE JMETER NODES'''
class jmnode_health_check(threading.Thread):
     def __init__(self):
         threading.Thread.__init__(self)
         self.allservers=jmservers

     def run(self):
         while not(isFinish):
             self.allservers=jmservers
             for i in self.allservers.keys(): 
                 try:
                     print self.allservers[i].add(10,15),i
                     if i not in availableJmeters:
                         availableJmeters.append(i)
                         print "This node is now UP: ",i  
                     if i in lostConnNodes:                         
                         lostConnNodes.remove(i)
                         print "This node is now UP: ",i  
                         
                 except:
                     #print "Unexpected error:", sys.exc_info()[0]
                     if i in availableJmeters:
                         availableJmeters.remove(i)
                         print "This node is now DOWN: ",i                     
                     if i not in lostConnNodes:
                         lostConnNodes.append(i)
                         print "This node is now DOWN: ",i                     
                         print "Health-check----List of Unavailable Nodes:",lostConnNodes
                     pass
             #every 10sec check whether the nodes are alive
             time.sleep(2);

#hCheckthr=jmnode_health_check()
#hCheckthr.start()
'''End of check'''

maxExpRepeat=1
def chooseAvailableCassHost():
    for i in (cassnodes.keys()):
        if (cassnodes[i] <maxExpRepeat) and (i not in cassNodesBenchmarking):
            return i
    return 'none'
def isMoreCassHost():
    for i in cassnodes.keys():
        if  cassnodes[i]<maxExpRepeat:
            return True
    return False    

while(True):
    if len(availableJmeters)==0:
        continue
    if isMoreCassHost()==False:       #check if experiments repeated certain times-closeing condition
        isFinish=True
        print "End of the Experiment"
        break
    cassHost=chooseAvailableCassHost()
    #print "availabel",cassHost
#    if cassHost not in cassNodesBenchmarking:
    if cassHost!='none':
        #print cassnodes,"CAss HOst: ",cassHost
        cassNodesBenchmarking.append(cassHost)
        jmeterHost=availableJmeters.pop()
        print "jmeter hosts",availableJmeters
        thr=rec_data(jmservers[jmeterHost],jmeterHost,cassHost)
        thr.start()
#for i in (jmnodes.keys()):
#        t=rec_data(jmservers[i])
#        t.start()
        #t.join()

#print jmservers['planet1.unipr.it'].add(10,5)
#for i in (jmnodes.keys()):
#        print 'sending to',jmservers[i]
#        jmservers[i].add(10,5)
