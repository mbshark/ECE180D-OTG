import numpy

sample=numpy.matrix([[1,2],[3,4]])


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
	error=False
	sz=len(entries)
	map = numpy.zeros(sz)

	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)
		map[a]=entries[a].pi

	print(map)
	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)

		if entries[a].fr > 0:
			I=numpy.where(map==entries[a].fr)
			if len(I)>1:
				error=True

			if not((entries[a].fr==entries[int(I[0][0])].pi)&(entries[a].pi==entries[int(I[0][0])].bk)):
				error=True

		if entries[a].rt > 0:
			I=numpy.where(map==entries[a].rt)
			if len(I)>1:
				error=True

			if not((entries[a].rt==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].lf)):
				error=True


		if entries[a].bk>0:
			I=numpy.where(map==entries[a].bk)
			if len(I)>1:
				error=True
				
			if not((entries[a].bk==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].fr)):
				error=True
				
		if entries[a].lf>0:
			I=numpy.where(map==entries[a].lf)
			if len(I)>1:
				error=True
				
			if not((entries[a].lf==entries[int(I[0])].pi)&(entries[a].pi==entries[int(I[0])].rt)):
				error=True
				

	return not(error)


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


			print(explored)
			print(chart)
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
			print("pad top")
			curr[0]=1

		if chart[curr[0]-1,curr[1]]==0:
			chart[curr[0]-1,curr[1]]=entries[ind].fr
			chart=addNeighbors(chart,findInd(entries[ind].fr,entries),entries)


	if entries[ind].rt>0:
		if curr[1]==sz[1]-1:
			chart=numpy.concatenate((chart,numpy.zeros([sz[0],1])),axis=1)
			print("pad right")

		if chart[curr[0],curr[1]+1]==0:
			chart[curr[0],curr[1]+1]=entries[ind].rt
			chart=addNeighbors(chart,findInd(entries[ind].rt,entries),entries)

	if entries[ind].bk>0:
		if curr[0]==sz[0]-1:
			chart=numpy.concatenate((chart,numpy.zeros([1,sz[1]])),axis=0)
			print("pad bottom")

		if chart[curr[0]+1,curr[1]]==0:
			chart[curr[0]+1,curr[1]]=entries[ind].bk
			chart=addNeighbors(chart,findInd(entries[ind].bk,entries),entries)

	if entries[ind].lf>0:
		if curr[1]==0:
			chart=numpy.concatenate((numpy.zeros([sz[0],1]),chart),axis=1)
			print("pad left")
			curr[1]=1

		if chart[curr[0],curr[1]-1]==0:
			chart[curr[0],curr[1]-1]=entries[ind].lf
			chart=addNeighbors(chart,findInd(entries[ind].lf,entries),entries)

	return chart
	

def findInd(pi,entries):
	sz=len(entries)
	for a in numpy.linspace(0,sz-1,sz):
		a=int(a)
		if entries[a].pi==pi:
			return a

	return -1



n=retNeighbors(sample)

for a in numpy.linspace(0,len(n)-1,len(n)):
	a=int(a)
	print(n[a].pi)
	print(n[a].fr)
	print(n[a].rt)
	print(n[a].bk)
	print(n[a].lf)
	print("-------")


chart=makeChart(n)
print(chart)



