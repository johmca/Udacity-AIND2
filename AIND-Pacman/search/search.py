# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

  Here is the algorithm psuedocode.....

  function GRAPH-SEARCH(problem) returns a solution or failure
    initialise the frontier using the initial state of the problem
    initialise the explored set to be empty
    loop do
        if the frontier is empty return failure
        choose a leaf node and remove it from the frontier
        if the node contains a goal state then return the corresponding solution
        add the node to the explored set
        expand the chosen node, adding the result nodes to the frontier only if
           not already in the frontier or the explored set

  The frontier will be implemented as a utility.stack which is a LIFO queue
  The explored set will he implemented as a set
  To expand a node execute - problem.getSuccessors(state)
  To check if a node contains a goal state -  problem.isGoalState(state)
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())

    Run as follows
  python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs
  python pacman.py -l bigMaze -p SearchAgent -a fn=dfs -z .5


  """
  "*** YOUR CODE HERE ***"

  print('Running DFS routine..')


  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH



  #Create the frontier as an instance of stack
  frontier = util.Stack()

  #Create the explored area as a set
  explored = set()

  #Add start state and path (root) to frontier

  frontier.push((problem.getStartState(),[]))

  #Loop through the frontier
  #  Select the node from the top of the queue (this will be the latest one to have been added as stack is LIFO) which
  #  means we keep going deeper (Depth first)
  #  Does the node under consider contain the goal state - if so return the path to this state
  #  if not then proceed to add the state to the explored set
  #  expand the state of the node under consideration
  #  Add the successor states of node under consideration to the frontier (left to right - left will be explored first
  #  as processing in LIFO sequence)
  while not frontier.isEmpty():
      stateUnderConsideration, stateUnderConsiderationPath = frontier.pop()
      print('State under consideration:', stateUnderConsideration, stateUnderConsiderationPath)
      if problem.isGoalState(stateUnderConsideration):
          print('Yippeee we gfound the goal state ad the directions are:', stateUnderConsiderationPath)
          return(stateUnderConsiderationPath)
          #return(West,West,West,West,South,South,East,South,South,West)
          #return [w,w,w,w,s,s,e,s,s,w]
      explored.add(stateUnderConsideration)
      successorStates = problem.getSuccessors(stateUnderConsideration)
      print('Successor states=', successorStates)
      for each in successorStates: #loop round each successor state adding node to frontier
          state = each[0]
          path = stateUnderConsiderationPath + [each[1]]

          if state not in explored:
              print('Adding node to frontier State=', state, 'Path=', path)
              frontier.push((state,path))

    #Should only reach here if frontier was empty so return failure
  return []
  #util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]

   Here is the algorithm psuedocode.....

  function BREADTH-FIRST-SEARCH(problem) returns a solution or failure
    Iinitialise initial node = (problem.INITIAL_STATE, PATH =[])
    initialise the frontier with initial node as the only element
    initialise the explored set to be empty
    loop do
        if the frontier is empty return failure
        choose a leaf node and remove (pop) it from the frontier
        add the node.STATE to the explored set
        cildren = expand the chosen node into an array of children (state, action, cost)
        for each child in children
        if the child.STATE is not in explored set and not in frontier
           calculate PATH_TO_CHILD = PATH_TO_PARENT + child.ACTION
           if problem.GOAL_TEST(child.STATE) then RETURN(PATH_TO_CHILD)
           add child node (child_state, path_to_child)to frontier

  The frontier will be implemented as a utility.queue which is a FIFO queue
  The explored set will he implemented as a set
  To expand a node execute - problem.getSuccessors(state) - returns a list of children in form (state, action, cost)
  To check if a node contains a goal state -  problem.isGoalState(state)

  Run as follows
  python pacman.py -l tinyMaze -p SearchAgent -a fn=bfs
  python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
  python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5


  """
  "*** YOUR CODE HERE ***"
  print('Running BFS routine..')

  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH

  # Create the frontier as an instance of queue class (FIFO queue)
  frontier = util.Queue()

  # Create the explored area as a set
  explored = set()

  # Add start state and path (root) to frontier

  frontier.push((problem.getStartState(), []))

  # Loop through the frontier
  #  Select the node from the top of the queue (this will be the first one to have been added as stack is FIFO) which
  #  means we go wider then  deeper (breadth first)
  #  Add the state to the explored set
  #  expand the state of the node under consideration
  #  loop round the children of the node under consideration
  #     if the child is the goal state return the path to the child
  #     if the child is not in the explored set or the frontier add the child to the frontier
  while not frontier.isEmpty():
      stateUnderConsideration, stateUnderConsiderationPath = frontier.pop()
      print('State under consideration:', stateUnderConsideration, stateUnderConsiderationPath)
      explored.add(stateUnderConsideration)
      successorStates = problem.getSuccessors(stateUnderConsideration)
      print('Successor states=', successorStates)
      for each in successorStates: #loop round each successor state adding node to frontier
          state = each[0]
          path = stateUnderConsiderationPath + [each[1]]
          if state not in explored:
              #In BFS check is state is a goal state as we add to frontier to avoid unecessary iterations
              if problem.isGoalState(state):
                  print('Yippeee we found the goal state', state, 'and the directions are:', path)
                  return (path)
              print('Adding state to frontier ',state,' with path',path)
              frontier.push((state,path))
  #util.raiseNotDefined()
      
