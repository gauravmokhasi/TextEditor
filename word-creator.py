import cPickle as pickle
d={}

name='OSWI.txt'
f= open(name ,'r')
for index in xrange(200000):
    entry = f.readline().strip()
    b=''
    flag=True
    for i in range(len(entry)):
        if(flag and entry[i]!=' '):
            b+=entry[i]
        else:
            flag=False
    if(len(b)< len(entry)):
        d[b.lower()] = entry[len(b):]
        
#print d
pickle.dump(d, open('word_store',"wb"))
    
