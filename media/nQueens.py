import copy

def queensAux(dim, solved, last, it):  #use it or lose it approach

	useIt = copy.deepcopy(solved)
	useIt[last[0]] [last[1]] = useIt[last[0]] [last[1]] + 1

	if queen(useIt) and dim == it + 1:
		print "Solution below:"
		printer (useIt)
		return 1

	next = nextify(dim, last)
	if next[0] == -1:
		return 0

	if queen(useIt): #useIt and loseIt
		return queensAux(dim, solved, next, it) + queensAux(dim, useIt, next, it + 1)
	else: # only loseIt (prunning)
		return queensAux(dim, solved, next, it)

def nextify (dim, last):
	if (last[0]+1 == dim and last[1]+1 == dim):
		return (-1,-1)
	if (last[1]+1 < dim):
		return (last[0], last[1] + 1)
	if (last[1]+1 == dim):
		return (last[0] + 1, 0)

def printer(listL):
	for x in listL:
		print x

def makeBoard(dim):
	a = []
	for y in range (dim):
		row = range(dim)
		for x in row:
			row[x] = 0
		a = a + [row]
	return a

def XQueens(dim):
	if(dim > 0):
		a = queensAux(dim, makeBoard(dim), (0,0), 0)
		print "Number of distinct solutions:"
		print a
	else:
		print "Enter a positive number."

def rookR(listL):
	for x in listL:
		if sum(x) > 1:
			return False
	return True

def rookC(listL):
	sum = 0
	index = 0
	for x in listL:
		for x in listL:
			sum = sum + x[index]
			if sum > 1:
				return False
		index = index + 1
		sum = 0
	return True

def bishop (listL):
	for x in range(len(listL)):
		other1 = 0
		other2 = 0
		other3 = len(listL) - 1
		other4 = len(listL) - 1 - x
		sum1 = 0
		sum2 = 0
		sum3 = 0
		sum4 = 0
		for y in range(x,len(listL)):
			sum1 = sum1 + listL[y][other1]
			sum2 = sum2 + listL[other2][y]
			sum3 = sum3 + listL[other3][y]
			other1 = other1 + 1
			other2 = other2 + 1
			other3 = other3 - 1
		for y in range(0,len(listL)-x):
			sum4 = sum4 + listL[y][other4]
			other4 = other4 - 1
		if ( sum1 > 1 or sum2 > 1 or sum3 > 1 or sum4 > 1 ): 
			return False
	return True


def queen(listL):
	return rookC(listL) and rookR(listL) and bishop(listL)

