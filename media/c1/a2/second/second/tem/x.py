import sys
f=open(sys.argv[1],'r+')
g=open('fourth.txt','w+')
g.write(f.read())
f.close()
g.close()
