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

  To run for the tinymaze using the DFS seacrch algorithm
  python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs


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

  To run for the tinymaze using the BFS seacrch algorithm
  python pacman.py -l tinyMaze -p SearchAgent -a fn=bfs

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
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
