from random import *
import numpy as numpy_library
import itertools as itertools
import copy
import time
import random

DIMENSION = 3
WAIT = 5
userFirst = 1
computerFirst = 2
MIN = "1"
MAX = "2"
# standard function constants based on conjecture
# and limited gameplay experience
CONSTS = {'c1': 21.0, 'c2':5.0, 'c3': 4.0,
                      'c4': 3.0, 'c5': 3.0, 'c6': 2.5,}

messageComputersTurn     = "Computer's turn."
messageChoosePlayer      = "Which player goes first? (1 = you, 2 = computer, 0 = stop) "
messageGoodbye           = "Goodbye. Thanks for playing JackToe!."
messageTryAgain          = "That is invalid. Please try again."
messageUsersTurn         = "User's turn."
messageWelcome           = "Welcome to JackToe!"
messageYouWin            = "User wins."
messageCompWin           = "Computer Wins"


'''
returns true we have [DIMENSION] in a row
'''
def hasRow(listDict):
    cells = map((lambda x: x['cell']), listDict)
    listAnd = reduce( (lambda x,y: x & y), cells) #should be NON zero if 1's matching exists
    return bool(listAnd)

'''
returns true if a board (DIMENSION X DIMENSION) has been won
'''
def isWin(board):
    for row in board:
        if hasRow(row):
            return True
    board_Transpose = zip(*board)
    for column in board_Transpose:
        if hasRow(column):
            return True
    zip(*board)
    length = len(board)
    diagonal1 = [board[i][i] for i in range(length)] #returns y=-x diagonal (the trace)
    diagonal2 = [board[i][length-i-1] for i in range(length)] #returns y=x diagonal
    if (hasRow(diagonal1) or hasRow(diagonal2)):
        return True
    return False

''' the utility function! '''
def utility(state):
    func1 = f1_score(state)
    func2 = f2_center(state)
    func3 = f3_side(state)
    func4 = f4_corner(state)
    func5 = f5_blocking(state)
    func6 = f6_potential(state)
    #print "func1 is: ", func1
    return CONSTS['c1']*func1 + CONSTS['c6']*func6

'''
Calculated by subtracting score of current player
from score of opponent.
'''
def f1_score(state):
    score_min = state.score[MIN]
    score_max = state.score[MAX]
    # It may seem confusing to do score_min - score_max ...
    # This is a result of utility being called
    # before board is modified so really utility is
    # called for previous player.
    return  score_min - score_max

'''
Returns all the boards that have not been won yet.
'''
def getActive(state):
    active_boards = []
    for line_boards in state.boards:
        for board in line_boards:
            if not isWin(board):
                # copy because i think i might be modifying memory:
                active_boards += [board]
    assert active_boards != []
    return active_boards

'''
Relative number of ACTIVE center
pieces
'''
def f2_center(state):
    center = {MIN: 0, MAX: 0,}
    activeBoards = getActive(state)
    for board in activeBoards:
        if board[1][1]['cell'] == int(MIN):
            center[MIN] += 1
        elif board[1][1]['cell'] == int(MAX):
            center[MAX] += 1
    return center[MIN] - center[MAX]

'''
Relative number of ACTIVE side
pieces
'''
def f3_side(state):
    sideCount = {MIN: 0, MAX: 0,}
    activeBoards = getActive(state)
    for board in activeBoards:
        sides = [board[1][0], board[0][1], board[1][2], board[2][1]]
        for side in sides:
            if side['cell'] == int(MIN):
                sideCount[MIN] += 1
            elif side['cell'] == int(MAX):
                sideCount[MAX] += 1
    return sideCount[MIN] - sideCount[MAX]

'''
Relative number of ACTIVE corner
pieces
'''
def f4_corner(state):
    cornerCount = {MIN: 0, MAX: 0,}
    activeBoards = getActive(state)
    for board in activeBoards:
        corners = [board[0][0], board[0][2], board[2][0], board[2][2]]
        for corner in corners:
            if corner['cell'] == int(MIN):
                cornerCount[MIN] += 1
            elif corner['cell'] == int(MAX):
                cornerCount[MAX] += 1
    return cornerCount[MIN] - cornerCount[MAX]

