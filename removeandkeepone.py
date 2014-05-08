import os

allfile=[]
path=r'F:\Dropbox\Dropbox\Reading Stuff\0-MyPhD\2exp-tcpdump\6jmeter\round7\jmeteraunz'
filed={}


for filename in os.listdir(path):
    current_file_path = os.path.join(path, filename)
    if os.stat(current_file_path).st_size<35000:
        os.remove(current_file_path)
        continue
    allfile.append(filename)
    
while len(allfile)!=0:
    print len(allfile)
    filename=allfile.pop()
    base='-'.join(str(filename).split('-')[:-1])
    for filename1 in os.listdir(path):
        if str(filename1).startswith(str(base)):
            current_file_path = os.path.join(path, filename1)
            filed[current_file_path]=os.stat(current_file_path).st_size
    print filed
    if len(allfile)==0:
        break;
    for i in filed.keys():
        maxnum=max(filed, key=filed.get)
        if i!=(maxnum):
            os.remove(i)
        if str(str(i).split('\\')[-1]) in allfile:
            allfile.remove(str(str(i).split('\\')[-1]))
    #if maxnum in allfile:
     #   allfile.remove(maxnum)
    filed.clear()


