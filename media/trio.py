#!python

# Trio! Command-Line Interface (CLI)
# author: Chet Weger
# purpose: Presents a simple interface the Trio! game, as explained in assignment 3
#
# My program works ok... I think it has 3x3 solved.  However, it's pretty slow on larger boards
# because I have a very slow utility function and I make alot of copies which is very expensive.
# 

from random import randrange
import numpy as numpy_library
import itertools as itertools
import copy
import time

# The game is played on a rows x rows board with attributes attributes.
# For now rows and attributes are as specified as constants
rows = 3
attributes = 3

messageComputersTurn     = "Computer's turn."
messageChoosePlayer      = "Which player goes first? (1 = you, 2 = computer, 0 = stop) "
messageGoodbye           = "Goodbye. Thanks for playing Trio!."
messageTryAgain          = "That is invalid. Please try again."
messageUsersTurn         = "User's turn."
messageWelcome           = "Welcome to Trio!."
messageYouWin            = "User wins."
messageCompWin           = "Computer Wins"
wait = 40

interCellGap = " "

userFirst = 1
computerFirst = 2

empty = -1

'''
returns true if there is a 'matching'
'''
def matching(touple):
    listAnd = reduce( (lambda x,y: x&y), touple) #should be NON zero if 1's matching exists

    opposite = map ( (lambda x: ~x), touple)
    mask = 2**attributes - 1
    masked_opposite = map( (lambda x: x&mask), opposite)
    listAnd_opposite = reduce( (lambda x,y: x&y), masked_opposite)  #should be NON zero if 0's matching exists

    unplayed = ~reduce( (lambda x,y: x|y), touple) #should BE ZERO iff there was -1 in touple

    #print listAnd, listAnd_opposite, unplayed
    return ( (bool(listAnd) or bool(listAnd_opposite)) and bool(unplayed) )

'''
returns true if board has a victory
'''
def isWinning(board):
    for row in board:
        if(matching(row)):
            return True
    board_Transpose = zip(*board)
    for column in board_Transpose:
        if(matching(column)):
            return True
    length = len(board)
    diagonal1 = tuple(board[i][i] for i in range(length)) #returns y=-x diagonal (the trace)
    diagonal2 = tuple(board[i][length-i-1] for i in range(length)) #returns y=x diagonal
    if(matching(diagonal1) or matching(diagonal2)):
        return True
    return False

'''
Utility basically measures the number of "options" that a player has.  it is sort of equivalent to looking 2 extra steps ahead, but it provides valuable information about trends...
'''
def noWin(state):
    a = State()
    gen = state.nextLayerPiece(a)
    nextS = gen.next()
    while(nextS != None):
        if isWinning(nextS.board):
            return False
        nextS = gen.next()
    return True

def countOptions(state):
    nextLayer = state.nextLayerList()
    filterList = filter(noWin, nextLayer)
    return len(filterList)

'''
alpha-beta helper
'''
def minH(state, depth, maxDepth, a, b, parentNumOptions):
    if(len(state.unplayedPieces) == 0):
        return 0

    childNumOptions = countOptions(state)

    if(depth == maxDepth):
        return (childNumOptions - parentNumOptions + 50)
    a = State()
    gen = state.nextLayer(a)
    nextS = gen.next()
    returnedV = (9005, state.pair)
    while(nextS != None):
        if(not isWinning(nextS.board)):
            returnedV = min(returnedV, (maxH(nextS, depth+1, maxDepth, a, b, childNumOptions), nextS.pair))
            if(returnedV[0] <= a):
                return returnedV
            b = min(b, returnedV[0])
        elif(isWinning(nextS.board)):
            return -200 # defeat
        nextS = gen.next()
    return returnedV

def maxH(state, depth, maxDepth, a, b, parentNumOptions):
    if(len(state.unplayedPieces) == 0):
        return 0

    childNumOptions = countOptions(state)

    if(depth == maxDepth):
        return (childNumOptions - parentNumOptions, + 50)
    a = State()
    gen = state.nextLayer(a)
    nextS = gen.next()
    returnedV = (-9005, state.pair)
    while(nextS != None):
        if(not isWinning(nextS.board)):
            returnedV = max(returnedV, (minH(nextS, depth+1, maxDepth, a, b, childNumOptions), nextS.pair))
            if(returnedV[0] >= b):
                return returnedV
            a = max(a, returnedV[0])
        elif(isWinning(nextS.board)):
            return 200 # victory
        nextS = gen.next()
    return returnedV



'''
Checks if a win exists
Then calls helper
'''
def ab(state):
    a = State()
    nL = state.nextLayerPiece(a)
    nextS = nL.next()
    while(nextS != None):
        if isWinning(nextS.board):
            print "board was winning", nextS.board
            return (3, nextS.pair)
        nextS = nL.next()
    start = time.clock()
    farthestDepth = 1
    duration = 0
    while(duration<wait and farthestDepth < 4):
        pair = maxH(state, 0, farthestDepth, -9005, 9005, 63)
        duration = time.clock() - start
        farthestDepth = farthestDepth + 1
        if(farthestDepth>2**rows):
            break #exit if depth is terminated :)
    return pair

