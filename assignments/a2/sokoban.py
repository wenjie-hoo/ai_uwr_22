import collections
import numpy as np

def transferToGameState(layout):
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == '.': layout[irow][icol] = 0   # free space
            elif layout[irow][icol] == 'W': layout[irow][icol] = 1 # wall
            elif layout[irow][icol] == 'K': layout[irow][icol] = 2 # player
            elif layout[irow][icol] == 'B': layout[irow][icol] = 3 # box
            elif layout[irow][icol] == 'G': layout[irow][icol] = 4 # goal
            elif layout[irow][icol] == '*': layout[irow][icol] = 5 # box on goal
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 
    return np.array(layout)

def PosOfPlayer(gameState):
    #Return the position of agent
    return tuple(np.argwhere(gameState == 2)[0]) 
def PosOfBoxes(gameState):
    #Return the positions of boxes
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5)))

def PosOfWalls(gameState):
    #Return the positions of walls
    return tuple(tuple(x) for x in np.argwhere(gameState == 1)) # e.g. like those above

def PosOfGoals(gameState):
    #Return the positions of goals
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5))) # e.g. like those above

def isEndState(posBox):
    #Check if all boxes are on the goals
    return sorted(posBox) == sorted(posGoals)

def isLegalAction(action, posPlayer, posBox):
    #Check if the given action is legal
    xPlayer, yPlayer = posPlayer
    if action[-1].isupper(): # the move was a push
        x1, y1 = xPlayer + 2 * action[0], yPlayer + 2 * action[1]
    else:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
    return (x1, y1) not in posBox + posWalls

def legalActions(posPlayer, posBox):
    allActions = [[-1,0,'u','U'],[1,0,'d','D'],[0,-1,'l','L'],[0,1,'r','R']]
    xPlayer, yPlayer = posPlayer
    legalActions = []
    for action in allActions:
        x1, y1 = xPlayer + action[0], yPlayer + action[1]
        if (x1, y1) in posBox: # the move was a push
            action.pop(2) # drop the little letter
        else:
            action.pop(3) # drop the upper letter
        if isLegalAction(action, posPlayer, posBox):
            legalActions.append(action)
        else: 
            continue     
    return tuple(tuple(x) for x in legalActions) 

def updateState(posPlayer, posBox, action):
    xPlayer, yPlayer = posPlayer # the previous position of player
    newPosPlayer = [xPlayer + action[0], yPlayer + action[1]] # the current position of player
    posBox = [list(x) for x in posBox]
    if action[-1].isupper(): # if pushing, update the position of box
        posBox.remove(newPosPlayer)
        posBox.append([xPlayer + 2 * action[0], yPlayer + 2 * action[1]])
    posBox = tuple(tuple(x) for x in posBox)
    newPosPlayer = tuple(newPosPlayer)
    return newPosPlayer, posBox



def breadthFirstSearch():
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)
    startState = (beginPlayer, beginBox)
    frontier = collections.deque([[startState]]) # store states
    actions = collections.deque([[0]]) # store actions
    exploredSet = set()
    while frontier:
        node = frontier.popleft()
        node_action = actions.popleft() 
        if isEndState(node[-1][-1]):
            moves = ''.join(node_action[1:]).replace(',','')
            break
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            for action in legalActions(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)
                frontier.append(node + [(newPosPlayer, newPosBox)])
                actions.append(node_action + [action[-1]])
    return moves

if __name__ == '__main__':
    with open('./zad_input.txt',"r") as f: 
        layout = f.readlines()
    gameState = transferToGameState(layout)
    posWalls = PosOfWalls(gameState)
    posGoals = PosOfGoals(gameState)
    moves = breadthFirstSearch()
    with open("./zad_output.txt", "w") as f:
        f.write(moves.upper())