'''
returns true if 2 is blocked by 1 in a row
'''
def hasBlock(listDict):
    cells = map((lambda x: x['cell']), listDict)
    cells = sorted(cells)
    if cells == [1, 2, 2]:
        return "1" # Good for player 1
    elif cells == [1, 1, 2]:
        return "2"
    else:
        return None

'''
returns true we have [DIMENSION] in a row
'''
def hasPotential(listDict):
    cells = map((lambda x: x['cell']), listDict)
    cells = sorted(cells)
    if cells == [0, 2, 2]:
        return "2"  # Good for player 2
    if cells == [0, 1, 1]:
        return "1"
    else:
        return None

'''
gets the transpose of each board in a list of boards
'''
def transposeBoards(lBoards):
    newList = []
    for board in lBoards:
        newBoard = []
        for i in range(DIMENSION):
            newBoard += [[board[j][i] for j in range(DIMENSION)]]
        newList += [newBoard]
    return newList

'''
Counts the relative number of blocking positions.
'''
def f5_blocking(inputState):
    # why this line?
    # b/c i modify state
    state = State()
    state.copyThis(inputState)
    blocking = {'1': 0, '2': 0, }
    activeBoards = getActive(state)
    activeBoardsTranspose = transposeBoards(activeBoards)
    for board in activeBoards:
        for row in board:
            getblock = hasBlock(row)
            if getblock == MAX:
                blocking[MAX] += 1
            elif getblock == MIN:
                blocking[MIN] += 1
    for board in activeBoardsTranspose:
        #returns y=-x diagonal (the trace):
        diagonal1 = [board[i][i] for i in range(DIMENSION)]
        #returns y=x diagonal:
        diagonal2 = [board[i][DIMENSION-i-1] for i in range(DIMENSION)]
        # convert type to list so we can add diags...
        board = list(board)
        board += [diagonal1, diagonal2]
        for row in board:
            getBlock = hasBlock(row)
            if getBlock == MAX:
                blocking[MAX] += 1
            elif getBlock == MIN:
                blocking[MIN] += 1
    return blocking[MIN] - blocking[MAX]

'''
Counts the relative number of potential positions.
'''
def f6_potential(inputState):
    # why this line?
    # b/c i modify state
    state = State()
    state.copyThis(inputState)
    potential = {'1': 0, '2': 0, }
    activeBoards = getActive(state)
    activeBoardsTranspose = transposeBoards(activeBoards)
    for board in activeBoards:
        for row in board:
            getpot = hasPotential(row)
            if getpot == MAX:
                potential[MAX] += 1
            elif getpot == MIN:
                potential[MIN] += 1
    for board in activeBoardsTranspose:
        #returns y=-x diagonal (the trace):
        diagonal1 = [board[i][i] for i in range(DIMENSION)]
        #returns y=x diagonal:
        diagonal2 = [board[i][DIMENSION-i-1] for i in range(DIMENSION)]
        # convert type to list so we can add diags...
        board = list(board)
        board += [diagonal1, diagonal2]
        for row in board:
            getPot = hasPotential(row)
            if getPot == MAX:
                potential[MAX] += 1
            elif getPot == MIN:
                potential[MIN] += 1
    return potential[MIN] - potential[MAX]

'''
alpha-beta helper
'''
def minH(state, depth, maxDepth, a, b):

    value = 9001.0
    s = State()
    gen = state.genChildren(s)
    nextS = gen.next()

    if (depth == maxDepth) or (nextS == None):
        state.printInfo()
        return utility(state)
    iterations = 0
    while nextS != None:
        value = min(value, maxH(nextS, depth+1, maxDepth, a, b))
        print "error here: ", type(value), type(a)
        assert type(value) == type(a)
        if value <= a:
            return -9001.0 # we don't want to choose this!
        b = min(b, value)
        nextS = gen.next()
    return value

