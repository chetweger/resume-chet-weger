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

messageComputersTurn     = "Computer's turn."
messageChoosePlayer      = "Which player goes first? (1 = you, 2 = computer, 0 = stop) "
messageGoodbye           = "Goodbye. Thanks for playing JackToe!."
messageTryAgain          = "That is invalid. Please try again."
messageUsersTurn         = "User's turn."
messageWelcome           = "Welcome to JackToe!"
messageYouWin            = "User wins."
messageCompWin           = "Computer Wins"

MIN = "1"
MAX = "2"

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
    if(hasRow(diagonal1) or hasRow(diagonal2)):
        return True
    return False

''' the utility function! '''
def utility(state):
    func1 = f1_score(state)
    #print "func1 is: ", func1
    return func1

'''
Calculated by subtracting score of current player
from score of opponent
'''
def f1_score(state):
    score_min = state.score[MIN]
    score_max = state.score[MAX]
    # It may seem confusing to do min-max...
    # This is a result of utility being called
    # before board is modified so really utility is
    # called for previous player.
    return  score_min - score_max

'''
Returns all the boards that have not been won yet.
'''
def getActive(state):
    active_boards = []
    for board in state.boards:
        if not isWin(board):
            active_boards += [copy.deepcopy(board)]
    assert active_boards != []
    return active_boards

'''
Relative number of ACTIVE center
pieces
'''
def f2_center(state):
    center = {'1': 0, '2': 0,}
    activeBoards = getActive(state)
    for board in activeBoards:
        if board[1][1] == 1:
            center['1'] += 1
        elif board[1][1] == 2:
            center['2'] += 2
    return center[MIN] - center[MAX]

'''
Relative number of ACTIVE side
pieces
'''
def f3_side(state):
    sideCount = {'1': 0, '2': 0,}
    activeBoards = getActive(state)
    for board in activeBoards:
        sides = [board[1][0], board[0][1], board[1][2], board[2][1]]
        for side in sides:
            if side == 1:
                sideCount['1'] += 1
            elif side == 2:
                sideCount['2'] += 2
    return side[MIN] - side[MAX]

'''
Relative number of ACTIVE corner
pieces
'''
def f4_corner(state):
    cornerCount = {'1': 0, '2': 0,}
    activeBoards = getActive(state)
    for board in activeBoards:
        corners = [board[0][0], board[0][2], board[2][0], board[2][2]]
        for corner in corners:
            if corner == 1:
                cornerCount['1'] += 1
            elif corner == 2:
                cornerCount['2'] += 2
    return corner[MIN] - corner[MAX]

'''
returns true if 2 is blocked by 1 in a row
'''
def hasBlock(listDict):
    cells = map((lambda x: x['cell']), listDict)
    cells = sorted(cells)
    if cells == [2, 2, 1]:
        return "1" # Good for player 1
    elif cells == [2, 1, 1]:
        return "2"
    else:
        return None

'''
returns true we have [DIMENSION] in a row
'''
def hasPotential(listDict):
    cells = map((lambda x: x['cell']), listDict)
    cells = sorted(cells)
    if cells == [2, 2, 0]:
        return "2"  # Good for player 2
    if cells == [1, 1, 0]:
        return "1"
    else:
        return None

'''
counts the relative number of blocking positions
'''
def f5_blocking(inputState):
    # why this line?
    # b/c i modify state
    state = copy.deepcopy(inputState)
    p1_blocking = 0
    p2_blocking = 0

    activeBoards = getActive(state)

    for board in activeBoards:
        for row in board:
            getPot = hasBlock(row)
            if getPot == "2":
                p1_blocking += 1
            elif getPot == "1":
                p2_blocking += 1
    activeBoardsTranspose = zip(*activeBoards)
    for board in activeBoardsTranspose:
        #returns y=-x diagonal (the trace):
        diagonal1 = [board[i][i] for i in range(length)]
        #returns y=x diagonal:
        diagonal2 = [board[i][length-i-1] for i in range(length)]
        board += [diagonal1, diagonal2]
        for row in board:
            getPot = hasBlock(row)
            if getPot == "2":
                p1_blocking += 1
            elif getPot == "1":
                p2_blocking += 1
    return {'p1_blocking': p1_blocking, 'p2_blocking': p2_blocking,}

