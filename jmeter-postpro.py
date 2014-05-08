'''
Created on 27-Jan-2014

this piece of code will postprocess the output of the jmeter and plot the experiment based on Load and Latency 

@author: hsn
'''

'''
linux=/homes/hs302/Dropbox/Reading Stuff/0-MyPhD/2exp-tcpdump/5qmul/jmeter/sg/jmeterrow4/test/testsg100-ed.txt
windows=F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\5qmul\\sg\\2sg5th20e10qm-ed.txt
'''

import sys
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
    latdecider=[]
    error=0
    maxAcc=''
    jmhostname=''
    host=path.split("\\")[-1]
    #if not(os.path.exists(path)):
    #    return
    lines=open(path,'r+').readlines()
    ping=lines[0].split(':')[0][:-4]
    for lineindx,line in enumerate(lines):
        line=line.rstrip('\n')  
        if line.startswith('#'):
            if(line[-1]!='0'):
                error+=1
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
        if line.startswith('jmeter hostname'):
            jmhostname=line.split(':')[1]
        if line.startswith('25thvalues'):
            latdecider.append(line.split(':')[1])
        if line.startswith('50thvalues'):
            latdecider.append(line.split(':')[1])
        if line.startswith('75thvalues'):
            latdecider.append(line.split(':')[1])

        if line.startswith('5025thvalue'):
            latdecider.append(line.split(':')[1])
        if line.startswith('5050thvalue'):
            latdecider.append(line.split(':')[1])
        if line.startswith('7525thvalue'):
            latdecider.append(line.split(':')[1])
        if line.startswith('7550thvalue'):
            latdecider.append(line.split(':')[1])
        if line.startswith('9025thvalue'):
            latdecider.append(line.split(':')[1])
        if line.startswith('9050thvalue'):
            latdecider.append(line.split(':')[1])
            
    for sample in jmrecs.values():
        expcnt.append(sample[0])
        hitcnt.append(sample[1])
        opscnt.append(sample[2])

        per25.append(sample[3])
        per50.append(sample[4])
        per75.append(sample[5])
        per90.append(sample[6])
        per99.append(sample[7])    

    if len(expcnt)<2:
        return
#     std50latency=str(numpy.median([i for i in per50 if i >= float(ping)+15])-float(ping))
    #print [i for i in per50 if i >= float(ping)+15]
    std50latency=str(numpy.percentile([i for i in per50 if i >= float(ping)+10]+[0],75))
    std75latency=str(numpy.percentile([i for i in per75 if i >= float(ping)+10]+[0],75))
    std90latency=str(numpy.percentile([i for i in per90 if i >= float(ping)+10]+[0],75))
    std99latency=str(numpy.percentile([i for i in per99 if i >= float(ping)+10]+[0],75))
    #print [i for i in per50 if i >= float(ping)+20]
    return jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,std99latency,host,jmhostname,latdecider
