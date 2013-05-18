import copy
import time
import random
import sys

DIMENSION = 3
WAIT = 5
userFirst = 1
computerFirst = 2
MIN = "1"
MAX = "2"
# standard function constants based on conjecture
# and limited gameplay experience
ALPHA = 0.005
CONSTS = {'c1': 21.0, 'c2':5.0, 'c3': 4.0,
                      'c4': 3.0, 'c5': 2.0, 'c6': 1.5,}
TD_CONSTS = {'c1': 21.0, 'c2':5.0, 'c3': 4.0,
                      'c4': 3.0, 'c5': 2.0, 'c6': 1.5,}

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

'''
Determines if the current board is full.
'''
def isFull(board):
    for row in board:
        for cell in row:
            if cell['cell'] == 0:
                return False
    return True

'''
Determines if the game is over!
If over, prints message and exits program.
'''
def checkOver(state):
    for rowBoards in state.boards:
        for board in rowBoards:
            if (not isFull(board)) and (not isWin(board)):
                return #
    if state.score['1'] == state.score['2']:
        print "Game Over.\nBoth players tied at", state.score['2'], "points."
    elif state.score['1'] > state.score['2']:
        print "Game Over.\nPlayer 1 won with", state.score['1'], "points versus", state.score['2'], "points for player 2!"
    elif state.score['1'] < state.score['2']:
        print "Game Over.\nPlayer 2 won with", state.score['2'], "points versus", state.score['1'], "points for player 1"
    print "Final board position was:"
    state.printInfo()
    sys.exit(0)

''' the utility function! '''
def utility(state, constants, sub):
    f1 = f1_score(state) * constants['c1']
    f2 = f2_center(state) * constants['c2']
    f3 = f3_corner(state) * constants['c3']
    f4 = f4_side(state) * constants['c4']
    f5 = f5_blocking(state) * constants['c5']
    f6 = f6_potential(state) * constants['c6']
    if sub:
        return -(f1 + f2 + f3 + f4 + f5 + f6)
    else:
        return (f1 + f2 + f3 + f4 + f5 + f6)

''' the utility function plus dictionary for TD learning! '''
def subUtil(state, constants, sub):
    f1 = f1_score(state) * constants['c1']
    f2 = f2_center(state) * constants['c2']
    f3 = f3_corner(state) * constants['c3']
    f4 = f4_side(state) * constants['c4']
    f5 = f5_blocking(state) * constants['c5']
    f6 = f6_potential(state) * constants['c6']
    if sub:
        return [-f1, -f2, -f3, -f4, -f5, -f6]
    else:
        return [f1, f2, f3, f4, f5, f6]


'''
Calculated by subtracting score of current player
from score of opponent.
'''
def f1_score(state):
    # Why MIN - MAX ?
    # Because player who call utility does not change state
    # so the state corresponds to the previous player.
    return state.score[MIN] - state.score[MAX]

'''
Returns all the boards that have not been won yet.
'''
def getActive(state):
    active_boards = []
    for line_boards in state.boards:
        for board in line_boards:
            if (not isWin(board)) and (not isFull(board)):
                # copy because i think i might be modifying memory:
                active_boards += [board]
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
Relative number of ACTIVE corner
pieces
'''
def f3_corner(state):
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
Relative number of ACTIVE side
pieces
'''
def f4_side(state):
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
def minH(state, depth, maxDepth, a, b, constants, sub):

    value = 9001.0
    s = State()
    gen = state.genChildren(s)
    nextS = gen.next()

    if (depth == maxDepth) or (nextS == None):
        return utility(state, constants, sub)

    iterations = 0
    copy_in = State()
    while nextS != None:
        copy_in.copyThis(nextS)
        value = min(value, maxH(copy_in, depth+1, maxDepth, a, b, constants, sub))
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
def maxH(state, depth, maxDepth, a, b, constants, sub):

    value = -9001.0
    s = State()
    gen = state.genChildren(s)
    nextS = gen.next()

    if (depth == maxDepth):
        return utility(state, constants, sub)

    if depth == 0:
        iteration = 0

        highestSoFar = State()
        highestSoFar.copyThis(nextS)

        min_h = minH(nextS, depth+1, maxDepth, a, b, constants, sub)
        value = (min_h, highestSoFar)
        while nextS != None:
            iteration += 1
            min_h = minH(nextS, depth+1, maxDepth, a, b, constants, sub)
            assert type(value) == type((min_h, nextS))
            value = copy.deepcopy(max( value, (min_h, nextS) ))
            if value >= (b, 'make comparisons work'):
                return (9001.0, value[1]) # we don't want to select this
            a = max(a, value[0])
            nextS = gen.next()
        return value
    else:
        copy_in = State()
        while nextS != None:
            copy_in.copyThis(nextS)
            value = max(value, minH(copy_in, depth+1, maxDepth, a, b, constants, sub))
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
def ab(state, constants, sub):
    start = time.clock()
    farthestDepth = 1
    duration = 0
    while (duration < WAIT and farthestDepth < 4):
        new = copy.deepcopy(state)
        nextState = maxH(new, 0, farthestDepth, -9005.0, 9005.0, constants, sub)
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
        print "boards are:\n", self.printer(), "You are playing into board column", self.nextPiece[1], "row", self.nextPiece[0], "\nScore is:", self.score#, "Complicated info:\n", self.printerComplicated()


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

