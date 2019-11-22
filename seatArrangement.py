import numpy
import random
from quickstart import getFormResponses



def seatGen(x,y,p):
	seats=numpy.zeros([x,y])
	count=1
	for a in numpy.linspace(0,x-1,x):
		a=int(a)
		for b in numpy.linspace(0,y-1,y):
			b=int(b)
			if random.random()<p:
				seats[a,b]=count
				count=count+1

	return seats


class entry:
	def __init__(self,pi,fr,rt,bk,lf):
		self.pi=pi
		self.fr=fr
		self.rt=rt
		self.bk=bk
		self.lf=lf

def retNeighbors(seats):
	neighbors=[]
	sz=seats.shape
	for a in numpy.linspace(0, sz[0]-1,sz[0]):
		a=int(a)
		for b in numpy.linspace(0,sz[1]-1,sz[1]):
			b=int(b)
			pi=seats[a,b]
			if pi>0:
				if a>0:
					fr=seats[a-1,b]
				else:
					fr=0
				if a<sz[0]-1:
					bk=seats[a+1,b]
				else:
					bk=0
				if b>0:
					lf=seats[a,b-1]
				else:
					lf=0
				if b<sz[1]-1:
					rt=seats[a,b+1]
				else:
					rt=0;

				neighbors.append(entry(pi,fr,rt,bk,lf))

	return neighbors			

def verify(entries):
	sz=len(entries)
	map = numpy.zeros(sz)

	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)
		map[a]=entries[a].pi

	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)

		if entries[a].fr > 0:
			I=numpy.where(map==entries[a].fr)

			if I[0].size!=1:
				return False

			if not((entries[a].fr==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].bk)):
				return False

		if entries[a].rt > 0:
			I=numpy.where(map==entries[a].rt)
			if I[0].size!=1:
				return False

			if not((entries[a].rt==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].lf)):
				return False


		if entries[a].bk>0:
			I=numpy.where(map==entries[a].bk)
			if I[0].size!=1:
				return False
				
			if not((entries[a].bk==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].fr)):
				return False
				
		if entries[a].lf>0:
			I=numpy.where(map==entries[a].lf)
			if I[0].size!=1:
				return False
				
			if not((entries[a].lf==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].rt)):
				return False
				

	return True

def makeChart(entries):
	if not(verify(entries)):
		return []

	seats=[]
	sz=len(entries)
	explored=numpy.zeros([sz,1])
	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)
		if explored[a]==0:
			chart=addNeighbors(numpy.matrix([]),a,entries)
			seats.append(chart)
			shape=chart.shape
			for b in numpy.linspace(0,shape[0]-1,shape[0]):
				b=int(b)
				for c in numpy.linspace(0,shape[1]-1,shape[1]):
					c=int(c)
					if chart[b,c]>0:
						I=findInd(chart[b,c],entries)
						explored[I]=1

	return seats

def addNeighbors(chart,ind,entries):
	if chart.size==0:
		chart=numpy.matrix([entries[ind].pi])

	sz=chart.shape
	currTup=numpy.where(chart==entries[ind].pi)
	curr=numpy.array([currTup[0][0],currTup[1][0]])
	#print(curr)
	if entries[ind].fr>0:
		if curr[0]==0:
			chart=numpy.concatenate((numpy.zeros([1,sz[1]]),chart),axis=0)
			sz=chart.shape
			curr[0]=1

		if chart[curr[0]-1,curr[1]]==0:
			chart[curr[0]-1,curr[1]]=entries[ind].fr
			chart=addNeighbors(chart,findInd(entries[ind].fr,entries),entries)
			sz=chart.shape
			currTup=numpy.where(chart==entries[ind].pi)
			curr=numpy.array([currTup[0][0],currTup[1][0]])

	if entries[ind].rt>0:
		if curr[1]==sz[1]-1:
			chart=numpy.concatenate((chart,numpy.zeros([sz[0],1])),axis=1)
			sz=chart.shape

		if chart[curr[0],curr[1]+1]==0:
			chart[curr[0],curr[1]+1]=entries[ind].rt
			chart=addNeighbors(chart,findInd(entries[ind].rt,entries),entries)
			sz=chart.shape
			currTup=numpy.where(chart==entries[ind].pi)
			curr=numpy.array([currTup[0][0],currTup[1][0]])

	if entries[ind].bk>0:
		if curr[0]==sz[0]-1:
			chart=numpy.concatenate((chart,numpy.zeros([1,sz[1]])),axis=0)
			sz=chart.shape

		if chart[curr[0]+1,curr[1]]==0:
			chart[curr[0]+1,curr[1]]=entries[ind].bk
			chart=addNeighbors(chart,findInd(entries[ind].bk,entries),entries)
			sz=chart.shape
			currTup=numpy.where(chart==entries[ind].pi)
			curr=numpy.array([currTup[0][0],currTup[1][0]])

	if entries[ind].lf>0:
		if curr[1]==0:
			chart=numpy.concatenate((numpy.zeros([sz[0],1]),chart),axis=1)
			sz=chart.shape
			curr[1]=1

		if chart[curr[0],curr[1]-1]==0:
			chart[curr[0],curr[1]-1]=entries[ind].lf
			chart=addNeighbors(chart,findInd(entries[ind].lf,entries),entries)
			sz=chart.shape
			currTup=numpy.where(chart==entries[ind].pi)
			curr=numpy.array([currTup[0][0],currTup[1][0]])

	return chart
	
def findInd(pi,entries):
	sz=len(entries)
	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)
		if entries[a].pi==pi:
			return a

	return -1




"""
for a in numpy.linspace(0,len(n)-1,len(n)):
	a=int(a)
	print(n[a].pi)
	print(n[a].fr)
	print(n[a].rt)
	print(n[a].bk)
	print(n[a].lf)
	print("-------")
"""

"""
# Generate a seating map where each seat in a grid has a number
seats=seatGen(6,6,0.5)
#seats=numpy.matrix([[1,2],[3,0]])

# returns the neighbors of all of those seats and creates an "entry" for each pi
inputs=retNeighbors(seats)

#inputs=random.shuffle(inputs)

output=makeChart(inputs)

print(seats)
print("***************")

for a in range(0,len(output)):
	print(output[a])
	print("--------------")
"""
# seats=seatGen(6,6,0.5)
# inputs=retNeighbors(seats)

neighbors=[]
values = getFormResponses()
for row in values:
    neighbors.append(entry(int(row[1]),int(row[4]),int(row[3]),int(row[5]),int(row[2])))

   
#inputs=random.shuffle(inputs)

seats=makeChart(neighbors)

print(seats)
print("***************")