'''
Stores info on game and creates "next layer"
In retrospect, the biggest problem with my program is that I make so many deepcopies... it's very slow to create new layers
'''
class State:
# state represents the board, next piece to be played, and other relevant info
    def __init__(self):
        """ Construct a new board. """
        self.board = [[empty for col in range(rows)] for row in range(rows)]
        self.unplayedCoordinates = list(itertools.product(range(rows),range(rows)))
        self.unplayedPieces = range(2**attributes)
        self.nextPiece = 0
        self.unplayedPieces.remove(0)
        self.pair = ()
    def printer(self):
        for row in self.board:
            print row

    def printInfo(self):
        print "board is:", self.board, "unplayedPieces are", self.unplayedPieces, "unplayedCoordinates are", self.unplayedCoordinates, "next piece is", self.nextPiece, "isWinning?", isWinning(self.board), "utility is", utility(self)

    def copyBoard(self, otherBoard):
        for i in range(len(otherBoard.board)):
            self.board[i] = copy.copy(otherBoard.board[i])

    def copyThis(self, state):
        self.copyBoard(state)
        self.unplayedCoordinates = copy.copy(state.unplayedCoordinates)
        self.unplayedPieces = copy.copy(state.unplayedPieces)
        self.nextPiece = copy.copy(state.nextPiece)
        self.pair = copy.copy(state.pair)

    def nextLayerList(self): #list of states
        nextMovesList = []
        for co in self.unplayedCoordinates:
            for nextPiece in self.unplayedPieces:
                a = State()
                a.copyThis(self)
                a.board[co[0]][co[1]] = a.nextPiece
                a.nextPiece = nextPiece
                try:
                    a.unplayedCoordinates.remove(co)
                except:
                    1#do nothing

                try:
                    a.unplayedPieces.remove(nextPiece)
                except:
                    1#do nothing
                a.pair = (co,nextPiece)
                nextMovesList.append(a)
        return nextMovesList

    def nextLayer(self, a): #list of states
        for co in self.unplayedCoordinates:
            for nextPiece in self.unplayedPieces:
                a.copyThis(self)
                a.board[co[0]][co[1]] = a.nextPiece
                a.nextPiece = nextPiece
                try:
                    a.unplayedCoordinates.remove(co)
                except:
                    1#do nothing

                try:
                    a.unplayedPieces.remove(nextPiece)
                except:
                    1#do nothing
                a.pair = (co,nextPiece)
                yield a
        yield None

    def nextLayerPiece(self, a): #list of states
        for co in self.unplayedCoordinates:
            a.copyThis(self)
            a.board[co[0]][co[1]] = a.nextPiece
            try:
                a.unplayedCoordinates.remove(co)
            except:
                1#do nothing
            a.pair = (co, a.nextPiece)
            yield a
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
        rowsStr = raw_input("Enter the number of rows ")
        attributesStr = raw_input("Enter the size of the pieces (in bits) ")
        if rowsStr.isdigit() and attributesStr.isdigit():
            global rows
            rows = int(rowsStr)
            global attributes
            attributes = int(attributesStr)
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

def playTrio(firstPlayer):
    """ Play the game, given first player, or stop. """
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


def userTurn(state):
    """ Simulate one round of play with the user starting. """
    print messageUsersTurn
    print state.printer()
    while True:
        msg = "Determine X value/location of next piece (piece==" + str(state.nextPiece) + ")"
        x = raw_input(msg)
        y = raw_input("Place y value of next piece (higher values are lower)")

        if( (x).isdigit() and (y).isdigit() and ((int(y),int(x)) in state.unplayedCoordinates) ):
            x = int(x)
            y = int(y)
            break
        else:
            print messageTryAgain
    state.board[y][x] = state.nextPiece

    try:
        state.unplayedCoordinates.remove((y,x))
    except:
        1#do nothing

    try:
        state.unplayedPieces.remove(state.nextPiece)
    except:
        1#do nothing
    if isWinning(state.board):
        print messageYouWin
        return 0

    if len(state.unplayedPieces) == 0:
        print messageDraw
        return 0

    while True:
        msg = "Please select one of the following pieces:" + "".join(map (str, state.unplayedPieces))
        nextPiece = raw_input(msg)
        if( (nextPiece).isdigit() and (int(nextPiece) in state.unplayedPieces) ):
            nextPiece = int(nextPiece)
            break
        else:
            print messageTryAgain
    state.unplayedPieces.remove(nextPiece)
    state.nextPiece = nextPiece
    state.printer()


def computerTurn(state):
    """ Simulate the computer's turn. """
    print messageComputersTurn
    print state.printer()

    # pick a random cell from the ones remaining

    # PICKS AN UNOCCUPIED CELL ANYWA

    (x,(coordinate, piece)) = ab(state)
    print coordinate, x, piece
    print state.nextPiece
    state.board[coordinate[0]][coordinate[1]] = state.nextPiece
    try:
        state.unplayedPieces.remove(state.nextPiece)
    except:
        1#nothing
    try:
        state.unplayedCoordinates.remove(coordinate)
    except:
        1#nothing
    state.nextPiece = piece
    # if user won, end game
    if isWinning(state.board):
        print messageCompWin
        state.printer()
        return 0

    # if it is a draw, end game
    if len(state.unplayedPieces) == 0:
        print messageDraw
        state.printer()
        return 0

print "To start the game enter \"main()\". Board sizes beyond 3x3 may take VERY long to complete search." 