'''-----------------------------------------------------------------------------------------'''
def plotSeprate(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname,latdecider):
    
    plt.figure(figsize=(10,10))
    plt.figure(1)

    plt.subplot(611)
    # #l2,=plt.plot(jmrecs.keys(), hitcnt, 'y*-')
    l1,=plt.plot(jmrecs.keys(), expcnt, 'bo-')
    l3,=plt.plot(jmrecs.keys(), opscnt, 'r+-')
    plt.ylim(0,max(expcnt))
    plt.legend([l1, l3], ["Expected ops","Actul ops"],loc=4)
    plt.xlabel('Sec')
    plt.ylabel('operation per second')
    if len(latdecider)==3:
        plt.title('(client: '+jmhostname+' ,server: '+host+')--Avg ping:'+ping+'--Acc RPS='+maxAcc+'--Latency='+latdecider[0]+', '+latdecider[1]+', '+latdecider[2])
    elif len(latdecider)==6:
        plt.title('(client: '+jmhostname+' ,server: '+host+')--Avg ping:'+ping+'--Acc RPS='+maxAcc+'--Lat50th='+latdecider[0]+','+latdecider[1]+','+'Lat75th='+latdecider[2]+','+latdecider[3]+','+'Lat90th='+latdecider[4]+','+latdecider[5])
    else:
        plt.title('(client: '+jmhostname+' ,server: '+host+')--Avg ping:'+ping+'--Acc RPS='+maxAcc)
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    plt.subplot(612)
    #l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    plt.ylim(min(per25),numpy.median(per50)*10)
    plt.legend([l5, l6, l7], ["50th","75th","90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(613)
    l3,=plt.plot(jmrecs.keys(), abs((numpy.array(opscnt)/numpy.array(expcnt))*100-100), 'r+-')
    plt.ylim(0,60,10)
    #plt.ylim(min(per25),numpy.median(per50)*10)
    #plt.legend([l4], ["25th"],loc=2)
    #plt.xlabel('Sec')
    plt.ylabel('Thr Loss(%)')
    plt.grid()
    #plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(614)
    l5,=plt.plot(jmrecs.keys(), per50, 'g+-')
    #plt.ylim(min(per25),numpy.median(per50)*10)
    if len(latdecider)==6:
        plt.plot([min(jmrecs.keys())-1, max(jmrecs.keys())], [latdecider[0], latdecider[0]], 'b--')
    plt.ylim(min(per50),(float(ping))+60)
    plt.legend([l5], ["50th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    plt.subplot(615)
    l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    #plt.ylim(min(per25),numpy.median(per50)*10)
    if len(latdecider)==6:
        plt.plot([min(jmrecs.keys())-1, max(jmrecs.keys())], [latdecider[2], latdecider[2]], 'b--')
    plt.ylim(min(per75),(float(ping))+120)
    plt.legend([l6], ["75th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))


    plt.subplot(616)
    l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    #plt.ylim(min(per90),numpy.median(per90)*5)
    if len(latdecider)==6:
        plt.plot([min(jmrecs.keys())-1, max(jmrecs.keys())], [latdecider[4], latdecider[4]], 'b--')
    plt.ylim(min(per90),(float(ping))+150)
    plt.legend([l7], ["90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    print ('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'.png')

    #if not(os.path.isfile('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')):
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'.png')
    #plt.show()
    plt.clf()
'''-----------------------------------------------------------------------------------------'''
def plotboxplotThrVsLat(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname):
    
    print expcnt
    #print per50
    #print per90
    #print per99
    data50={}
    data75={}
    data90={} 
    data99={}
    for indx,item in enumerate(expcnt):
        item=int(item)
        if item not in data90.keys():
            data50[item]=[]
            data75[item]=[]            
            data90[item]=[]
            data99[item]=[]
        data50[item].append(float(per50[indx]))        
        data75[item].append(float(per75[indx]))
        data90[item].append(float(per90[indx]))
        data99[item].append(float(per99[indx]))
     

    import collections
    data50=collections.OrderedDict(sorted(data50.items()))
    data75=collections.OrderedDict(sorted(data75.items()))
    data90=collections.OrderedDict(sorted(data90.items()))
    data99=collections.OrderedDict(sorted(data99.items()))
    #print data50
    #print data75    
    #print data90
    #print data99 
    #plt.xticks(data50.keys(),data50.keys())
    
    xax=[]
    for i in data50.keys():
        xax.append(i/100)
    
    wid=1
#    plt.boxplot(data50.values(), notch=False,positions = xax)
 #   plt.boxplot(data90.values(), notch=False,positions = xax)
  #  plt.boxplot(data99.values(), notch=False,patch_artist=True,positions = xax)
    #plt.boxplot(x, notch, sym, vert, whis, positions, widths, patch_artist, bootstrap, usermedians, conf_intervals, hold)

    plt.figure(figsize=(18.5,18.5))
    plt.figure(1)
    plt.suptitle(path.split('\\')[-1])
    
    plt.subplot(221)
    ocs,lbls=plt.xticks(data50.keys(),data50.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data50.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    #plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
    plt.ylim(min(per25),numpy.percentile(per90,97))    
    plt.title('50th Percentile')
    
    o={}
    for item in data50.keys():
        #print np.median(b[item])
        o[item]=numpy.median(data50[item])
    o=collections.OrderedDict(sorted(o.items()))
    print o.keys(),o.values()
    plt.plot(o.keys(), o.values(), 'b+-')
    
    
    plt.subplot(222)
    ocs,lbls=plt.xticks(data75.keys(),data75.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    #plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
    plt.ylim(min(per25),numpy.percentile(per90,97))
    plt.title('75th Percentile')    
    
    plt.subplot(223)
    ocs,lbls=plt.xticks(data90.keys(),data90.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data90.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
    plt.ylim(min(per25),numpy.percentile(per90,97))    
    plt.title('90th Percentile')
    #plt.gca().xaxis.set_major_locator(plt.NullLocator())
    
    plt.subplot(224)
    ocs,lbls=plt.xticks(data99.keys(),data99.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data99.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    plt.ylim(min(per25),numpy.percentile(per99,95))
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per99), 95),20))    
    plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.title('99th Percentile')

    plt.rcParams.update({'font.size': 20})
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'limit.png')
    plt.show()
    #plt.clf()

'''-----------------------------------------------------------------------------------------'''
def plotboxplotThrVsLatRatioLatvalue(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname):
    
    data50={}
    data75={}
    data90={} 
    data99={}
    for indx,item in enumerate(expcnt):
        item=int(item)
        if item not in data90.keys():
            data50[item]=[]
            data75[item]=[]            
            data90[item]=[]
            data99[item]=[]
        data50[item].append(float(per50[indx]))        
        data75[item].append(float(per75[indx]))
        data90[item].append(float(per90[indx]))
        data99[item].append(float(per99[indx]))
     
    import collections
    data50=collections.OrderedDict(sorted(data50.items()))
    data75=collections.OrderedDict(sorted(data75.items()))
    data90=collections.OrderedDict(sorted(data90.items()))
    data99=collections.OrderedDict(sorted(data99.items()))
    
    xax=[]
    for i in data50.keys():
        xax.append(float(i/100.0))
    
    wid=1
    
    plt.figure(figsize=(18.5,18.5))
    plt.figure(1)
    plt.suptitle(path.split('\\')[-1])

        
    plt.subplot(221)
    a=[int(float(x)*100.0/float(max(data75.keys()))) for x in data75.keys()]
    #print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=10)
    plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    plt.ylabel('Throughput(op/sec) %')
    plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per75), 97),20),numpy.arange(0,int(numpy.percentile((per75), 97)-float(ping)),20))
    plt.xlim(float(ping),float(ping)+100)
    plt.title('75th Percentile')
    o={}
    for item in data75.keys():
        o[item]=numpy.median(data75[item])
    o=collections.OrderedDict(sorted(o.items()))
    #print o.keys(),o.values()
    plt.plot( o.values(),xax, 'r+-',label='Connected Medians')
    '''regression'''
    from scipy import stats
    import bisect
    from scipy.optimize import curve_fit
    gradient, intercept, r_value, p_value, std_err = stats.linregress(o.values()[bisect.bisect(xax,xax[-1]/2)-1:],xax[bisect.bisect(xax,xax[-1]/2)-1:])
    halfmax=bisect.bisect(xax,xax[-1]/2)        #Find the index of half of the max value
    xx= numpy.linspace(min(o.values()),max(o.values()),100)
    z=gradient*xx+intercept
    plt.plot(xx,z,'g',label='Linear Regression')
    '''error'''
    #from sklearn.metrics import mean_squared_error
    print 'actual latency:',o.values()[bisect.bisect(xax,xax[-1]/2)-1:]
    print 'act thr:',xax[bisect.bisect(xax,xax[-1]/2)-1:]
    print 'explatency',gradient*numpy.array(xax[bisect.bisect(xax,xax[-1]/2)-1:])+intercept
    
    '''fitting'''
    def fitFunc(x, a, b, c):
        #return a*x + b
        return a*(x**2)+b*x + c
    t=numpy.asarray(o.values()[bisect.bisect(xax,xax[-1]/2)-1:])
    noisy=numpy.asarray(xax[bisect.bisect(xax,xax[-1]/2)-1:])
    fitParams, fitCovariances = curve_fit(fitFunc, t, noisy)
    #print fitParams
    #print fitCovariances
    plt.plot(xx, fitFunc(xx, fitParams[0], fitParams[1], fitParams[2]),'ko-',markersize=3,label='Polynomial Regression')
    plt.legend(loc=4)
    print '221:linear(r_value,p_value,std_err):', r_value, p_value, std_err
    print '221:fitCovariances:', fitCovariances
    '''-------------------------------------------------------------------------------------------------------------------'''
    plt.subplot(222)
    a=[int(float(x)*100.0/float(max(data75.keys()))) for x in data75.keys()]
  #  print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=10)
    plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    a=[int(x*100/int(float(ping))) for x in numpy.arange(int(float(ping)),numpy.percentile((per75), 97),20)]
    plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per75), 97),20),a)
    plt.xlim(float(ping),numpy.percentile(per75,97))
    plt.title('75th Percentile')
    o={}
    for item in data75.keys():
        o[item]=numpy.median(data75[item])
    o=collections.OrderedDict(sorted(o.items()))
 #   print o.keys(),o.values()
    plt.plot( o.values(),xax, 'r+-',)
    '''regression'''
    gradient, intercept, r_value, p_value, std_err = stats.linregress(o.values()[bisect.bisect(xax,xax[-1]/2)-1:],xax[bisect.bisect(xax,xax[-1]/2)-1:])
    halfmax=bisect.bisect(xax,xax[-1]/2)        #Find the index of half of the max value
    xx= numpy.linspace(min(o.values()),max(o.values()),100)
    z=gradient*xx+intercept
    plt.plot(xx,z,'g')
    plt.legend(loc=4) 