'''
called by ab
The minmax alpha-beta prunning algorithm as described by Norvig p. 170
'''
def maxH(state, depth, maxDepth, a, b):

    value = -9001.0
    s = State()
    gen = state.genChildren(s)
    nextS = gen.next()

    if (depth == maxDepth):
        utilityRecieved = utility(state)
        print "utility for below: ", utilityRecieved
        state.printInfo()
        print
        return utility(state)

    if depth == 0:
        iteration = 0
        min_h = minH(nextS, depth+1, maxDepth, a, b)
        value = (min_h, nextS)
        while nextS != None:
            iteration += 1
            min_h = minH(nextS, depth+1, maxDepth, a, b)
            assert type(value) == type((min_h, nextS))
            value = max( value, (min_h, nextS) )
            if value >= (b, 'make comparisons work'):
                return (9001.0, value[1]) # we don't want to select this
            a = max(a, value[0])
            nextS = gen.next()
        return value
    else:
        while nextS != None:
            value = max(value, minH(nextS, depth+1, maxDepth, a, b))
            assert type(value) == type(b)
            if value >= b:
                return 9001.0 # don't want to select this (another option is implied)
            a = max(a, value)
            nextS = gen.next()
        return value

'''
Could the current player force a win?
return move if yes; None if not
'''
def getWin(state):
    a = State()
    cG = state.genChildren(a)
    nextS = cG.next()
    while nextS != None:
        if isWin(nextS):
            return nextS
        nextS = cG.next()
    return None

'''
Checks if a win exists
Then calls helper
'''
def ab(state):
    '''
    possibleWin = getWin(state)
    if possibleWin:
        print "Computer Won"
        return possibleWin
    '''
    start = time.clock()
    farthestDepth = 1
    duration = 0
    while (duration < WAIT and farthestDepth < 4):
        nextState = maxH(state, 0, farthestDepth, -9005.0, 9005.0)
        '''
        print "\n*"
        print state.printInfo()
        print "\n*"
        '''
        duration = time.clock() - start
        farthestDepth += 1
    return nextState

def turn(integer):
    if(integer == 1): return 2
    else: return 1

