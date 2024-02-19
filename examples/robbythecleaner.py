import random

situation = []
for north in range(0, 3): # We will always find ourselves in a situation of the form <North, South, East, West, Current>.
    for south in range(0, 3):
        for east in range(0, 3):
            for west in range(0, 3):
                for current in range(0, 3):
                    sit = north * 10000 + south * 1000 + east * 100 + west * 10 + current
                    situation.append(sit)

STRATEGYLENGTH = 243


 
def randomStrategy(): # 0 stands for MoveNorth, 1 stands for MoveSouth, 2 stands for MoveEast, 3 stands for MoveWest, 4 stands for StayPut, 5 stands for PickUp, 6 stands for RandomMove
    l = []
    for i in range(STRATEGYLENGTH):
        l.append(random.randint(0,6)) 
    return l

def move(action: int, pos: tuple[int], board):
    (x, y) = pos
    score = 0 
    if action == 0: # Action is MoveNorth. 
        if x == 0: #If x == 0, then there's a wall to the north, so a crash will happen. 
            return (-5, (x,y), board)
        else:
            return (0, (x-1,y), board)

    if action == 1: # Action is MoveSouth.
        if x == 9: # Hit wall     
            return (-5, (x,y), board)
        else:
            return (0, (x+1,y), board)   
        
    if action == 2: # Action is MoveEast.
        if y == 9: # Hit wall
            return (-5,(x,y), board)
        else:
            return (0,(x,y+1), board)
        
    if action == 3: # Action is MoveWest
        if y == 0: # Hit wall 
            return (-5,(x,y), board)
        else:
            return (0,(x,y-1), board)
        
    if action == 4: # Action is StayPut
        return (0, (x,y), board)
    
    if action == 5: # Action is PickUpCan
        if board[x][y] == 1:
            board[x][y] = 0
            return (10,(x,y), board)
        else:
            return (-1,(x,y), board)
        
    if action == 6: # Action is RandomMove
        return move(random.randint(0,6), pos, board)
    
def generateBoard():
    return [[random.randint(0, 1) for j in range(10)] for i in range(10)]  # This generates a random cleaning board.

def evaluate_strategy(strategy: list[int]):
    scoresum = 0
    for round in range(100):
        board = generateBoard()
        current_situation = 2*10000 + board[1][0]*1000 + board[0][1]*100 + 2*10 + board[0][0] #currentsituation is [North, South, East, West, Current]. I start on board[0][0], so North and West are Walls, hence contain '2'.
        current_score = 0
        current_position = (0, 0)
        for i in range (200):
            sit_index = situation.index(current_situation)
            action = strategy[sit_index]
            (action_score, current_position, board) = move(action, current_position, board)
            current_score += action_score
        scoresum += current_score
    
    return scoresum/100   # The fitness of a strategy is its average score over 100 trials.

def mating(l1: list[int], l2: list[int]):
    splittingpoint = random.randint(1,STRATEGYLENGTH-1)
    child1 = l1 [:splittingpoint] + l2 [splittingpoint:] # child1 is obtained by picking a random splitting point and doing basic shuffling
    child2 = l2 [:splittingpoint] + l1 [splittingpoint:] # Likewise for child2

    mutations1 = random.randint(0,5) # The number of mutations that will occur in child1
    mutations2 = random.randint(0,5) # The number of mutations that will occur in child2

    for i in range(mutations1):
        position = random.randint(0,STRATEGYLENGTH-1)  # We mutated child1
        child1[position] = random.randint(0,6)

    for i in range(mutations2):
        position = random.randint(0,STRATEGYLENGTH-1) # We mutated child2
        child2[position] = random.randint(0,6)
    
    return (child1,child2)

popstr = []

for i in range(200):
    popstr.append(randomStrategy()) # This generates a list of 200 strategies. Again, a strategy just tells you what to do in a certain situation, e.g. move to the north (0). 
    
for count in range(1000):

    fitness_list = []

    for i in range (len(popstr)):
        fitness_list.append(evaluate_strategy(popstr[i]))

    spf = [(fitness_list[i],popstr[i]) for i in range (len(fitness_list))]

    spf.sort(reverse=True)

    print(spf[0][0])

    newpopulation = []

    for i in range(100):
        (strategy1,strategy2) = mating(spf[random.randint(0,5)][1],spf[random.randint(0,5)][1]) # Pick two fit parents to obtain two probabilistically fit children
        newpopulation.append(strategy1)
        newpopulation.append(strategy2)

    popstr = newpopulation













        



