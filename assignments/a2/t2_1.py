import collections
import numpy as np
import heapq
import time

class PriorityQueue:
    def  __init__(self):
        self.Heap = []
        self.Count = 0

    def push(self, item, priority):
        entry = (priority, self.Count, item)
        heapq.heappush(self.Heap, entry)
        self.Count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.Heap)
        return item

    def isEmpty(self):
        return len(self.Heap) == 0
    
def transferToGameState(layout):
    layout = [x.replace('\n','') for x in layout]
    layout = [','.join(layout[i]) for i in range(len(layout))]
    layout = [x.split(',') for x in layout]
    maxColsNum = max([len(x) for x in layout])
    for irow in range(len(layout)):
        for icol in range(len(layout[irow])):
            if layout[irow][icol] == '.': layout[irow][icol] = 0  
            elif layout[irow][icol] == 'W': layout[irow][icol] = 1 
            elif layout[irow][icol] == 'K': layout[irow][icol] = 2 
            elif layout[irow][icol] == 'B': layout[irow][icol] = 3 
            elif layout[irow][icol] == 'G': layout[irow][icol] = 4 
            elif layout[irow][icol] == '*': layout[irow][icol] = 5 
        colsNum = len(layout[irow])
        if colsNum < maxColsNum:
            layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 
    return np.array(layout)

def PosOfPlayer(gameState):
    return tuple(np.argwhere(gameState == 2)[0]) 
def PosOfBoxes(gameState):
    return tuple(tuple(x) for x in np.argwhere((gameState == 3) | (gameState == 5)))
def PosOfWalls(gameState):
    return tuple(tuple(x) for x in np.argwhere(gameState == 1)) 

def PosOfGoals(gameState):
    return tuple(tuple(x) for x in np.argwhere((gameState == 4) | (gameState == 5)))

def isEndState(posBox):
    return sorted(posBox) == sorted(posGoals)

def isLegalAction(action, posPlayer, posBox):
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

def heuristic(posPlayer, posBox):
    distance = 0
    completes = set(posGoals) & set(posBox)
    sortposBox = list(set(posBox).difference(completes))
    sortposGoals = list(set(posGoals).difference(completes))
    for i in range(len(sortposBox)):
        distance += (abs(sortposBox[i][0] - sortposGoals[i][0])) + (abs(sortposBox[i][1] - sortposGoals[i][1]))
    return distance

def cost(actions):
    return len([x for x in actions if x.islower()])

def aStarSearch():
    beginBox = PosOfBoxes(gameState)
    beginPlayer = PosOfPlayer(gameState)

    start_state = (beginPlayer, beginBox)
    frontier = PriorityQueue()
    frontier.push([start_state], heuristic(beginPlayer, beginBox))
    exploredSet = set()
    actions = PriorityQueue()
    actions.push([0], heuristic(beginPlayer, start_state[1]))
    while frontier:
        node = frontier.pop()
        node_action = actions.pop()
        if isEndState(node[-1][-1]):
            print(','.join(node_action[1:]).replace(',',''))
            moves = ''.join(node_action[1:]).replace(',','')
            break
        if node[-1] not in exploredSet:
            exploredSet.add(node[-1])
            Cost = cost(node_action[1:])
            for action in legalActions(node[-1][0], node[-1][1]):
                newPosPlayer, newPosBox = updateState(node[-1][0], node[-1][1], action)
                
                Heuristic = heuristic(newPosPlayer, newPosBox)
                frontier.push(node + [(newPosPlayer, newPosBox)], Heuristic + Cost) 
                actions.push(node_action + [action[-1]], Heuristic + Cost)
    return moves

if __name__ == '__main__':
    time_start = time.time()
    with open('./zad_input.txt',"r") as f: 
        layout = f.readlines()
    gameState = transferToGameState(layout)
    posWalls = PosOfWalls(gameState)
    posGoals = PosOfGoals(gameState)
    moves = aStarSearch()
    with open("./zad_output.txt", "w") as f:
        f.write(moves.upper())
    time_end=time.time()
    print('Runtime',"%.4f" %(time_end-time_start))