class State:
# state represents the board, next piece to be played, and other relevant info
    def __init__(self):
        """ Construct a new board. """
        self.boards = [[[[ {"cell": 0, "x": x, "y": y, "x_board": x_board, "y_board": y_board}
                           for x in range(DIMENSION)] for y in range(DIMENSION)]
                           for x_board in range(DIMENSION)] for y_board in range(DIMENSION)]
        self.nextPiece = [1,1,1] # next board to be played in {(-1, -1, ?) for any board}
        self.score = {"1": 0, "2": 0}

        ''' describe location of piece placements so far '''
        self.numCenter = {"1": 0, "2": 0}
        self.numSide = {"1": 0, "2": 0}
        self.numCorner = {"1": 0, "2": 0}

    def isWinExampleBoard(self, board):
        length = len(board)
        for a in range(length):
            for b in range(length):
                self.boards[0][0][a][b]['cell'] = board[a][b]
        return isWin (self.boards[0][0])

    '''
    Determine if coordinate entered is on an empty square
    '''
    def isUnoccupied(self, y, x):
        return self.boards[self.nextPiece[0]][self.nextPiece[1]][y][x]['cell'] == 0


    def printer(self):
        length = DIMENSION**2*4 + 1
        buf = ['-' for x in range(length)]
        buf = ''.join(buf)
        printRows = ['|' for col in range(DIMENSION*DIMENSION)]
        for (rowBoards, i) in zip(self.boards, range(DIMENSION)):
            for board in rowBoards:
                for (row, j) in zip(board, range(DIMENSION)):
                    printRows[(i*DIMENSION)+j] = printRows[(i*DIMENSION)+j] + ' ' + str([x['cell'] for x in row]) + ' |'
        for (i, row) in zip(range(DIMENSION**2), printRows):
            if ( i % DIMENSION == 0 ):
                print buf
            print row
        print buf

    def printerComplicated(self):
        length = DIMENSION**2*8 + 3
        buf = ['-' for x in range(length)]
        buf = ''.join(buf)
        printRows = ['|' for col in range(DIMENSION*DIMENSION)]
        for (rowBoards, i) in zip(self.boards, range(DIMENSION)):
            for board in rowBoards:
                for (row, j) in zip(board, range(DIMENSION)):
                    printRows[(i*DIMENSION)+j] = printRows[(i*DIMENSION)+j] + ' ' + str(row) + ' |'
        for (i, row) in zip(range(DIMENSION**2), printRows):
            if ( i % DIMENSION == 0 ):
                print buf
            print row
        print buf


    def printInfo(self):
        print "boards are:\n", self.printer(), "nextPiece is", self.nextPiece, "\nScore is:", self.score#, "Complicated info:\n", self.printerComplicated()


    def copyBoards(self, otherState):
        rangeBoards = range(len(otherState.boards))
        for y_board in rangeBoards:
            for x_board in rangeBoards:
                for y in rangeBoards:
                    for x in rangeBoards:
                        self.boards[y_board][x_board][y][x] = copy.copy(
                              otherState.boards[y_board][x_board][y][x])

    def copyThis(self, other):
        self.copyBoards(other)
        self.nextPiece = copy.copy(other.nextPiece)
        self.score = copy.copy(other.score)
        self.numCenter = copy.copy(other.numCenter)
        self.numSide = copy.copy(other.numSide)
        self.numCorner = copy.copy(other.numCorner)

    def updatePieceLocs(self, c1, c2):
        currentPlayer = str(self.nextPiece[2])
        if (c1 == 1 and c2 == 1):
            self.numCenter[currentPlayer] += 1
        elif (c1 == 1 or c2 == 1):
            self.numSide[currentPlayer] += 1
        else:
            self.numCorner[currentPlayer] += 1

    def genChildren(self, child): #list of states
        aL = range(DIMENSION)
        bL = range(DIMENSION)
        cL = range(DIMENSION)
        dL = range(DIMENSION)
        random.shuffle(aL)
        random.shuffle(bL)
        random.shuffle(cL)
        random.shuffle(dL)
        #print "isWin?", isWin(self.boards[self.nextPiece[0]][self.nextPiece[1]])
        if isWin(self.boards[self.nextPiece[0]][self.nextPiece[1]]):
            #print "One"
            for a in aL:
                for b in bL:
                    if(not isWin(self.boards[a][b])):
                        for c in cL:
                            for d in dL:
                                if(self.boards[a][b][c][d]['cell'] == 0):
                                    child.copyThis(self)
                                    nP = turn(self.nextPiece[2])
                                    child.nextPiece = (c,d,nP)
                                    child.boards[a][b][c][d]['cell'] = self.nextPiece[2]
                                    if isWin(child.boards[a][b]):
                                        child.score[str(self.nextPiece[2])] += 1
                                    child.updatePieceLocs(c, d)
                                    child.printer
                                    yield child
        else:
            #print "Two"
            a = self.nextPiece[0]
            b = self.nextPiece[1]
            for c in cL:
                for d in dL:
                    if(self.boards[a][b][c][d]['cell'] == 0):
                        child.copyThis(self)
                        nP = turn(self.nextPiece[2])
                        child.nextPiece = (c,d,nP)
                        child.boards[a][b][c][d]['cell'] = self.nextPiece[2]
                        if isWin(child.boards[a][b]):
                            child.score[str(self.nextPiece[2])] += 1
                        child.updatePieceLocs(c, d)
                        yield child
        yield None

def main():
    """ Run the Trio! playing program. """
    print messageWelcome
    playUntilExit()

def playUntilExit():
    """ Play successive games until the user decides to stop. """
    while True:
        firstPlayer = getFirstPlayer()
        if firstPlayer == 0:
            print messageGoodbye
            return
        playTrio(firstPlayer)

def getFirstPlayer():
    """ Get the first player, or an indication to stop. """
    while True:
        dim = raw_input("Enter the dimension of the game \n")
        if dim.isdigit():
            global DIMENSION
            DIMENSION = int(dim)
            break
        else:
            print messageTryAgain
    while True:
        response = raw_input(messageChoosePlayer)
        if response == "1":
            return 1
        elif response == "2":
            return 2
        elif response == "0":
            return 0
        else:
            print messageTryAgain

