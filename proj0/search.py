# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from util import *

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # position = problem.getStartState()
    # stack = Stack()
    # result = []
    # visited = set()
    # visited.add(position)
    #
    # while not problem.isGoalState(position):
    #     successors = problem.getSuccessors(position)
    #     flag = 0
    #     for i in range(len(successors)):
    #         if successors[i][0] in visited:
    #             flag += 1
    #         else:
    #             stack.push(position)
    #             position = successors[i][0]
    #             result.append(successors[i][1])
    #             visited.add(position)
    #             break
    #         if flag == len(successors):
    #             position = stack.pop()
    #             result.pop()
    # return result

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs

    position = problem.getStartState()
    startposition = position
    queue = Queue()
    result = []
    way = []
    visited = set()
    visited.add(position)

    # move forward
    while not problem.isGoalState(position):
        successors = problem.getSuccessors(position)
        for i in range(len(successors)):
            if successors[i][0] not in visited:
                queue.push(successors[i][0])
                result.append((successors[i][0], successors[i][1], position))
                visited.add(successors[i][0])
        position = queue.pop()
        visited.add(position)
    while position != startposition:
        for tmp in result:
            if tmp[0] == position:
                way.append(tmp[1])
                position = tmp[2]
    way.reverse()
    return way

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    prioqueue = PriorityQueue()
    position = problem.getStartState()
    startposition = position
    visited = set()
    visited.add(startposition)
    result = []
    way = []
    value = 0
    path = PriorityQueue()

    while not problem.isGoalState(position):
        successor = problem.getSuccessors(position)
        for i in range(len(successor)):
            if successor[i][0] not in visited:
                cost = successor[i][2] + value
                prioqueue.update((successor[i][0], cost), cost)
                result.append((successor[i][0], successor[i][1], position, cost))
        temp = prioqueue.pop()
        if temp[0] in visited:
            temp = prioqueue.pop()
        position = temp[0]
        value = temp[1]
        visited.add(position)
    while position != startposition:
        for tmp in result:
            if tmp[0] == position:
                path.push((tmp[1], tmp[2]), tmp[3])
        temp = path.pop()
        way.append(temp[0])
        position = temp[1]
    way.reverse()
    return way

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # prioqueue = PriorityQueue()
    # position = problem.getStartState()
    # startposition = position
    # visited = set()
    # visited.add(startposition)
    # result = []
    # way = []
    # value = 0
    # path = PriorityQueue()
    #
    # while not problem.isGoalState(position):
    #     successor = problem.getSuccessors(position)
    #     for i in range(len(successor)):
    #         if successor[i][0] not in visited:
    #             cost1 = successor[i][2] + value
    #             cost2 = cost1 + heuristic(successor[i][0], problem)
    #             prioqueue.update((successor[i][0], cost1), cost2)
    #             result.append((successor[i][0], successor[i][1], position, cost2))
    #     temp = prioqueue.pop()
    #     if temp[0] in visited:
    #         temp = prioqueue.pop()
    #     position = temp[0]
    #     value = temp[1]
    #     visited.add(position)
    # while position != startposition:
    #     for tmp in result:
    #         if tmp[0] == position:
    #             path.push((tmp[1], tmp[2]), tmp[3])
    #     temp = path.pop()
    #     way.append(temp[0])
    #     position = temp[1]
    # way.reverse()
    # return way
    fringe= PriorityQueue()
    path=[]                             #加一个going to visit？
    closed=[]
    fringe.push(((problem.getStartState(),"Stop",0),path,0),0)      #((successors,path,total_cost),cost)
    while not fringe.isEmpty():
    #for i in range(10):
       # print("------------------",i)
        state,newpath,cost=fringe.pop()
        if state[0] not in closed:
            #print("This State:",state)
            #print("Current path",newpath)
            #print("&&&&&&&&&&&&&&&&&&&&&&&&&&& ")
            closed.append(state[0])                         #state = ((x,y),"direction",cost)
            if problem.isGoalState(state[0]):
                path=newpath
                return path
            else:
                successors=problem.getSuccessors(state[0])
                for successor in successors:
                    if successor[0] not in closed:
                        successorPath=newpath[:] #****************不能直接 a=b， 指向同一个内存，会同时修改两个
                        successorPath.append(successor[1])
                        fringe.push((successor,successorPath,successor[2]+cost),cost+successor[2]+heuristic(successor[0],problem))
                        #print("Cost",successor[2])
    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
