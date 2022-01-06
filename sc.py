import pickle
import os
name = input('League?')
L = os.listdir(name)
t = {}
i = 0
for l in L:
    t[l] = i
    t[i] = l
    i+=1
s = {}
s['starti'] = 0
s['startj'] = 1

while i > 0:
    i-=1
    s[i] = 0

f = open(name+'teamnum.pic','wb')
pickle.dump(t,f)
f = open(name+'status.pic','wb')
pickle.dump(s,f)