#    print 'values',xax[halfmax-1:],o.values()[halfmax-1:]
    '''fitting'''
    def fitFunc(x, a, b, c):
        #return a*x + b
        return a*(x**2)+b*x + c
    t=numpy.asarray(o.values()[bisect.bisect(xax,xax[-1]/2)-1:])
    noisy=numpy.asarray(xax[bisect.bisect(xax,xax[-1]/2)-1:])
    fitParams, fitCovariances = curve_fit(fitFunc, t, noisy)
    #print fitParams
    #print fitCovariances
    plt.plot(xx, fitFunc(xx, fitParams[0], fitParams[1], fitParams[2]),'ko-',markersize=3)
    print '222:linear(r_value,p_value,std_err):', r_value, p_value, std_err
    print '222:fitCovariances:', fitCovariances
    '''-------------------------------------------------------------------------------------------------------------------'''
    plt.subplot(223)
    a=[int(float(x)*100.0/float(max(data90.keys()))) for x in data90.keys()]
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=10)
    plt.boxplot(data90.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    plt.ylabel('Throughput(op/sec) %')
    plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per90), 97),20),numpy.arange(0,int(numpy.percentile((per90), 97)-float(ping)),20))
    plt.xlim(float(ping),float(ping)+100)
    plt.xlabel('Latency(ms)')
    plt.title('90th Percentile')
    o={}
    for item in data90.keys():
        o[item]=numpy.median(data90[item])
    o=collections.OrderedDict(sorted(o.items()))
    #print o.keys(),o.values()
    plt.plot( o.values(),xax, 'r+-',)
    #plt.gca().xaxis.set_major_locator(plt.NullLocator())
    '''regression'''
    gradient, intercept, r_value, p_value, std_err = stats.linregress(o.values()[bisect.bisect(xax,xax[-1]/2)-1:],xax[bisect.bisect(xax,xax[-1]/2)-1:])
    halfmax=bisect.bisect(xax,xax[-1]/2)        #Find the index of half of the max value
   # print 'values',xax[halfmax-1:],o.values()[halfmax-1:]    
    #print o.values()
   # print "Gradient and intercept and error:", gradient, intercept,p_value, std_err
    xx= numpy.linspace(min(o.values()),max(o.values()),100)
    z=gradient*xx+intercept
    plt.plot(xx,z,'g')
    plt.legend(loc=4)       
    '''fitting'''
    def fitFunc(x, a, b, c):
        #return a*x + b
        return a*(x**2)+b*x + c
    t=numpy.asarray(o.values()[bisect.bisect(xax,xax[-1]/2)-1:])
    noisy=numpy.asarray(xax[bisect.bisect(xax,xax[-1]/2)-1:])
    fitParams, fitCovariances = curve_fit(fitFunc, t, noisy)
    #print fitParams
    #print fitCovariances
    plt.plot(xx, fitFunc(xx, fitParams[0], fitParams[1], fitParams[2]),'ko-',markersize=3)
    print '223:linear(r_value,p_value,std_err):', r_value, p_value, std_err
    print '223:fitCovariances:', fitCovariances
    '''-------------------------------------------------------------------------------------------------------------------'''
    plt.subplot(224)
    a=[int(float(x)*100.0/float(max(data90.keys()))) for x in data90.keys()]
    #print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=10)
    plt.boxplot(data90.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()        
    a=[int(x*100/int(float(ping))) for x in numpy.arange(int(float(ping)),numpy.percentile((per90), 97),20)]
    plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per90), 97),20),a)
    plt.xlim(float(ping),numpy.percentile(per75,97))
    plt.xlabel('Latency(%)')
    plt.title('90th Percentile1')
    o={}
    for item in data90.keys():
        o[item]=numpy.median(data90[item])
    o=collections.OrderedDict(sorted(o.items()))
    #print o.keys(),o.values()
    plt.plot( o.values(),xax, 'r+-')
    '''regression'''
    gradient, intercept, r_value, p_value, std_err = stats.linregress(o.values()[bisect.bisect(xax,xax[-1]/2)-1:],xax[bisect.bisect(xax,xax[-1]/2)-1:])
    halfmax=bisect.bisect(xax,xax[-1]/2)        #Find the index of half of the max value
    #print xax[halfmax-1:],o.values()[halfmax-1:]    
    #print o.values()
    #print "Gradient and intercept and error:", gradient, intercept,std_err
    xx= numpy.linspace(min(o.values()),max(o.values()),100)
    z=gradient*xx+intercept
    plt.plot(xx,z,'g')
    plt.legend(loc=4)       
    '''fitting'''
    def fitFunc(x, a, b, c):
        #return a*x + b
        return a*(x**2)+b*x + c
    t=numpy.asarray(o.values()[bisect.bisect(xax,xax[-1]/2)-1:])
    noisy=numpy.asarray(xax[bisect.bisect(xax,xax[-1]/2)-1:])
    fitParams, fitCovariances = curve_fit(fitFunc, t, noisy)
    #print fitParams
    #print fitCovariances
    plt.plot(xx, fitFunc(xx, fitParams[0], fitParams[1], fitParams[2]),'ko-',markersize=3)
    print '224:linear(r_value,p_value,std_err):', r_value, p_value, std_err
    print '224:fitCovariances:', fitCovariances

    plt.rcParams.update({'font.size': 20})
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'limit.png')
    plt.show()
    #plt.clf()


'''-----------------------------------------------------------------------------------------'''
def plotboxplotThrVsLatratio(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname):
    
    print expcnt
    #print per50
    #print per90
    #print per99
    data50={}
    data75={}
    data90={} 
    data99={}
    for indx,item in enumerate(expcnt):
        item=int(item)
        if item not in data90.keys():
            data50[item]=[]
            data75[item]=[]            
            data90[item]=[]
            data99[item]=[]
        data50[item].append(float(per50[indx]))        
        data75[item].append(float(per75[indx]))
        data90[item].append(float(per90[indx]))
        data99[item].append(float(per99[indx]))
     

    import collections
    data50=collections.OrderedDict(sorted(data50.items()))
    data75=collections.OrderedDict(sorted(data75.items()))
    data90=collections.OrderedDict(sorted(data90.items()))
    data99=collections.OrderedDict(sorted(data99.items()))
    #print data50
    #print data75    
    #print data90
    #print data99 
    #plt.xticks(data50.keys(),data50.keys())
    
    xax=[]
    for i in data50.keys():
        xax.append(i/100)
    
    wid=1
    isxaxlat=True
    
    plt.figure(figsize=(18.5,18.5))
    plt.figure(1)
    plt.suptitle(path.split('\\')[-1])
    
    plt.subplot(221)
    a=[int(float(x)*100.0/float(max(data50.keys()))) for x in data50.keys()]
    print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=12)
    plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    plt.ylabel('Throughput(op/sec) %')
    plt.xlim(float(ping),numpy.percentile(per50,97))
    if isxaxlat==True:    
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per50), 97),20),numpy.arange(0,int(numpy.percentile((per50), 97)-float(ping)),20))
    else:
        a=[int(x*100/int(float(ping))) for x in numpy.arange(int(float(ping)),numpy.percentile((per50), 97),10)]
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per50), 97),10),a)
    plt.title('50th Percentile')
    