def uniformCostSearch(problem):
  """Search the node of least total cost first.

  Pseudo code  from text book fig 3:14 p84....

  function UNIFORM-COST-SEARCH(problem) returns a solution or failure

  set initial_node = new node with node.STATE = problem.INITIAL-STATE, node.PATH = [], node.PATH-COST=0
  set frontier = new priority queue ordered by PATH-COST with first element = initial_node
  set explored = empty set
  loop do
    if frontier is empty then return failure
    set current_node =POP(frontier) i.e. node with lowest cost from frontier is selected
    if problem.GOAL_TEST(current_node.STATE) is True then return current_node.PATH
    add current_node.STATE to explored set
    successors = Expand successors of current_node.STATE
    for successor in successors
        if successor.STATE is not in explored set and is not in frontier
            add successor to frontier with (state, path, cummulative cost)
        elseif  successor.STATE is in frontier but has higher path cost
            replace the existing node in frontier with the sucessor node


  """
  "*** YOUR CODE HERE ***"
  print('Running Uniform Cost Search routine..')

  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH

  # Create the frontier as an instance of priority queue class (ordered by path cost - lowest at top)
  frontier = util.PriorityQueue()

  # Create the explored area as a set
  explored = set()

  # Add inital node (start state, empty path) and initial path cost of 0  to queue - cost acts the priority for this queue
  frontier.push ((problem.getStartState(), []),0)
  #Some tests
  # frontier.push (((1,1), ['West']), 661)
  # item  = frontier.pop()
  # print('Look who popped off first.....')
  # print('First popping item=', item)
  # print('First popping item state=', item[0])
  # print('First popping item path=', item[1])


  # Loop through the frontier
  #  Select the node from the top of the queue (tFhis will be the one with lowest cost first)
  #  Add the state to the explored set
  #  expand the state of the node under consideration
  #  loop round the children of the node under consideration
  #     if the child is the goal state return the path to the child
  #     if the child is not in the explored set or the frontier add the child to the frontier
  while not frontier.isEmpty():
      item = frontier.pop() #Lowest cost node is retrieved from frontier
      #itemUnderConsideration, itemUnderConsiderationPathCost = frontier.pop()
      itemUnderConsiderationState = item[0]
      itemUnderConsiderationPath = item[1]
      print('Node under consideration:', itemUnderConsiderationState, itemUnderConsiderationPath)

      # If node under consideration contains goal state stop search and return path
      if problem.isGoalState(itemUnderConsiderationState):
          print('Yippeee we found the goal state', itemUnderConsiderationState, 'and the directions are:', itemUnderConsiderationPath)
          return (itemUnderConsiderationPath)

      # Add state of selected node to explored set
      explored.add(itemUnderConsiderationState)

      # Expand selected node's state to find sucessors
      print('Finding successor state for ',itemUnderConsiderationState)
      successorStates = problem.getSuccessors(itemUnderConsiderationState) #Returns (state,action,total path cost)
      print('Successor states=', successorStates)

      # loop round each successor state adding it as a node ((state,path),path_cost) to frontier
      for successor in successorStates:
          successorState = successor[0]
          successorAction = successor[1]
          successorPathCost = successor[2]
          print('Processing Sucessor state=',successorState,'Action=',successorAction,'Action Cost=',successorPathCost)
          print('itemunderconsiderationpath',itemUnderConsiderationPath)
          print('successorAction',successorAction)

          successorPath = itemUnderConsiderationPath[:] #Python 2 syntax to copy a list; don't use = as the new list is the old list(copies reference)
          successorPath.append(successorAction)
          print('succesor path',successorPath)
          #Calculate path cost by passing path to get cost function - important to note that this function makes a call
          #to an overridden heuristic (defauts to return 1 but will accept an override from comamnd line)
          successorPathCost = problem.getCostOfActions(successorPath)
          #Ignore sucessor state if already explored. If not already exlored add to frontier.
          if  successorState not in explored:
              print('Adding Sucessor node to frontier. State=', successorState, ', Path=', successorPath, ', Path Cost=', successorPathCost)
              frontier.push((successorState, successorPath),successorPathCost)

  #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial and returns 0.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  """

  A* Search uses a cost function which combines actual cost and esimated cost I.E. f(n) + h(n) where f(n) is the actual
  cost incurred to reach node n and h(n) is a heuristic function giving the estimated costs to get from node n to the
  goal state. h(s) must be an unerestimate for A* to work e.g. the straigt line distance from a town to another is
  admissable as it underestimates the distance. A* search algorithm is identical to UCS except for the cost function
  used.

  Search the node that has the lowest combined cost and heuristic first.

  Implement A* graph search in the empty function aStarSearch in search.py.
  A* takes a heuristic function as an argument. Heuristics take two arguments: a state in the search problem (the main
  argument), and the problem itself (for reference information). The nullHeuristic heuristic function in search.py is a
  trivial example.   You can test your A* implementation on the original problem of finding a path through a maze to a
  fixed position using the Manhattan distance heuristic (implemented already as manhattanHeuristic in searchAgents.py).

 python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

  This function accepts arguments
  i)    problem - an object containign the definition of the problem and relevant methods
  ii)   heuristic function - the function to be used to estimate the cost remaining to the goal state (defualts to
         nullHeuristic)

  This function returns a path of actions leading from the start state to the goal state as a python list.


  """
  "*** YOUR CODE HERE ***"
  print('Running A* search routine..')
  print('Heuristic in use is',heuristic)

  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH

  # Create the frontier as an instance of priority queue class (ordered by path cost - lowest at top)
  frontier = util.PriorityQueue()

  # Create the explored area as a set
  explored = set()

  # Add inital node (start state, empty path) and initial path cost of 0  to queue - cost acts the priority for this queue
  actualPathCost = 0
  estimatedRemainingPathCost = heuristic(problem.getStartState(), problem)
  estimatedTotalPathCost = actualPathCost + estimatedRemainingPathCost

  frontier.push((problem.getStartState(), []), estimatedTotalPathCost )
  # Some tests
  # frontier.push (((1,1), ['West']), 661)
  # item  = frontier.pop()
  # print('Look who popped off first.....')
  # print('First popping item=', item)
  # print('First popping item state=', item[0])
  # print('First popping item path=', item[1])


  # Loop through the frontier
  #  Select the node from the top of the queue (tFhis will be the one with lowest cost first)
  #  Add the state to the explored set
  #  expand the state of the node under consideration
  #  loop round the children of the node under consideration
  #     if the child is the goal state return the path to the child
  #     if the child is not in the explored set or the frontier add the child to the frontier
  while not frontier.isEmpty():
      item = frontier.pop()  # Lowest cost node is retrieved from frontier
      # itemUnderConsideration, itemUnderConsiderationPathCost = frontier.pop()
      itemUnderConsiderationState = item[0]
      itemUnderConsiderationPath = item[1]
      print('Node under consideration:', itemUnderConsiderationState, itemUnderConsiderationPath)

      # If node under consideration contains goal state stop search and return path
      if problem.isGoalState(itemUnderConsiderationState):
          print('Yippeee we found the goal state', itemUnderConsiderationState, 'and the directions are:',
                itemUnderConsiderationPath)
          return (itemUnderConsiderationPath)

      # Add state of selected node to explored set
      explored.add(itemUnderConsiderationState)

      # Expand selected node's state to find sucessors
      print('Finding successor state for ', itemUnderConsiderationState)
      successorStates = problem.getSuccessors(itemUnderConsiderationState)  # Returns (state,action,total path cost)
      print('Successor states=', successorStates)

      # loop round each successor state adding it as a node ((state,path),path_cost) to frontier
      for successor in successorStates:
          successorState = successor[0]
          successorAction = successor[1]
          successorPathCost = successor[2]
          print(
          'Processing Sucessor state=', successorState, 'Action=', successorAction, 'Action Cost=', successorPathCost)
          print('itemunderconsiderationpath', itemUnderConsiderationPath)
          print('successorAction', successorAction)

          successorPath = itemUnderConsiderationPath[
                          :]  # Python 2 syntax to copy a list; don't use = as the new list is the old list(copies reference)
          successorPath.append(successorAction)
          print('succesor path', successorPath)
          # Calculate path cost by passing path to get cost function - important to note that this function makes a call
          # to an overridden heuristic (defauts to return 1 but will accept an override from comamnd line)
          successorPathCost = problem.getCostOfActions(successorPath)
          # Ignore sucessor state if already explored. If not already exlored add to frontier.
          if successorState not in explored:
              # Add inital node (start state, empty path) and initial path cost of 0  to queue - cost acts the priority for this queue
              estimatedRemainingPathCost = heuristic(successorState, problem)
              estimatedTotalPathCost = successorPathCost + estimatedRemainingPathCost

              print(
              'Adding Sucessor node to frontier. State=', successorState, ', Path=', successorPath, ', Path Cost=',
              estimatedTotalPathCost)
              frontier.push((successorState, successorPath), estimatedTotalPathCost)

  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
