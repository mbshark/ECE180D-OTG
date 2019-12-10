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



def findU(chart):
	sz=chart.shape
	x=sz[1]
	y=sz[0]

	if x<3 or y<2:
		return

	for a in range(0,x-2):
		for b in range(a+2,x):
			for c in range(1,y):
				test=numpy.zeros([c+1,b-a+1])
				test[0:c,0]=chart[0:c,a]
				test[c,0:b-a+1]=chart[c,a:b+1]
				test[0:c,b-a]=chart[0:c,b]

				for d in range(0,c):
					print(test[d:c+1,:])
					print("***************")

def findC(chart):

	sz=chart.shape
	x=sz[1]
	y=sz[0]

	if x<2 or y<3:
		return

	for a in range(0,y-2):
		for b in range(a+2,y):
			for c in range(0,x-1):
				test=numpy.zeros([b-a+1,x-c])
				test[0,0:x-c]=chart[a,c:x]
				test[0:b-a,0]=chart[a:b,c]
				test[b-a,0:x-c]=chart[b,c:x]

				for d in range(2,x-c):
					print(test[:,0:d])



def findL(charts):
	for n in range(0,len(charts)):
		chart=charts[n]
		sz=chart.shape
		x=sz[1]
		y=sz[0]

		mscore=0

		if x<2 or y<3:
			print()
		else:
			for a in range(1,y):
				for b in range(0,x-1):
					test=numpy.zeros([a+1,x-b])
					test[0:a,0:1]=chart[0:a,b:b+1]
					test[a,0:x-b]=chart[a,b:x]
					for c in range(2,x-b+1):
						for d in range(0,a):
							print(test[d:a+1,0:c])
							print("***************")
							print(valL(test[d:a+1,0:c]))
							print("----------")
							if valL(test[d:a+1,0:c])>mscore:
								mscore=valL(test[d:a+1,0:c])
								best=test[d:a+1,0:c]
	print(best)

def findA():

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

def valU():
	sz=chart.shape
	x=sz[1]
	y=sz[0]





def valC():
	sz=chart.shape
	x=sz[1]
	y=sz[0]

def valL(chart):
	sz=chart.shape
	x=sz[1]
	y=sz[0]

	pen=min(1.6*x/y,y/(1.6*x))

	val=sum(sum(chart>0))**3/(x+y-1)

	return val*pen

def valA():
	sz=chart.shape
	x=sz[1]
	y=sz[0]


"""
s1=chartGen(4,4,0.8)
s2=chartGen(3,3,1)
s=[]
s.append(s1)
s.append(s2)
print(s1)
print("-----------")
print(s2)
print("--------------")

findL(s)
"""
def main():
	s=chartGen(10,20,1)
	print(s)
	print("--------------")

	findL(s)

if __name__ == "__main__":
	main()