#     plt.subplot(222)
#     ocs,lbls=plt.xticks(data75.keys(),data75.keys())
#     plt.setp(lbls, rotation=90, fontsize=12)
#     plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid)
#     plt.grid()
#     #plt.xlabel('Throughput(op/sec)')
#     plt.ylabel('Latency(ms)')
#     plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
#     plt.ylim(min(per25),numpy.percentile(per90,97))
#     plt.title('75th Percentile')    

    plt.subplot(222)
    a=[int(float(x)*100.0/float(max(data75.keys()))) for x in data75.keys()]
    print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=12)
    plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    plt.ylabel('Throughput(op/sec) %')
    #plt.xlabel('Latency(ms)')
    print "per25",numpy.percentile(per25,25),min(per25),min(data75[data75.keys()[1]]),ping
    plt.xlim(float(ping),numpy.percentile(per75,97))
    if isxaxlat==True:    
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per75), 97),20),numpy.arange(0,int(numpy.percentile((per75), 97)-float(ping)),20))
    else:
        a=[int(x*100/int(float(ping))) for x in numpy.arange(int(float(ping)),numpy.percentile((per75), 97),20)]
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per75), 97),20),a)
    plt.title('75th Percentile')
     
    plt.subplot(223)
    a=[int(float(x)*100.0/float(max(data90.keys()))) for x in data90.keys()]
    #print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=12)
    plt.boxplot(data90.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    plt.ylabel('Throughput(op/sec) %')
    #print "per25",numpy.percentile(per25,25),min(per25),min(data90[data90.keys()[1]]),ping
    plt.xlim(float(ping),numpy.percentile(per90,97))    
    #a=[int(float(x)*100.0/float(max(data90.keys()))) for x in data90.keys()]
    if isxaxlat==True:    
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per90), 97),20),numpy.arange(0,int(numpy.percentile((per90), 97)-float(ping)),20))
        plt.xlabel('Latency(ms)')
    else:
        a=[int(x*100/int(float(ping))) for x in numpy.arange(int(float(ping)),numpy.percentile((per90), 97),20)]
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per90), 97),20),a)
        plt.xlabel('Latency(%)')
    plt.title('90th Percentile')
    #plt.gca().xaxis.set_major_locator(plt.NullLocator())
    print 'Maxacc:',maxAcc
    o={}
    for item in data50.keys():
        #print np.median(b[item])
        o[item]=numpy.median(data50[item])
    o=collections.OrderedDict(sorted(o.items()))
    print o.keys(),o.values()
    plt.plot(o.values(),o.keys(), 'b+-')

    plt.subplot(224)
    a=[int(float(x)*100.0/float(max(data99.keys()))) for x in data99.keys()]
    print 'list',a
    ocs,lbls=plt.yticks(a,a)
    plt.setp(lbls, rotation=0, fontsize=12)
    plt.boxplot(data99.values(), notch=False,positions = xax,widths = wid,vert=0)
    plt.grid()
    plt.ylabel('Throughput(op/sec) %')
    print "per25",numpy.percentile(per25,25),min(per25),min(data99[data99.keys()[1]]),ping
    plt.xlim(float(ping),numpy.percentile(per99,97))    
    #a=[int(float(x)*100.0/float(max(data90.keys()))) for x in data90.keys()]
    if isxaxlat==True:    
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per99), 97),20),numpy.arange(0,int(numpy.percentile((per99), 97)-float(ping)),20))
        plt.xlabel('Latency(ms)')
    else:
        a=[int(x*100/int(float(ping))) for x in numpy.arange(int(float(ping)),numpy.percentile((per99), 97),20)]
        plt.xticks(numpy.arange(int(float(ping)),numpy.percentile((per99), 97),20),a)
        plt.xlabel('Latency(%)')
    plt.title('99th Percentile')

    plt.rcParams.update({'font.size': 20})
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'limit.png')
    plt.show()
    #plt.clf()


'''-----------------------------------------------------------------------------------------'''
def plotboxplotThrVsLatbkp(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname):
    
    print expcnt
    #print per50
    #print per90
    #print per99
    data50={}
    data75={}
    data90={} 
    data99={}
    for indx,item in enumerate(expcnt):
        item=int(item)
        if item not in data90.keys():
            data50[item]=[]
            data75[item]=[]            
            data90[item]=[]
            data99[item]=[]
        data50[item].append(float(per50[indx]))        
        data75[item].append(float(per75[indx]))
        data90[item].append(float(per90[indx]))
        data99[item].append(float(per99[indx]))
     

    import collections
    data50=collections.OrderedDict(sorted(data50.items()))
    data75=collections.OrderedDict(sorted(data75.items()))
    data90=collections.OrderedDict(sorted(data90.items()))
    data99=collections.OrderedDict(sorted(data99.items()))
    #print data50
    #print data75    
    #print data90
    #print data99 
    #plt.xticks(data50.keys(),data50.keys())
    
    xax=[]
    for i in data50.keys():
        xax.append(i/100)
    
    wid=1
#    plt.boxplot(data50.values(), notch=False,positions = xax)
 #   plt.boxplot(data90.values(), notch=False,positions = xax)
  #  plt.boxplot(data99.values(), notch=False,patch_artist=True,positions = xax)
    #plt.boxplot(x, notch, sym, vert, whis, positions, widths, patch_artist, bootstrap, usermedians, conf_intervals, hold)


    
    plt.figure(figsize=(18.5,18.5))
    plt.figure(1)
    print path
    plt.suptitle(path.split('\\')[-1])
     
    plt.subplot(221)
    ocs,lbls=plt.xticks(data50.keys(),data50.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data50.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    #plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
    plt.ylim(min(per25),numpy.percentile(per90,97))    
    plt.title('50th Percentile')
     
    o={}
    for item in data50.keys():
        #print np.median(b[item])
        o[item]=numpy.median(data50[item])
    o=collections.OrderedDict(sorted(o.items()))
    print o.keys(),o.values()
    plt.plot(xax, o.values(), 'b+-',)
     
     
    plt.subplot(222)
    ocs,lbls=plt.xticks(data75.keys(),data75.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data75.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    #plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
    plt.ylim(min(per25),numpy.percentile(per90,97))
    plt.title('75th Percentile')    
    o={}
    for item in data75.keys():
        #print np.median(b[item])
        o[item]=numpy.median(data75[item])
    o=collections.OrderedDict(sorted(o.items()))
    print o.keys(),o.values()
    plt.plot(xax, o.values(), 'b+-',)

    
    plt.subplot(223)
    ocs,lbls=plt.xticks(data90.keys(),data90.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data90.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per90), 97),20))
    plt.ylim(min(per25),numpy.percentile(per90,97))    
    plt.title('90th Percentile')
    o={}
    for item in data90.keys():
        #print np.median(b[item])
        o[item]=numpy.median(data90[item])
    o=collections.OrderedDict(sorted(o.items()))
    print o.keys(),o.values()
    plt.plot(xax, o.values(), 'b+-',)

    #plt.gca().xaxis.set_major_locator(plt.NullLocator())
     
    plt.subplot(224)
    ocs,lbls=plt.xticks(data99.keys(),data99.keys())
    plt.setp(lbls, rotation=90, fontsize=12)
    plt.boxplot(data99.values(), notch=False,positions = xax,widths = wid)
    plt.grid()
    plt.ylim(min(per25),numpy.percentile(per99,95))
    plt.yticks(numpy.arange(min(per25),numpy.percentile((per99), 95),20))    
    plt.xlabel('Throughput(op/sec)')
    plt.ylabel('Latency(ms)')
    plt.title('99th Percentile')
 
    plt.rcParams.update({'font.size': 20})
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'limit.png')
    plt.show()
    #plt.clf()