'''
counts the relative number of potential positions
'''
def f6_potential(state):
    # why this line?
    # b/c i modify state
    state = copy.deepcopy(inputState)
    thisPlayerStr = str(state.nextPiece[2])
    thisPlayerInt = state.nextPiece[2]

    otherPlayStr = str(turn(thisPlayerInt))
    otherPlayInt = turn(thisPlayerInt)

    p1_potential = 0
    p2_potential = 0
    activeBoards = getActive(state)

    for board in activeBoards:
        if not isWin(board):
            for row in board:
                getPot = hasPotential(row)
                if getPot == "2":
                    p1_potential += 1
                    p2_potential += 1
    return {'p1_potential': p1_potential, 'p2_potential': p2_potential,}

'''
alpha-beta helper
'''
def minH(state, depth, maxDepth, a, b):

    value = 9001
    s = State()
    gen = state.genChildren(s)
    nextS = gen.next()
    print "minH, depth is", depth

    if (depth == maxDepth) or (nextS == None):
        print "returned utility:", utility(state)
        state.printInfo()
        return utility(state)
    iterations = 0
    while nextS != None:
        print "min iterations: ", iterations
        copy_in = copy.deepcopy(nextS)
        value = min(value, maxH(copy_in, depth+1, maxDepth, a, b))
        assert type(value) == type(a)
        if value <= a:
            return -9001 # we don't want to choose this!
        b = min(b, value)
        nextS = gen.next()
    return value

'''
called by ab
The minmax alpha-beta prunning algorithm as described by Norvig p. 170
'''
def maxH(state, depth, maxDepth, a, b):
    print "called maxH; depth:", depth

    value = -9001
    s = State()
    gen = state.genChildren(s)
    nextS = gen.next()

    if (depth == maxDepth):
        return utility(state)

    if depth == 0:
        iteration = 0
        highestSoFar = copy.deepcopy(nextS)
        min_h = minH(nextS, depth+1, maxDepth, a, b)
        value = (min_h, highestSoFar)
        while nextS != None:
            iteration += 1
            print "min_h:", min_h
            #print value < (min_h, nextS), value, min_h, "see below", nextS == value[1]
            min_h = minH(nextS, depth+1, maxDepth, a, b)
            assert type(value) == type((min_h, nextS))
            value = copy.deepcopy(max( value, (min_h, nextS) ))
            print value
            if value >= (b, 'make comparisons work'):
                print "should not be true"
                return (9001, value[1]) # we don't want to select this
            a = max(a, value[0])
            #print "\n***\niteration ", iteration, nextS.printInfo(), nextS == value[1], value, "min_h: ", min_h, "iteration", iteration, "\n***\n\n"
            nextS = gen.next()
        return value
    else:
        while nextS != None:
            copy_in = copy.deepcopy(nextS)
            value = max(value, minH(copy_in, depth+1, maxDepth, a, b))
            assert type(value) == type(b)
            if value >= b:
                return 9001 # don't want to select this (another option is implied)
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
        new = copy.deepcopy(state)
        nextState = maxH(new, 0, farthestDepth, -9005, 9005)
        '''
        print "\n*"
        print state.printInfo()
        print "\n*"
        '''
        duration = time.clock() - start
        print "hi there!"
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
                        self.boards[y_board][x_board][y][x] = copy.copy(otherState.
                                                    boards[y_board][x_board][y][x])

    def copyThis(self, other):
        self.copyBoards(other)
        self.nextPiece = copy.copy(other.nextPiece)
        self.score = copy.copy(other.score)


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
Tests program
'''
def test():

    a = State()
    a.boards[0][0][0][0]['cell'] = 1
    a.boards[0][0][1][1]['cell'] = 1
    a.nextPiece[0] = 0
    a.nextPiece[1] = 0
    a.nextPiece[2] = 1

    a.printInfo()
    b = ab(a)[1]
    b.printInfo()

def getState():
    a = State()
    a.boards[0][0][0][0]['cell'] = 1
    a.boards[0][0][1][1]['cell'] = 1
    a.nextPiece = [0,0,1]
    return a
