import sys
import matplotlib.pyplot as plt
import numpy
import os

def process(path):
    HPCUR=[]
    HPMAX=0
    CPU=[]
    lines=open(path,'r+').readlines()
    for lineindx,line in enumerate(lines):
        if not(line.startswith(' ')):
            continue
        #print line
        l=line.rstrip('\n').split() 
        if len(l)<4:
            continue
        if l[1]=='CassandraDaemon':
            HPCUR.append(float(l[2][:-1]))
            HPMAX=float(l[3][:-1])            
            CPU.append(float(l[6][:-1]))
            print CPU[-1], line
        if len(CPU)==210:
            return HPCUR,HPMAX,CPU
    return HPCUR,HPMAX,CPU 
'''-----------------------------------------------------------------------------------------'''
def plotjvmtop(path,HPCUR,HPMAX,CPU):
    
    plt.figure(figsize=(10,10))
    plt.figure(1)
    xaxis=[]
    xaxisc=[]   
    for i in range(len(HPCUR)):
        xaxis.append(i)
    for i in range(len(CPU)):
        xaxisc.append(i)


    plt.subplot(211)
    l1,=plt.plot(xaxis, HPCUR, 'bo-')
    #l3,=plt.plot(xaxis, HPMAX, 'r+-')
    plt.ylim(0,int(HPMAX))
    plt.xlabel('Sec')
    plt.ylabel('Mb')
    plt.title('JVM Heap Size')
    #plt.setp(xaxis, rotation=90)
    plt.grid()
    #plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    plt.subplot(212)
    l1,=plt.plot(xaxisc, CPU, 'g--')
    #plt.ylim(0,max(CPU))
    plt.xlabel('Sec')
    plt.ylabel('Pecentage %')
    plt.title('JVM CPU STATUS ')
    plt.grid()
    
    print (CPU)
#     plt.subplot(212)
#     l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
#     l5,=plt.plot(jmrecs.keys(), per50, 'g--')
#     l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
#     l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
#     plt.ylim(min(per25),numpy.median(per50)*10)
#     plt.legend([l4, l5, l6, l7], ["25th","50th","75th","90th"],loc=2)
#     plt.xlabel('Sec')
#     plt.ylabel('Latency(msec)')
#     plt.grid()
#     plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
# 
#     plt.subplot(613)
#     l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
#     plt.ylim(min(per25),numpy.median(per50)*10)
#     plt.legend([l4], ["25th"],loc=2)
#     plt.xlabel('Sec')
#     plt.ylabel('Latency(msec)')
#     plt.grid()
#     plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
# 
#     plt.subplot(614)
#     l5,=plt.plot(jmrecs.keys(), per50, 'g--')
#     #plt.ylim(min(per25),numpy.median(per50)*10)
#     plt.ylim(min(per50),(float(ping))+60)
#     plt.legend([l5], ["50th"],loc=2)
#     plt.xlabel('Sec')
#     plt.ylabel('Latency(msec)')
#     plt.grid()
#     plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
# 
#     plt.subplot(615)
#     l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
#     #plt.ylim(min(per25),numpy.median(per50)*10)
#     plt.ylim(min(per75),(float(ping))+100)
#     plt.legend([l6], ["75th"],loc=2)
#     plt.xlabel('Sec')
#     plt.ylabel('Latency(msec)')
#     plt.grid()
#     plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
# 
#     plt.subplot(616)
#     l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
#     #plt.ylim(min(per90),numpy.median(per90)*5)
#     plt.ylim(min(per90),(float(ping))+120)
#     plt.legend([l7], ["90th"],loc=2)
#     plt.xlabel('Sec')
#     plt.ylabel('Latency(msec)')
#     plt.grid()
#     plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #print ('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')

    #if not(os.path.isfile('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')):
     #   figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    plt.show()
    #plt.clf()
'''-----------------------------------------------------------------------------------------'''
if __name__ == "__main__":
    maxacclist=[]
    maxaccall={}
    maxAccArray=[] 
    excel=[]
    tmp=''
    path=r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\round9'
    for root, dirs, files in os.walk(path):
        print "root",root
    
        for file in os.listdir(root):
            current_file_path = os.path.join(root, file)
            if current_file_path.endswith('.txtt'):
                HPCUR,HPMAX,CPU=process(current_file_path)
                plotjvmtop(current_file_path,HPCUR,HPMAX,CPU)  
