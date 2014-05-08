'''
Created on 27-Jan-2014

this piece of code will postprocess the output of the jmeter and plot the experiment based on Load and Latency 

@author: hsn
'''

'''
linux=/homes/hs302/Dropbox/Reading Stuff/0-MyPhD/2exp-tcpdump/5qmul/jmeter/sg/jmeterrow4/test/testsg100-ed.txt
windows=F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\5qmul\\sg\\2sg5th20e10qm-ed.txt
'''

import matplotlib.pyplot as plt
import numpy
import os

def process(path):
    expcnt=[]
    hitcnt=[]
    opscnt=[]
    per25=[]
    per50=[]
    per75=[]
    per90=[]
    per99=[]
    jmrecs={}
    error=""
    maxAcc=''
    host=path.split("\\")[-1]
    #if not(os.path.exists(path)):
    #    return
    lines=open(path,'r+').readlines()
    ping=lines[0].split(':')[0][:-4]
    for lineindx,line in enumerate(lines):
        line=line.rstrip('\n')  
        if line.startswith('#30    Threads'):
            if(line[-1]!=0):
                error=' --- ERROR ---'
        if line.startswith('Time:'):
            time=int(line.split(':')[1])
            jmrecs[time]=[0,0,0,0,0,0,0,0]
           
        if line.startswith('Expected op/per/sec'):
            jmrecs[time][0]=float(line.split(':')[1][1:])
        if line.startswith('Actual   Hit/per/sec'):    
            jmrecs[time][1]=float(line.split(':')[1][1:])
        if line.startswith('Actual   Op/per/sec'):
            jmrecs[time][2]=float(line.split(':')[1][1:])
        if line.startswith('25th Percentile'):
            jmrecs[time][3]=float(line.split(':')[1][1:])
        if line.startswith('50th Percentile'):
            jmrecs[time][4]=float(line.split(':')[1][1:])
        if line.startswith('75th Percentile'):
            jmrecs[time][5]=float(line.split(':')[1][1:])
        if line.startswith('90th Percentile'):
            jmrecs[time][6]=float(line.split(':')[1][1:])
        if line.startswith('99th Percentile'):
            jmrecs[time][7]=float(line.split(':')[1][1:])
        if line.startswith('************************MAX Accepted'):
            maxAcc=(line.split(':')[1][1:])
    for sample in jmrecs.values():
        expcnt.append(sample[0])
        hitcnt.append(sample[1])
        opscnt.append(sample[2])
        m=1
        per25.append(sample[3]*m)
        per50.append(sample[4]*m)
        per75.append(sample[5]*m)
        per90.append(sample[6]*m)
        per99.append(sample[7]*m)    

    if len(expcnt)<2:
        return
    
#     std50latency=str(numpy.median([i for i in per50 if i >= float(ping)+15])-float(ping))
    #print [i for i in per50 if i >= float(ping)+15]
    std50latency=str(numpy.percentile([i for i in per50 if i >= float(ping)+10]+[0],75))
    std75latency=str(numpy.percentile([i for i in per75 if i >= float(ping)+10]+[0],75))
    std90latency=str(numpy.percentile([i for i in per90 if i >= float(ping)+10]+[0],75))
    std99latency=str(numpy.percentile([i for i in per99 if i >= float(ping)+10]+[0],75))
    #print [i for i in per50 if i >= float(ping)+20]
    
    return jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,std99latency,host
