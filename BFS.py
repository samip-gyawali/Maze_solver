class Node(object):
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

class Frontier(object): # Stack Frontier for DFS
    def __init__(self):
        self.frontier = []
        
    def add(self,node):
        self.frontier.append(node)
    
    def remove(self):
        if not self.empty():
            thisNode = self.frontier[0]
            self.frontier = self.frontier[1:]
            return thisNode
    
    def contains_state(self,state):
        return any(state == node.state for node in self.frontier)

    def empty(self):
        return (len(self.frontier) == 0)
    

class Maze(object):
    def __init__(self, fileName):
        self.height = -1
        self.width =  -1
        self.walls = []
        self.explored = set()
        self.solution = []
        self.start = ()
        self.goal = ()

        with open(fileName,'r') as f:
            fileContents = f.read()
    
        if fileContents.count('A') != 1:
            raise Exception("Maze must begin at a single point!")
        if fileContents.count('B') != 1:
            raise Exception("Maze must end at a single point!")

        fileContents = fileContents.splitlines()
        self.height = len(fileContents)
        self.width = len(fileContents[0])

        for r in range(self.height):
            for c in range(self.width):
                if fileContents[r][c] == 'A':
                    self.start = (r,c)
                elif fileContents[r][c] == 'B':
                    self.goal = (r,c)
                elif fileContents[r][c] == '#':
                    self.walls.append((r,c))

    def __isValid(self,state):
        r,c = state

        if (state not in self.walls) and (state not in [node.state for node in list(self.explored)]) and (0<=r<self.height) and (0<=c<self.width):
            return True
        else:
            return False
    
    def solve(self):
        startNode = Node(self.start,None,None)
        solved = False
        frontier = Frontier()
        frontier.add(startNode)

        while not solved and not frontier.empty():
            currentNode = frontier.remove()
            self.explored.add(currentNode)
            if currentNode.state == self.goal:
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
                    if self.__isValid((mr,mc)):
                        possibleNode = Node((mr,mc),currentNode,(mr-r,mc-c))
                        frontier.add(possibleNode)

        self.__showSolution()
        self.__showExplored()

    def __showSolution(self):
        exploredNodes = list(self.explored)
        exploredStates = [node.state for node in exploredNodes]
        thisNode = exploredNodes[exploredStates.index(self.goal)] # begin from goal

        while thisNode.parent != None:
            self.solution.append(thisNode.state)
            thisNode = thisNode.parent
        
        with open('./BFS/Maze_3/solution.txt','w') as f:
            for r in range(self.height):
                for c in range(self.width):
                    if (r,c) == self.start:
                        f.write('A')
                    elif (r,c) == self.goal:
                        f.write('B')
                    elif (r,c) in self.solution:
                        f.write('|')
                    elif (r,c) in self.walls:
                        f.write('#')
                    else:
                        f.write(' ')
                
                f.write('\n')
    
    def __showExplored(self):
        with open('./BFS/Maze_3/explored.txt','w') as f:
            for r in range(self.height):
                for c in range(self.width):
                    if (r,c) == self.start:
                        f.write('A')
                    elif (r,c) == self.goal:
                        f.write('B')
                    elif (r,c) in [node.state for node in list(self.explored)]:
                        f.write('|')
                    elif (r,c) in self.walls:
                        f.write('#')
                    else:
                        f.write(' ')
                
                f.write('\n')
            
            f.write(f'\nTotal Explored States: {len(self.explored)}')


myMaze = Maze('maze3.txt')
myMaze.solve()