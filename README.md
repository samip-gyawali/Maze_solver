# General Working for each algorithm:

## The `Node` class:
- Each node is a part of the graph used for solving a **search problem**.
- A node stores basic data about the graph such as:
    - State of the node
    - Parent of the node (Node before it)
    - Action (action taken from the parent node to get to this node)

## The `Frontier` class:
- Defines the data structure and working of the Frontier.
- Frontier is a data structure that stores all of the nodes from the current node that can be expanded further (or explored).
- At the fundamental level, the data structure of the `Frontier` differentiates one algorithm from another.

## The `Maze` Class:
- Constructor takes in `fileName` as a parameter. The file contains the unsolved maze.
- The height and width of the maze is stored in `Maze.height` and `Maze.width` respectively.
- The position of start and end of the maze is stored in `Maze.start` and `Maze.goal`.
- The `Maze.solution` stores a list of coordinates which give path from A to B.
- The `Maze.walls` stores a list of coordinates which are walls.
- The `Maze.explored` is a set that stores coordinates of all the explored states by the agent.

### `Maze.__isValid()` module:
- Takes a state (or position of the agent) as a parameter and returns if the move is valid based on multiple comparisons.

### `Maze.__isGoal()` module:
- Takes a state (or position of the agent) as a parameter and returns if the state is the goal state (a goal check).

### `Maze.solve()` modukeL
- Creates a node of the start state and sets its `parent` and `action` to `None` and adds it to the frontier.
- The `solved` variable is a boolean which indicates if the maze is solved.
- A loop begins until the maze is solved or the `frontier` is empty (in which case, maze has no solution).
- A node is removed from the frontier--the data structure or logic of the frontier determines which node is removed.
- The node is added to `Maze.explored` set.
- The node's state is checked against the goal state (using the `Maze.__isGoal()` module).
- If it is, `solved` is set to `True` and the loop ends as we've found the solution.
- If not, the possible moves from the currentNode are checked (only left, right, up or down are allowed and no diagonals)
- Using the `Maze.__isValid()` module, it is checked which of the possible moves yields a valid state.
- Those states are added to the frontier.

### `Maze.__showSolution()` module:
- It turns the `Maze.explored` set into a list and checks the index of the goal state in it, which is the beginning node for the loop.
- A loop starts until the parent of the current node is `None` (which is True for the start state. So the loop continues until we find the start state).
- The state for each current node is added to the `Maze.solution` list. (as it gives the path from B to A which is reverse of the solution).
- The next node is the parent of the current node.
- Once the loop completes `Maze.solution` contains a list of states (or coordinates for ease) that was used to get from A to B.
- The solved maze is created in the `<ALGORITHM>/<MAZE>/solution.txt` file.


# BFS vs DFS:
- Breadth-First Search (BFS) implements the Queue Data Structure (where the first node added to the frontier is removed first).
- Depth-First Search (DFS) implements the Stack Data Structure (where the last node added to the frontier is removed first).
- When encountered with a fork (or a choice), BFS goes back and forth between both choices, while DFS chooses a path and explores it completely until finding the goal or reaching a dead end (in which case it takes the another path).
- BFS is guarenteed to find the optimal path but will likely explore more states than needed. DFS is more efficient but isn't guarenteed to find the optimal path (as shown in maze 3).

# GBFS and A* search:
- Greedy Best First Search (GBFS) and A* search algorithms are more *intelligent* than BFS and DFS.

## Greedy Best First Search (GBFS):
- GBFS uses a Heuristic function (here the **Manhattan Distance**) to estimate the distance (path cost) from the current node to the goal and chooses the path with least value of the heuristic when encountered with a choice.
- In program, this is implemented by adding a `heuristic` property to the `Node`, where heuristic is calculated using the **Manhattan Distance**
-  A node is added to the frontier based on heuristic (where node with the lowest heuristic is added to front of the frontier).
- When removing a node from the frontier, the node in the beginning of the frontier is removed first.

## A* Search:
- Is more *intelligent* than GBFS. Rather than only using the heuristic, this chooses a node based on the sum of heuristic and distance travelled from the start node.
- In practice, we add another property, `steps` to the node where steps stores the steps from start node taken.
- For the start node (`parent = None`) the step is zero. And for each consecutive node, the step is the steps of the parent node + 1.
- Another property `totalEstimate` sums the heuristic and the `steps` and when a new node is added to the `Frontier`, its position is determined from the `totalEstimate` (where lower the `totalEstimate` more front in the `frontier` is the node).
- When removing a node from the frontier, the node in the beginning of the frontier is removed first.