'''-----------------------------------------------------------------------------------------'''
def plotSepratePaper(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname):
    
    plt.figure(figsize=(10,10))
    plt.figure(1)

    plt.subplot(411)
    l1,=plt.plot(jmrecs.keys(), expcnt, 'bo-')
    # #l2,=plt.plot(jmrecs.keys(), hitcnt, 'y*-')
    l3,=plt.plot(jmrecs.keys(), opscnt, 'r+-')
    plt.ylim(0,max(expcnt))
    plt.legend([l1,l3], ["Expected Throughput","Actual Throughput"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Operation per Second')
    #plt.title('LOAD vs LATENCY(client: '+jmhostname+' ,server: '+host+')  --  Average ping: '+ping+' -- Accepted RPS='+maxAcc+' -- Latency Diff50th,75th,95th='+std50latency+', '+std75latency+', '+std90latency)
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    #plt.subplot(412)
    #l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
    #l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    #l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    #l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    #plt.ylim(min(per25),numpy.median(per50)*10)
    #plt.legend([l4, l5, l6, l7], ["25th","50th","75th","90th"],loc=2)
    #plt.xlabel('Sec')
    #plt.ylabel('Latency(msec)')
    #plt.grid()
    #plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    #plt.subplot(412)
    #l4,=plt.plot(jmrecs.keys(), per25, 'gs-')
    #plt.ylim(min(per25),numpy.median(per50)*10)
    #plt.legend([l4], ["25th"],loc=2)
    #plt.xlabel('Sec')
    #plt.ylabel('Latency(msec)')
    #plt.grid()
    #plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(412)
    l5,=plt.plot(jmrecs.keys(), per50, 'g--')
    #plt.ylim(min(per25),numpy.median(per50)*10)
    plt.ylim(min(per50),(float(ping))+40)
    plt.legend([l5], ["50th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(413)
    l6,=plt.plot(jmrecs.keys(), per75, 'g^-')
    #plt.ylim(min(per25),numpy.median(per50)*10)
    plt.ylim(min(per75),(float(ping))+80)
    plt.legend([l6], ["75th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    plt.subplot(414)
    l7,=plt.plot(jmrecs.keys(), per90, 'g*-')
    #plt.ylim(min(per90),numpy.median(per90)*5)
    plt.ylim(min(per90),(float(ping))+100)
    plt.legend([l7], ["90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    print ('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'.png')

    #if not(os.path.isfile('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')):
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'.png')
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'.eps')
    #plt.show()
    plt.clf()
'''-------------------------------------------------------------------------------------------------------------'''

'''-------------------------------------------------------------------------------------------------------------'''

def plottrflatencypaper(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99,maxAcc,ping,error,std50latency,std75latency,std90latency,host,path,jmhostname):
    
    plt.figure(figsize=(10,10))
    plt.figure(1)

    min1=12
    max1=50
    
    expcnt=expcnt[min1:max1]
    opscnt=opscnt[min1:max1]
    per25=per25[min1:max1]
    per50=per50[min1:max1]
    per75=per75[min1:max1]
    per90=per90[min1:max1]
    keys=jmrecs.keys()[min1:max1]
    
    plt.subplot(211)
    l1,=plt.plot(keys, expcnt, 'bo-')
    # #l2,=plt.plot(jmrecs.keys(), hitcnt, 'y*-')
    
    
    l3,=plt.plot(keys, opscnt, 'r+-')
    plt.ylim(0,max(expcnt)+500)
    plt.xlim(min1,max1+3)
    plt.legend([l1, l3], ["Expected Throughput","Actual Throughput"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Operation Per Second')
    #plt.title('LOAD vs LATENCY(client: '+jmhostname+' ,server: '+host+')  --  Average ping: '+ping+' -- Accepted RPS='+maxAcc+' -- Latency Diff50th,75th,95th='+std50latency+', '+std75latency+', '+std90latency)
    plt.grid()
    #plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))
    
    plt.subplot(212)
    l4,=plt.plot(keys, per25, 'gs-')
    l5,=plt.plot(keys, per50, 'g--')
    l6,=plt.plot(keys, per75, 'g^-')
    l7,=plt.plot(keys, per90, 'g*-')
    plt.ylim(min(per25),numpy.median(per50)*15)
    plt.xlim(min1,max1+3)
    plt.legend([l4, l5, l6, l7], ["25th","50th","75th","90th"],loc=2)
    plt.xlabel('Sec')
    plt.ylabel('Latency(msec)')
    plt.grid()
    #plt.xticks(range(min(jmrecs.keys())-1,max(jmrecs.keys()),10))

    
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    print ('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'.png')

    #if not(os.path.isfile('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')):
    #figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'limit.png')
    figure.savefig('\\'.join(path.split('\\')[:-1])+'\\'+jmhostname+'!'+path.split('\\')[-1][:-4]+'limit.eps')
    #plt.show()
    plt.clf()

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
    plt.title('LOAD vs LATENCY(client: jazz,server: '+host+')  --  Average ping: '+ping+' -- Accepted RPS='+maxAcc+' -- Latency Diff50th,75th,95th='+std50latency+', '+std75latency+', '+std90latency)
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
    
    #if not(os.path.isfile('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')):
     #   figure.savefig('\\'.join(path.split('\\')[:-1])+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    
    #plt.show()
                
    #for i in jmrecs.keys():
    #    print i,jmrecs.values()[i-1]
    #print len(jmrecs.keys()),jmrecs.keys()
    #print len(jmrecs.values()[1]),jmrecs.values()[0]
'''-----------------------------------------------------------------------------------------'''
def boxplt(maxacclist):
     
    mstpltlst=[]
    #maxacclist.sort(key=lambda x: x[1])
    for node in (maxacclist):
        mstpltlst.append(float(node[1]))
    plt.boxplot(mstpltlst,0,'')
    plt.show()
'''-----------------------------------------------------------------------------------------'''
def timeserieplot(maxacclist):
    alldata={} 
    print maxacclist
    for i in maxacclist:
        alldata[int(i[0].split('.')[-2].split('-')[-1])]=i[1]
    print maxacclist
    print alldata
    import collections
    
    #alldata=collections.OrderedDict(sorted(alldata.items()))
    #print alldata
    print len(alldata.values())
    xax=[]
    #for i in range(len(alldata.values())):
     #   xax.append(i*3)
    for i in ((alldata.keys())):
        xax.append(i*3)
    plt.plot(xax,alldata.values(),'bo-',linewidth=5.0,markersize=15)

    #ocs,lbls=plt.xticks([i for i in range(len(alldata.keys()))],alldata.keys())
    #ocs,lbls=plt.xticks([i for i in range(len(xax))],xax)
    #plt.setp(lbls, rotation=90, fontsize=8)
    #plt.yticks(numpy.arange(0, 20000, 2500))    
    plt.grid()
    #plt.xlim(0,299)
    #plt.ylim(0,20000)
    plt.ylabel('Operation per Second')
    plt.xlabel('Time(Min)')
    #print alldata.keys()[0][:5]
    title='Throughput discovered by benchmark-- (Number of samples from left to right:'
    for i in alldata.keys():
        title+=str(len(alldata[i]))+' -- '
    title+=')'
    #plt.title(title)
    #plt.tick_params(axis='x', which='major', labelsize=13)
    #plt.tick_params(axis='y', which='major', labelsize=15)
    plt.rcParams.update({'font.size': 30})
    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    print '\\'.join(path.split('\\'))+'\\ex1'+path.split('\\')[-1][:-4]+'.png'
    figure.savefig('\\'.join(path.split('\\'))+'\\ex1'+path.split('\\')[-1][:-4]+'.png')
    plt.show()

'''-----------------------------------------------------------------------------------------'''
def boxplotcdflatency(maxacclist50,maxacclist75,maxacclist90,type,whichperc):
    alldata=maxacclist
    import collections
    maxacclist50=collections.OrderedDict(sorted(maxacclist50.items()))
    maxacclist75=collections.OrderedDict(sorted(maxacclist75.items()))
    maxacclist90=collections.OrderedDict(sorted(maxacclist90.items()))
    #print len(maxacclist.values())
    xax=[]
    xax1=[]
    xax2=[]
    import numpy as np
    import statsmodels.api as sm # recommended import according to the docs

    for i in range(len(maxacclist90.keys())):
        xax.append(i*6)
        xax1.append(i*6+1)
        xax2.append(i*6+2)
    #xax=numpy.array(range(len(maxacclist90.keys())))*6
    #xax1=(numpy.array(range(len(maxacclist75.keys())))+1)*6
    #for i in maxacclist90.keys():
     #   xax.append(i/500)
    boxplotorCdf=type
    if boxplotorCdf=='b' and whichperc=='all':
        #plt.boxplot(maxacclist90.values())
        b1=plt.boxplot(maxacclist50.values(), notch=False,positions = xax,widths=1,patch_artist=True)
        b2=plt.boxplot(maxacclist75.values(), notch=False,positions = xax1,widths=1,patch_artist=True)
        b3=plt.boxplot(maxacclist90.values(), notch=False,positions = xax2,widths=1,patch_artist=True)
        plt.setp(b1['boxes'], color='red')
        plt.setp(b2['boxes'], color='cyan')
        plt.setp(b3['boxes'], color='magenta')
        '''drawing 3plots for legends'''
        lg1, = plt.plot([1,1],'r-')
        lg2, = plt.plot([1,1],'c-')
        lg3, = plt.plot([1,1],'m-')
        plt.legend((lg3, lg2,lg1),('95th', '75th','50th'),loc=2)
    elif whichperc=='50':
        b1=plt.boxplot(maxacclist50.values(),patch_artist=True)
        plt.setp(b1['boxes'], color='red')
    elif whichperc=='75':
        b2=plt.boxplot(maxacclist75.values(),patch_artist=True)
        plt.setp(b2['boxes'], color='cyan')
    elif whichperc=='90':
        b3=plt.boxplot(maxacclist90.values(),patch_artist=True)
        plt.setp(b3['boxes'], color='magenta')
    
   
    

#    elif boxplotorCdf=='s':
 #       for i in range(len(maxacclist90.values())):
  #          xax.append([i+1] * len(maxacclist90.values()[i]))
   #         plt.plot(xax[i],maxacclist90.values()[i],'b+',markersize=19)
    #else:
     #   for i in range(len(maxacclist90.values())):
      #      ecdf = sm.distributions.ECDF(maxacclist90.values()[i])
       #     x = np.linspace(0, 200)
        #    y = ecdf(x)
        #    plt.step(x, y)

    #plt.plot([9.5, 9.5], [0, 12000], 'k--',markersize=15)
    #plt.plot([18.5, 18.5], [0,12000], 'k--',markersize=19)
    
    if whichperc=='all':
        ocs,lbls=plt.xticks(xax1,[x for x in maxacclist90.keys()])
    else:
        ocs,lbls=plt.xticks([i+1 for i in range(len(maxacclist90.keys()))],maxacclist90.keys())
    plt.setp(lbls, rotation=90, fontsize=8)
    #plt.yticks(numpy.arange(0, 100, 10))    
    plt.grid()
    #plt.xlim(0,(len(maxacclist90.values()))+1)

    plt.ylabel('Latency over the Ping(ms)')
    plt.xlabel('Expected Throughput (ops/secs)')
    title='Latency vs throughput'
    plt.rcParams.update({'font.size': 15})
    plt.tick_params(axis='x', which='major', labelsize=15)

    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #print '\\'.join(path.split('\\'))+'\\ex1'+path.split('\\')[-1][:-4]+'.png'
    if whichperc=='50':
        plt.ylim(0,max(maxacclist90.values()[-1]))
        figure.savefig('\\'.join(path.split('\\'))+'\\laten50'+path.split('\\')[-1][:-4]+'.png')   
    elif whichperc=='75' :
        plt.ylim(0,max(maxacclist90.values()[-1]))
        figure.savefig('\\'.join(path.split('\\'))+'\\laten75'+path.split('\\')[-1][:-4]+'.png')        
    elif whichperc=='90':
        plt.ylim(0,max(maxacclist90.values()[-1]))
        figure.savefig('\\'.join(path.split('\\'))+'\\laten90'+path.split('\\')[-1][:-4]+'.png')        
    elif whichperc=='all':
        #print max(maxacclist90.values()[-1])
        plt.ylim(0,max(maxacclist90.values()[-1]))
        figure.savefig('\\'.join(path.split('\\'))+'\\latenall'+path.split('\\')[-1][:-4]+'.png')        

    #
    plt.show()
'''-----------------------------------------------------------------------------------------'''
def boxplotcdfThroughputLoss(maxacclist,type):
    print "loss"
    alldata=maxacclist
      
#     for i in maxacclist:
#         if i[0][0]=='z':
#             break;
#         if any(char.isdigit() for char in (i[0].split(".")[0])):
#             i[0]=(i[0].split(".")[0][:-1])[4:].upper()
#         else:
#             i[0]=(i[0].split(".")[0])[4:].upper()
#     
#     for i in maxacclist:
#         #print i
#         if i[0] not in alldata.keys():
#             alldata[i[0]]=[]
#         #alldata[i[0]].append(float(i[1]))
#         for x in (i[1]):
#             alldata[i[0]].append(float(x))
    import collections
    alldata=collections.OrderedDict(sorted(alldata.items()))
    #print len(maxacclist.values())
    xax=[]
    import numpy as np
    import statsmodels.api as sm # recommended import according to the docs

    boxplotorCdf=type
    if boxplotorCdf=='b':
        plt.boxplot(alldata.values())
        print alldata.values()
    elif boxplotorCdf=='s':
        for i in range(len(alldata.values())):
            xax.append([i+1] * len(alldata.values()[i]))
            plt.plot(xax[i],alldata.values()[i],'b+',markersize=19)
    else:
        for i in range(len(alldata.values())):
            ecdf = sm.distributions.ECDF(alldata.values()[i])
            x = np.linspace(0, 200)
            y = ecdf(x)
            plt.step(x, y)

    #plt.plot([9.5, 9.5], [0, 12000], 'k--',markersize=15)
    #plt.plot([18.5, 18.5], [0,12000], 'k--',markersize=19)
    ocs,lbls=plt.xticks([i+1 for i in range(len(alldata.keys()))],alldata.keys())
    plt.setp(lbls, rotation=90, fontsize=8)
    plt.yticks(numpy.arange(0, 100, 10))    
    plt.grid()
    plt.xlim(0,(len(alldata.values()))+1)
    plt.ylim(0,50)
    plt.ylabel('Throughput Loss %')
    plt.xlabel('Expected Throughput (ops/secs)')
    title='Throughput loss'
    plt.rcParams.update({'font.size': 15})
    plt.tick_params(axis='x', which='major', labelsize=15)

    figure = plt.gcf() # get current figure
    figure.set_size_inches(18.5,10.5 )
    #print '\\'.join(path.split('\\'))+'\\ex1'+path.split('\\')[-1][:-4]+'.png'
    figure.savefig('\\'.join(path.split('\\'))+'\\loss'+path.split('\\')[-1][:-4]+'.png')

    plt.show()
   
'''-----------------------------------------------------------------------------------------'''
def cdfplot(maxacclist):
    alldata={} 
    for i in maxacclist:
        if i[0][0]=='z':
            break;
        if any(char.isdigit() for char in (i[0].split(".")[0])):
            i[0]=(i[0].split(".")[0][:-1])[4:].upper()
        else:
            i[0]=(i[0].split(".")[0])[4:].upper()
    
    for i in maxacclist:
        #print i
        if i[0] not in alldata.keys():
            alldata[i[0]]=[]
        alldata[i[0]].append(float(i[1]))
    import collections
    alldata=collections.OrderedDict(sorted(alldata.items()))
    print len(alldata.values())
    xax=[]
    import numpy as np
    import statsmodels.api as sm # recommended import according to the docs
    import matplotlib.pyplot as plt

    boxplotorCdf='c'
    if boxplotorCdf=='b':
        plt.boxplot(alldata.values())
    else:
        for i in range(len(alldata.values())):
            ecdf = sm.distributions.ECDF(alldata.values()[i])
            x = np.linspace(0, 12000)
            y = ecdf(x)
            plt.step(x, y)
    plt.show()
        #xax.append([i+1] * len(alldata.values()[i]))
        #plt.plot(xax[i],alldata.values()[i],'b+',markersize=19)
        
    
'''-----------------------------------------------------------------------------------------'''
def scatterorboxplotPercLat(maxacclist,type):
    alldata={} 
    boxplotOrScatter=type
    for i in maxacclist:
        if i[0][0]=='z':
            break;
        if any(char.isdigit() for char in (i[0].split(".")[0])):
            i[0]=(i[0].split(".")[0][:-1])[4:].upper()
        else:
            i[0]=(i[0].split(".")[0])[4:].upper()
    
    for i in maxacclist:
        #print i
        if i[0] not in alldata.keys():
            alldata[i[0]]=[]
        alldata[i[0]].append(float(i[1]))
    import collections
    alldata=collections.OrderedDict(sorted(alldata.items()))
    print len(alldata.values())
    xax=[]
    if boxplotOrScatter=='b':
        plt.boxplot(alldata.values())
    else:
        for i in range(len(alldata.values())):
            xax.append([i+1] * len(alldata.values()[i]))
            plt.plot(xax[i],alldata.values()[i],'b+',markersize=15)
    
    plt.plot([9.5, 9.5], [0, 12000], 'k--')
    plt.plot([18.5, 18.5], [0,12000], 'k--')
    ocs,lbls=plt.xticks([i+1 for i in range(len(alldata.keys()))],alldata.keys())
    plt.setp(lbls, rotation=90, fontsize=8)
    plt.yticks(numpy.arange(0, 20000, 1000))    
    plt.grid()
    plt.xlim(0,(len(alldata.values()))+1)
    plt.ylim(0,12000)
    plt.ylabel('operation per second')
 #   if alldata.keys()[0][:5]=='1STAN':
    #    plt.xlabel('VM Types(Google Compute Engine)')
   # elif alldata.keys()[0][:5]=='1MICR':
   #     plt.xlabel('VM Types(Amazon Ec2)')
  #  elif alldata.keys()[0][:5]=='LARAS':
  #      plt.xlabel('VM Types(Microsoft Azure)')
    print alldata.keys()[0][:5]
    title='Throughput discovered by benchmark-- (Number of samples from left to right:'
    for i in alldata.keys():
        title+=str(len(alldata[i]))+' -- '
    title+=')'
    #plt.title(title)
    plt.rcParams.update({'font.size': 30})
    plt.tick_params(axis='x', which='major', labelsize=11)
    
    plt.show()
'''-----------------------------------------------------------------------------------------'''
def boxpltall(maxacclist,path):
    alldata={} 
    for i in maxacclist:
        if any(char.isdigit() for char in (i[0].split(".")[0])):
            i[0]=(i[0].split(".")[0][:-1])[4:].upper()
        else:
            i[0]=(i[0].split(".")[0])[4:].upper()
    
    for i in maxacclist:
        if i[0] not in alldata.keys():
            alldata[i[0]]=[]
        alldata[i[0]].append(float(i[1]))

    import collections
    alldata=collections.OrderedDict(sorted(alldata.items()))
    
    '''add data to csv file'''
    import csv
    with open(path+'\output.csv', "wb") as f:
        for i in alldata.keys():
            writer = csv.writer(f)
            writer = csv.writer(f, delimiter=',')
            print alldata[i]
            writer.writerow(alldata[i])
    
    box=plt.boxplot(alldata.values(),'', patch_artist=True)
    color=[]
    #color = ['cyan', 'lightblue', 'lightgreen', 'tan', 'pink']
    print  alldata.keys()
    for i in alldata.keys():
        if i[:3]=='LAR' :
            color.append('pink')
        if i[:3]=='MED' or i[:3]=='3ME' or i[:3]=='1ST':
            color.append('cyan')
        if i[:3]=='SMA' or i[:3]=='2SM' or i[:3]=='2ST':
            color.append('red')
        if i[:3]=='SHA' or i[:3]=='1MI' or i[:3]=='3ST':
            color.append('blue')
        if i[:3]=='5XL':
            color.append('green')

    for patch,col in zip(box['boxes'],color):
        patch.set_facecolor(col)
    
    locs,lbls=plt.xticks([i+1 for i in range(len(alldata.keys()))],alldata.keys())
    #lbl = plt.xticks()
    plt.setp(lbls, rotation=90, fontsize=8)
    plt.grid()
    plt.ylabel('operation per second')
    #plt.xlabel('VM Types(Google Compute Engine)')
    title='Throughput discovered by benchmark-- (Number of samples from left to right:'
    if alldata.keys()[0][:5]=='1STAN':
        plt.xlabel('VM Types(Google Compute Engine)')
    elif alldata.keys()[0][:5]=='1MICR':
        plt.xlabel('VM Types(Amazon Ec2)')
   # elif alldata.keys()[0][:5]=='LARAS':
    #    plt.xlabel('VM Types(Microsoft Azure)')

    plt.tick_params(axis='x', which='major', labelsize=13)
    #plt.tick_params(axis='y', which='major', labelsize=15)
    plt.rcParams.update({'font.size': 30})
    plt.title('VM Types(Microsoft Azure)')
    
    for i in alldata.keys():
        title+=str(len(alldata[i]))+' -- '
    title+=')'
    #plt.title(title)
    
    plt.show()

if __name__ == "__main__":
#     #lines=open(r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\ec2\ec2.txt','r+').readlines()
#     lines=open(r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\test\test.txt','r+').readlines()
#     for line in (lines):
#         host=line.rstrip('\n')
#         #path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\ec2\\'+host[1:]+'.txt'
#         
#         path='F:\\Dropbox\\Dropbox\\Reading Stuff\\0-MyPhD\\2exp-tcpdump\\6jmeter\\test\\'+host[1:]+'.txt'
#         process(path,host[1:])
    maxacclist=[]
    throghputlosslist={}
    latencylist50={}
    latencylist75={}
    latencylist90={}
    maxaccall={}
    maxAccArray=[] 
    excel=[]
    tmp=''
    jmhostname=''

#     import numpy as np
#     import statsmodels.api as sm # recommended import according to the docs
#     import matplotlib.pyplot as plt
#     sample = np.random.uniform(0, 1, 50)
#     sample=[1,2,2,3,2,3,3,3,3,3,3,3,3,3,10]
#     ecdf = sm.distributions.ECDF(sample)
#     x = np.linspace(min(sample), max(sample))
#     y = ecdf(x)
#     plt.step(x, y)
#     plt.show()
    
    #lines=open(r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\test\1eu1test.txt','r+').readlines()
    #path=r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\confplot\friday\sm\1'
    path=r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\round20(newimp-507590-with-20percent)'
    #path=r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\round16(diffpercentile)\zsma5030'
    open(path+'\max.csv', 'w').close()
    

    fileordir='d'  #scatter plot or boxplot based on 'f' means file, 'd' means directory
    for root, dirs, files in os.walk(path):
        print "root",root
        #maxacclist=[]
        #print "dirs", dirs
        #print "files", files
    
        for file in os.listdir(root):
            current_file_path = os.path.join(root, file)
            if current_file_path.endswith('.txt'):
                '''remove the file less than 35K'''
                if os.stat(current_file_path).st_size<20000:
                    os.remove(current_file_path)
                    continue
                if current_file_path.split('.')[-1]=="txt" and os.stat(current_file_path).st_size>15000:
                    jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,std99latency,host,jmhostname,latdecider=process(current_file_path)
                    '''get the throughput loss percentage vs increase in Throughput'''
                    lossper=list(abs((numpy.array(opscnt)/numpy.array(expcnt))*100-100))
                    for indx,i in enumerate(expcnt):
                        i=int(i/500)*500
                        if i not in throghputlosslist.keys():
                            throghputlosslist[i]=[]
                        throghputlosslist[i].append(int(lossper[indx]))
                    print throghputlosslist
                    '''get the latency in the increase of the throughput'''
                    #print 'per90:',per90
                    for indx,i in enumerate(expcnt):
                        i=int(i/500)*500
                        if i not in latencylist90.keys():
                            latencylist90[i]=[]
                        if i not in latencylist75.keys():
                            latencylist75[i]=[]
                        if i not in latencylist50.keys():
                            latencylist50[i]=[]
                        latencylist50[i].append(int(per50[indx]-float(ping)))
                        latencylist75[i].append(int(per75[indx]-float(ping)))
                        latencylist90[i].append(int(per90[indx]-float(ping)))
                    #print min(latencylist)
                    '''check and remove the files with errors'''
                    if error>20 or maxAcc=='0':
                        os.remove(current_file_path)
                        continue

                    #if fileordir=='f':
                    maxacclist.append([current_file_path.split('\\')[-1],maxAcc])
#                        throghputlosslist.append([current_file_path.split('\\')[-1],throghputlosslist])
                    #else:
                    #    maxacclist.append([root.split('\\')[-1],maxAcc])
                    #    throghputlosslist.append([root.split('\\')[-1],lossthr])
                   
                    #no use##plot50th(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path)
                    #plotSeprate(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path,jmhostname,latdecider)
                    #plotSepratePaper(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path,jmhostname)
                    #plottrflatencypaper(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path,jmhostname)
                    #plotboxplotThrVsLatRatioLatvalue(jmrecs,expcnt,hitcnt,opscnt,per25,per50,per75,per90,per99, maxAcc,ping,error,std50latency,std75latency,std90latency,host,current_file_path,jmhostname)
                    #print maxacclist 
                    print current_file_path,': ',maxAcc
                    tmp+=(current_file_path.split('\\')[-1])  #the number
            #                 tmp+=(',')
            #                 tmp+=(current_file_path.split('\\')[-1].split('-')[1])     #the host
            #                 tmp+=(',')
            #                 tmp+=(current_file_path.split('\\')[-1].split('-')[3])     #the country
                    if std50latency=='nan':
                        std50latency='0'
                    tmp+=(','+maxAcc+','+ping+','+std50latency+','+std75latency+','+std90latency+','+std99latency+'\n')
                    #print maxAccArray
                    fi=open(path+'\max1.csv','a')
                    
                    fi.write(tmp)
                    fi.close()
                    print tmp
                    tmp=''
    if len(maxacclist)>0:        
        #boxpltall(maxacclist,path)
        #timeserieplot(maxacclist)  #shows the timeseries of tthe experiments 
        scatterorboxplotPercLat(maxacclist,'b')    #shows the scatter plot of
        #cdfplot(maxacclist)
        #boxplotcdfThroughputLoss(throghputlosslist,'b')
        #boxplotcdflatency(latencylist50,latencylist75,latencylist90,'b','all') 
        #print maxacclist
        print throghputlosslist