''' Face the AI in meta-ttt '''
def playAI():
    print messageWelcome
    playUntilExit()

def playUntilExit():
    """ Play successive games until the user decides to stop. """
    while True:
        firstPlayer = getFirstPlayer()
        playType = raw_input("Do you want to play against AI (1)\nor let the AI play against itself(2)?")
        if playType.isdigit() and int(playType) == 2:
            a = State() # create a new empty board :)
            learning_TD_AI(a)
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
            SUBTRACT = True
            return 1
        elif response == "2":
            SUBTRACT = False
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

        state.nextPiece[2] = 2

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
    checkOver(state)

    print "You are playing piece", state.nextPiece[2]
    while True:
        if isWin(state.boards[state.nextPiece[0]][state.nextPiece[1]]):
            print "You must select a board to play into"
            x_board = raw_input("Assign column of meta-board to play into")
            y_board = raw_input("Assign row of meta-board to play into")
            if x_board.isdigit() and y_board.isdigit() and (not isWin(state.boards[int(y_board)][int(x_board)])):
                x_board = int(x_board)
                y_board = int(y_board)
                x = raw_input("Assign column of next piece")
                y = raw_input("Assign row of next piece")

                # adjust piece b/c this is how isUnoccupied[sic] works...
                state.nextPiece = [y_board,x_board,state.nextPiece[2]]

                if x.isdigit() and y.isdigit() and state.isUnoccupied(int(y), int(x)):
                    x = int(x)
                    y = int(y)
                    state.boards[y_board][x_board][y][x]['cell'] = state.nextPiece[2]
                    if isWin(state.boards[y_board][x_board]):
                        state.score[str(state.nextPiece[2])] += 1
                    state.nextPiece = [y, x, turn(state.nextPiece[2])]
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
    checkOver(state)
    print state.printInfo()
    (expectedUtility, nextState) = ab(state, CONSTS, True)
    print "Expected utility is: ", expectedUtility
    nextState.printInfo()
    state = copy.deepcopy(nextState)
    print "Scores: Player 1: ", state.score['1'], " Player 2: ", state.score['2']
    userTurn(state)

def normalize (tdConsts):
    norm = reduce( (lambda x,y: x+y), CONSTS.values())
    tot = reduce( (lambda x,y: x+y), tdConsts.values())
    for i in range(len(tdConsts)):
        tdConsts['c' + str(i+1)] = tdConsts['c' + str(i+1)] / tot * norm
    return tdConsts

def learning_TD_AI(prevState):
    print "\n\nTD AI player starting turn...", prevState.nextPiece[2]
    print "nativeAI", prevState.nextPiece[2]
    checkOver(prevState)

    # print, alpha-beta search etc.:
    SUBTRACT = False
    global TD_CONSTS
    (expectedUtility, state) = ab(prevState, TD_CONSTS, SUBTRACT)
    print "Expected utility is: ", expectedUtility, "\nTD_CONSTS for player",state.nextPiece[2],"are: ", TD_CONSTS
    print "Scores: Player 1: ", state.score['1'], " Player 2: ", state.score['2']
    state.printInfo()


    # modify temporal difference:
    changeTotalUtility = utility(state, TD_CONSTS, SUBTRACT) - utility(prevState, TD_CONSTS, SUBTRACT)
    sub1 = subUtil(state, TD_CONSTS, SUBTRACT)
    sub2 = subUtil(prevState, TD_CONSTS, SUBTRACT)
    changeSubUtil = [ (sub1[i] - sub2[i]) for i in range(len(sub1)) ]
    for i in range(len(TD_CONSTS)):
        TD_CONSTS['c' + str(i+1)] += ALPHA * changeTotalUtility * abs(changeSubUtil[i])

    # normalize
    TD_CONSTS = normalize(TD_CONSTS)

    print "TD_CONSTS after being adjusted are: ", TD_CONSTS
    naiveAI(state)

def naiveAI(state):
    print "\n\nNaive AIs turn: "
    print "nativeAI", state.nextPiece[2]
    SUBTRACT = True
    checkOver(state)
    (expectedUtility, nextState) = ab(state, CONSTS, SUBTRACT)
    print "Expected utility is: ", expectedUtility
    state = copy.deepcopy(nextState)
    print "Scores: Player 1: ", state.score['1'], " Player 2: ", state.score['2']
    state.printInfo()

    learning_TD_AI(state)

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
    a.nextPiece[2] = 1
    SUBTRACT = False
    b = ab(a, CONSTS, SUBTRACT)[1]
    print utility(b, CONSTS, SUBTRACT)
    b.printInfo()

'''
Test for f2_center
'''
def test2():
    a = State()
    a.nextPiece[0] = 1
    a.nextPiece[1] = 1
    a.printInfo()
    b = ab(a, CONSTS)[1]
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

    b = ab(a, CONSTS)[1]
    b.printInfo()

def getState():
    a = State()
    a.boards[0][0][2][0]['cell'] = 2
    a.boards[0][0][0][2]['cell'] = 2
    a.boards[0][0][1][2]['cell'] = 1
    a.nextPiece = [0,0,1]
    return a
