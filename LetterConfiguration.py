def detLetterConfiguration(seatingMatrix, letter):
	if (letter == 'U'):
		return findU(seatingMatrix)
	if (letter == 'C'):
		return findU(seatingMatrix)
	if (letter == 'L'):
		return findU(seatingMatrix)
	if (letter == 'A'):
		return findU(seatingMatrix)


def findU(seatingMatrix):
	return None

def findC(seatingMatrix):
	return None

def findL(seatingMatrix):
	return None

def findA(seatingMatrix):
	return None

def findVerticalLineScores(seatingMatrix):
	scores = [0] * len(seatingMatrix[0])
	for row in seatingMatrix:
		for pos in range(len(row)):
			if row[pos] == 1:
				scores[pos] = scores[pos] + 1
	return scores
		

def findHorizontalLineScores(seatingMatrix):
	scores = [0] * len(seatingMatrix)
	for row in range(len(seatingMatrix)):
		r = seatingMatrix[row]
		for pos in range(len(r)):
			if r[pos] == 1:
				scores[row] = scores[row] + 1
	return scores

def findVerticalAdjacencyScore(seatingMatrix):
	scores = []
	starts = []
	ends = []
	for p in range(len(seatingMatrix[0])):
		best = 0
		beststart = 0
		bestend = 0
		curr = 0
		currstart = 0
		for r in seatingMatrix:
			if (r[p] == 1):
				curr+=1
			else:
				if (curr > best):
					beststart = currstart
					best = curr
					bestend = p
				curr = 0
				currstart = p + 1
		if (curr > best):
			beststart = currstart
			best = curr
			bestend = len(seatingMatrix)
		scores.append(best)	
		starts.append(beststart)
		ends.append(bestend)	
	return [scores, starts, ends]

def findHorizontalAjacencyScore(seatingMatrix):
	scores = []
	for r in seatingMatrix:
		best = 0
		curr = 0			
		for p in range(len(r)):
			if (r[p] == 1):
				curr+=1
			else:
				if (curr > best):
					best = curr
				curr = 0
		if (curr > best):
			best = curr	
		scores.append(best)		
	return scores

def main():
	a = [[1, 0],[1, 1]]

	test1 = [[1,0,1], [1,1,1], [1,1,0]]
	'''
	101
	111
	110
	'''
	#print(findLetterConfiguration(seatingMatrix, "L"))
	vl1 = findVerticalLineScores(test1)
	hl1 = findHorizontalLineScores(test1)
	va1 = findVerticalAdjacencyScore(test1)
	ha1 = findHorizontalAjacencyScore(test1)
	print(vl1)
	print(hl1)
	print(va1)
	print(ha1)

if __name__ == "__main__":
	main()
