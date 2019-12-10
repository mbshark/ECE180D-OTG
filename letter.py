import numpy
import random

def chartGen(x,y,p):
	seats=numpy.zeros([x,y])
	count=1
	for a in range(0,x):
		for b in range(0,y):
			if random.random()<p:
				seats[a,b]=count
				count=count+1

	return seats



def findU(charts):
	best=[]
	mscore=0
	for n in range(0,len(charts)):
		chart=charts[n]
		sz=chart.shape
		x=sz[1]
		y=sz[0]

		if x>2 and y>1:
			for a in range(0,x-2):
				for b in range(a+2,x):
					for c in range(1,y):
						test=numpy.zeros([c+1,b-a+1])
						test[0:c,0:1]=chart[0:c,a:a+1]
						test[c,0:b-a+1]=chart[c:c+1,a:b+1]
						test[0:c,b-a:b-a+1]=chart[0:c,b:b+1]
						for d in range(0,c):
							if valU(test[d:c+1,:])>mscore or len(best)==0:
								mscore=valL(test[d:c+1,:])
								best=test[d:c+1,:]

	print(best)

def findC(charts):
	best=[]
	mscore=0
	for n in range(0,len(charts)):
		chart=charts[n]
		sz=chart.shape
		x=sz[1]
		y=sz[0]

		if x>1 and y>2:
			for a in range(0,y-2):
				for b in range(a+2,y):
					for c in range(0,x-1):
						test=numpy.zeros([b-a+1,x-c])
						test[0,0:x-c]=chart[a,c:x]
						test[0:b-a,0:1]=chart[a:b,c:c+1]
						test[b-a:b-a+1,0:x-c]=chart[b:b+1,c:x]
						for d in range(2,x-c):
							if valC(test[:,0:d])>mscore or len(best)==0:
								mscore=valL(test[:,0:d])
								best=test[:,0:d]

	print(best)



def findL(charts):
	best=[]
	mscore=0
	for n in range(0,len(charts)):
		chart=charts[n]
		sz=chart.shape
		x=sz[1]
		y=sz[0]
		
		if x>1 and y>1:
			for a in range(1,y):
				for b in range(0,x-1):
					test=numpy.zeros([a+1,x-b])
					test[0:a,0:1]=chart[0:a,b:b+1]
					test[a,0:x-b]=chart[a,b:x]
					for c in range(2,x-b+1):
						for d in range(0,a):
							if valL(test[d:a+1,0:c])>mscore or len(best)==0:
								mscore=valL(test[d:a+1,0:c])
								best=test[d:a+1,0:c]
	
	
	print(best)

def findA():
	best=[]
	mscore=0
	for n in range(0,len(charts)):
		chart=charts[n]
		sz=chart.shape
		x=sz[1]
		y=sz[0]

		if x<3 or y<4:
			return

		for a in range():
			for b in range():
				for c in range():
					for d in range():
						print()

def valU(chart):
	sz=chart.shape
	x=sz[1]
	y=sz[0]

	pen=min(x/y,y/(x))

	val=sum(sum(chart>0))**3/(y*2+x-2)**2

	return val*pen
	



def valC(chart):
	sz=chart.shape
	x=sz[1]
	y=sz[0]

	pen=min(x/y,y/(x))

	val=sum(sum(chart>0))**3/(y+2*x-2)**2

	return val*pen

def valL(chart):
	sz=chart.shape
	x=sz[1]
	y=sz[0]

	pen=min(1.6*x/y,y/(1.6*x))

	val=sum(sum(chart>0))**3/(x+y-1)**2

	return val*pen

def valA():
	sz=chart.shape
	x=sz[1]
	y=sz[0]

	val=0

	pen=0

	return val*pen


"""
s1=chartGen(3,4,0.8)
s2=chartGen(4,3,1)
s=[]
s.append(s1)
s.append(s1)
s.append(s2)
#print(s1)
#print("-----------")
#print(s2)
#print("--------------")
findU(s)
findC(s)
findL(s)
"""
"""
L=numpy.array([[1,0,0],[1,0,0],[0,0,0],[1,1,1]])
print(L)
print(valL(L))
"""