'''
Play the game, given first player, or stop.
'''
def playTrio(firstPlayer):
    print "Should only happen once"
    state = State()
    if firstPlayer == userFirst:

        while True:
            if userTurn(state) == 0:
                break
            if computerTurn(state) == 0:
                break

    elif firstPlayer == computerFirst:

        while True:
            if computerTurn(state) == 0:
                break
            if userTurn(state) == 0:
                break

    else:
        assert "Should never happen"

'''
Simulate one round of play with the user starting.
'''
def userTurn(state):
    print messageUsersTurn
    print state.printInfo()

    print "You are playing piece", state.nextPiece[2]
    while True:
        if isWin(state.boards[state.nextPiece[0]][state.nextPiece[1]]):
            print "You must select a board to play into"
            x_board = raw_input("Assign column of board to play into")
            y_board = raw_input("Assign row of board to play into")
            if x_board.isdigit() and y_board.isdigit() and (not isWin(state.boards[int(y_board)][int(x_board)])):
                x_board = int(x_board)
                y_board = int(y_board)
                x = raw_input("Assign column of next piece")
                y = raw_input("Assign row of next piece")
                if x.isdigit() and y.isdigit() and state.isUnoccupied(int(y), int(x)):
                    x = int(x)
                    y = int(y)
                    state.boards[y_board][x_board][y][x]['cell'] = state.nextPiece[2]
                    if isWin(state.boards[y_board][x_board]):
                        state.score[str(state.nextPiece[2])] += 1
                    state.nextPiece = (y, x, turn(state.nextPiece[2]))
                    break
            else:
                print messageTryAgain
        else:
            x = raw_input("Assign column of next piece")
            y = raw_input("Assign row of next piece")

            if x.isdigit() and y.isdigit() and state.isUnoccupied(int(y), int(x)):
                x = int(x)
                y = int(y)
                state.boards[state.nextPiece[0]][state.nextPiece[1]][y][x]['cell'] = state.nextPiece[2]
                if isWin(state.boards[state.nextPiece[0]][state.nextPiece[1]]):
                    state.score[str(state.nextPiece[2])] += 1
                state.nextPiece = (y, x, turn(state.nextPiece[2]))
                break
            else:
                print messageTryAgain
    print "Your move was:"
    state.printInfo()

    print "Scores: Player 1: ", state.score['1'], " Player 2: ", state.score['2']

    computerTurn(state)


'''
Simulate the computer's turn.
'''
def computerTurn(state):
    print messageComputersTurn
    print state.printInfo()
    (expectedUtility, nextState) = ab(state)
    print "Expected utility is: ", expectedUtility
    nextState.printInfo()
    state = copy.deepcopy(nextState)

    print "Scores: Player 1: ", state.score['1'], " Player 2: ", state.score['2']

    userTurn(state)

print "To start the game enter \"main()\"."

'''
Test for f1_score
'''
def test1():
    a = State()
    a.boards[0][0][0][0]['cell'] = 1
    a.boards[0][0][1][1]['cell'] = 1
    a.nextPiece[0] = 0
    a.nextPiece[1] = 0
    a.nextPiece[2] = 1
    a.printInfo()
    b = ab(a)[1]
    b.printInfo()

'''
Test for f2_center
'''
def test2():
    a = State()
    a.nextPiece[0] = 1
    a.nextPiece[1] = 1
    a.printInfo()
    b = ab(a)[1]
    b.printInfo()

'''
Test for f1_score
'''
def test3():
    a = State()
    a.boards[0][0][1][0]['cell'] = 1
    a.boards[0][0][0][0]['cell'] = 2
    #a.boards[0][0][1][1]['cell'] = 1
    a.nextPiece[0] = 0
    a.nextPiece[1] = 0
    a.nextPiece[2] = 2
    a.printInfo()

    b = ab(a)[1]
    b.printInfo()

def getState():
    a = State()
    a.boards[0][0][0][0]['cell'] = 1
    a.boards[0][0][1][1]['cell'] = 1
    a.nextPiece = [0,0,1]
    return a