'''-----------------------------------------------------------------------------------------'''
def plotSeprate(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path):
    
    plt.figure(figsize=(10,10))
    plt.figure(1)

    plt.subplot(611)
    l1,=plt.plot(jmrecs.keys(), expcnt, 'bo-')
    # #l2,=plt.plot(jmrecs.keys(), hitcnt, 'y*-')
    l3,=plt.plot(jmrecs.keys(), opscnt, 'r+-')
    plt.ylim(0,max(expcnt))
    plt.legend([l1, l3], ["Expected ops","Actul ops"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('operation per second')
    plt.title('LOAD vs LATENCY(client: jazz,server: '+host+')  --  Average ping: '+ping+error+' -- Accepted RPS='+maxAcc+' -- Latency Diff50th,75th,95th='+std50latency+', '+std75latency+', '+std90latency)
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    plt.subplot(612)
    l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l4, l5, l6, l7], ["25th","50th","75th","90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(613)
    l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l4], ["25th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(614)
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l5], ["50th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(615)
    l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l6], ["75th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(616)
    l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l7], ["90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    print ('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    
    plt.show()
'''-----------------------------------------------------------------------------------------'''
def plot50th(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path):
    plt.figure(figsize=(10,10))
    plt.figure(1)

    plt.subplot(411)
    l1,=plt.plot(jmrecs.keys(), expcnt, 'b+-')
    # #l2,=plt.plot(jmrecs.keys(), hitcnt, 'y*-')
    l3,=plt.plot(jmrecs.keys(), opscnt, 'r+-')
    plt.ylim(0,max(expcnt))
    plt.legend([l1, l3], ["Expected ops","Actul ops"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('operation per second')
    plt.title('LOAD vs LATENCY(client: jazz,server: '+host+')  --  Average ping: '+ping+error+' -- Accepted RPS='+maxAcc+' -- Latency Diff50th,75th,95th='+std50latency+', '+std75latency+', '+std90latency)
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    plt.subplot(412)
    l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l4, l5, l6, l7], ["25th","50th","75th","90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(413)
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    plt.ylim(min(per50),numpy.median(per50)*5)
    plt.legend([l5], ["50th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(414)
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    plt.ylim(min(per50),numpy.median(per50)*2)
    plt.legend([l5], ["50th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    print ('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    
    plt.show()
                
    #for i in jmrecs.keys():
    #    print i,jmrecs.values()[i-1]
    #print len(jmrecs.keys()),jmrecs.keys()
    #print len(jmrecs.values()[1]),jmrecs.values()[0]

if __name__ == "__main__":
#     #lines=open(r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\ec2\ec2.txt','r+').readlines()
#     lines=open(r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\test\test.txt','r+').readlines()
#     for line in (lines):
#         host=line.rstrip('\n')
#         #path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\ec2\\'+host[1:]+'.txt'
#         
#         path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\test\\'+host[1:]+'.txt'
#         process(path,host[1:])
    maxAccArray=[] 
    excel=[]
    tmp=''
    #lines=open(r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\test\1eu1test.txt','r+').readlines()
    path=r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\round2\eu'
    open(path+'\max.csv', 'w').close()
    for file in os.listdir(path):
        current_file_path = os.path.join(path, file)
        if current_file_path.split('.')[-1]=="txt" and os.stat(current_file_path).st_size>30000:
                
                jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,std99latency,host=process(current_file_path)
                #plot50th(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path)
                #plotSeprate(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path)
                print current_file_path,': ',maxAcc
                print "errror",error
                #maxAccArray.append(maxAcc)
                tmp+=(current_file_path.split('\\')[-1].split('-')[2])  #the number
#                 tmp+=(',')
#                 tmp+=(current_file_path.split('\\')[-1].split('-')[1])     #the host
#                 tmp+=(',')
#                 tmp+=(current_file_path.split('\\')[-1].split('-')[3])     #the country
                if std50latency=='nan':
                    std50latency='0'
                tmp+=(','+maxAcc+','+ping+','+std50latency+','+std75latency+','+std90latency+','+std99latency+'\n')
                
                c=numpy.asarray(maxAcc)
                print type(c)
                ecdf = sm.distributions.ECDF(np.random.uniform(0, 10, 10))
#                x = np.linspace(min(c), max(c))
#                y = ecdf(x)
#                plt.step(x, y)
#                plt.show()            
                
                #print maxAccArray
                fi=open(path+'\max.csv','a')
                fi.write(tmp)
                print tmp
                tmp=''
                
#     for line in (lines):
#         host=line.rstrip('\n')
#         #path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\ec2\\'+host[1:]+'.txt'
#         
#         path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\test\\1eu1test\\'+str(i)+'-'+host[1:]+'.txt'
        
#         for i in range(2):
#             path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\test\\1eu1test\\'+str(i)+'-'+host[1:]+'.txt'
#             print host[1:]
#             jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency=process(path,host[1:])
#             plot50th(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency)
#             maxAccArray.append(maxAcc)
#         print maxAcc
        #plotSeprate(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error)