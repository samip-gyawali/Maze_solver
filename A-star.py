class Node(object):
    def __init__(self,state,parent,action,goalState):
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic = abs(goalState[0]-self.state[0]) + abs(goalState[1]-self.state[1])
        if self.parent == None:
            self.steps = 0
        else:
            self.steps = self.parent.steps + 1
        
        self.totalEstimate = self.heuristic + self.steps
        

class Frontier(object):
    def __init__(self):
        self.frontier = []
    
    def contains_state(self,state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return (len(self.frontier) == 0)
    
    def remove(self):
        thisNode = self.frontier[0]
        self.frontier = self.frontier[1:]
        return thisNode

    def add(self,node):
        found = False
        i = 0
        temp = []
        while i < len(self.frontier) and not found:
            if self.frontier[i].totalEstimate < node.totalEstimate:
                temp.append(self.frontier[i])
                i += 1
            else:
                found = True
        
        temp.append(node)
        temp.extend(self.frontier[i:])
        self.frontier = temp

class Maze(object):
    def __init__(self,fileName):
        self.solution = []
        self.explored = set()
        self.walls = []
        self.height = -1
        self.width = -1
        self.start = ()
        self.goal = ()

        with open(fileName,'r') as f:
            fileContents = f.read()
        
        if fileContents.count('A') != 1:
            raise Exception("Maze must start at exactly one point!")
        
        if fileContents.count('B') != 1:
            raise Exception("Maze must end at exactly one point!")

        fileContents = fileContents.splitlines()

        self.height = len(fileContents)
        self.width = len(fileContents[0])

        for r in range(self.height):
            for c in range(self.width):
                if fileContents[r][c] == '#':
                    self.walls.append((r,c))
                elif fileContents[r][c] == 'A':
                    self.start = (r,c)
                elif fileContents[r][c] == 'B':
                    self.goal = (r,c)
    
    def __isValid(self,state):
        r,c = state
        if (state not in self.walls) and (state not in [node.state for node in list(self.explored)]) and (0<=r<self.height) and (0<=c<self.width):
            return True
        else:
            return False
    
    def __isGoal(self,state):
        return (self.goal == state)

    def solve(self):
        startNode = Node(self.start, None, None, self.goal) #Start
        solved = False
        frontier = Frontier()
        frontier.add(startNode)

        while not solved and not frontier.empty():
            currentNode = frontier.remove()
            self.explored.add(currentNode)
            if self.__isGoal(currentNode.state):
                solved = True
            else:
                r,c = currentNode.state

                possibleMoves = [
                    (r+1,c),
                    (r-1,c),
                    (r,c+1),
                    (r,c-1)
                ]

                for mr,mc in possibleMoves:
                    possibleNode = Node((mr,mc),currentNode,(mr-r,mc-c),self.goal)
                    if self.__isValid(possibleNode.state):
                        frontier.add(possibleNode)
        
        self.__showSolution()
        self.__showExplored()

    def __showSolution(self):
        exploredNodes = list(self.explored)
        exploredStates = [node.state for node in exploredNodes]
        thisNode = exploredNodes[exploredStates.index(self.goal)]

        while thisNode.parent != None: # Until the start state
            self.solution.append(thisNode.state)
            thisNode = thisNode.parent
        
        with open('./A star search/Maze_3/solution.txt','w') as f:
            for r in range(self.height):
                for c in range(self.width):
                    if (r,c) == self.start:
                        f.write('A')
                    elif (r,c) == self.goal:
                        f.write('B')
                    elif (r,c) in self.walls:
                        f.write('#')
                    elif (r,c) in self.solution:
                        f.write('|')
                    else:
                        f.write(' ')

                f.write('\n')                    
    
    def __showExplored(self):

        with open('./A star search/Maze_3/explored.txt','w') as f:
            for r in range(self.height):
                for c in range(self.width):
                    if (r,c) == self.start:
                        f.write('A')
                    elif (r,c) == self.goal:
                        f.write('B')
                    elif (r,c) in self.walls:
                        f.write('#')
                    elif (r,c) in [node.state for node in list(self.explored)]:
                        f.write('|')
                    else:
                        f.write(' ')

                f.write('\n')      

            f.write(f'\nTotal Explored: {len(self.explored)}')              


myMaze = Maze('maze3.txt')
myMaze.solve()