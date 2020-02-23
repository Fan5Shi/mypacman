# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # print("successorGameState : ")
        # print(successorGameState)
        newPos = successorGameState.getPacmanPosition()
        # print("newPos: ")
        # print(newPos)
        newFood = successorGameState.getFood()  # newFood has the function asList()
        # print("newFood: ")
        # print(newFood)
        newGhostStates = successorGameState.getGhostStates()
        # print("newGhostStates: ")
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        # print("newScaredTimes: ")
        # print(newScaredTimes)

        newCapsule = successorGameState.getCapsules()
        "*** YOUR CODE HERE ***"

        foods = newFood.asList()
        foodsNum = len(foods)
        foodmax = 0
        if foodsNum > 0:
            foodmax = util.manhattanDistance(newPos, foods[0])
        foodWeight = 0
        # scores = 0
        # print("scores: " + str(scores))

        for food in foods:
            dist = util.manhattanDistance(newPos, food)
            if dist < foodmax:
                foodmax = dist

        if foodmax > 0:
            foodWeight = 1.0 / foodmax

        # print("foodweight:",foodWeight)

        # print("min: " + str(minScore))
        min = util.manhattanDistance(newPos, newGhostStates[0].getPosition())
        for temp in newScaredTimes:
            if temp > 0:
                min = -util.manhattanDistance(newPos, newGhostStates[0].getPosition())
            else:
                min = util.manhattanDistance(newPos, newGhostStates[0].getPosition())

        minScore = 0
        if min > 0:
            minScore = -1.0 / min

        # scores = scores - foodsNum ** 2 + min - foodmax
        scores = successorGameState.getScore() + foodWeight + minScore
        # print("final scores: " + str(scores))
        # print("----------------------")
        return scores

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        scores = dict()
        for action in actions:
            temp = gameState.generateSuccessor(0, action)
            scores[action] = self.myValue(temp, 0, 1)
        return max(scores, key=scores.get)

    def myValue(self, gameState, cDepth, index):
        if self.depth == cDepth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif index == 0:
            return self.maxvalue(gameState, cDepth)
        else:
            return self.minvalue(gameState, cDepth, index)

    def maxvalue(self, state, cDepth):
        v = -100000
        array1 = []
        for action in state.getLegalActions(0):
            array1.append(state.generateSuccessor(0, action))
        for suc in array1:
            v = max(v, self.myValue(suc, cDepth, 1))
        # print("max: " + str(v))
        return v

    def minvalue(self, state, cDepth, index):
        v = 100000
        # array2 = []
        # for action in state.getLegalActions(index):
        #     array2.append(state.generateSuccessor(index, action))
        # for suc in array2:
        #     if index == state.getNumAgents() - 1:
        #         depth = cDepth + 1
        #         v = min(v, self.myValue(suc, depth, 0))
        #     else:
        #         index += 1
        #         v = min(v, self.myValue(suc, cDepth, index))
        # print("min: " + str(v))
        # return v
        for action in state.getLegalActions(index):
            if index == state.getNumAgents() - 1:
                v = min(v, self.myValue(state.generateSuccessor(index, action), cDepth + 1, 0))
            else:
                v = min(v, self.myValue(state.generateSuccessor(index, action), cDepth, index + 1))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        scores = dict()
        alpha = float("-inf")
        beta = float("inf")
        for action in actions:
            temp = gameState.generateSuccessor(0, action)
            scores[action] = self.myValue(temp, 0, 1, alpha, beta)
            alpha = max(alpha, max(scores.values()))
        return max(scores, key=scores.get)

    def myValue(self, gameState, cDepth, index, alpha, beta):
        if self.depth == cDepth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif index == 0:
            return self.maxvalue(gameState, cDepth, alpha, beta)
        else:
            return self.minvalue(gameState, cDepth, index, alpha, beta)

    def maxvalue(self, state, cDepth, alpha, beta):
        v = -100000
        # change the code from minimax
        for action in state.getLegalActions(0):
            suc = state.generateSuccessor(0, action)
            v = max(v, self.myValue(suc, cDepth, 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def minvalue(self, state, cDepth, index, alpha, beta):
        v = 100000
        for action in state.getLegalActions(index):
            if index == state.getNumAgents() - 1:
                v = min(v, self.myValue(state.generateSuccessor(index, action), cDepth + 1, 0, alpha, beta))
            else:
                v = min(v, self.myValue(state.generateSuccessor(index, action), cDepth, index + 1, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        scores = dict()
        for action in actions:
            temp = gameState.generateSuccessor(0, action)
            scores[action] = self.myValue(temp, 0, 1)
        return max(scores, key=scores.get)

    def myValue(self, gameState, cDepth, index):
        if self.depth == cDepth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif index == 0:
            return self.maxvalue(gameState, cDepth)
        else:
            return self.exp_value(gameState, cDepth, index)

    def maxvalue(self, state, cDepth):
        v = -100000
        array1 = []
        for action in state.getLegalActions(0):
            array1.append(state.generateSuccessor(0, action))
        for suc in array1:
            v = max(v, self.myValue(suc, cDepth, 1))
        return v

    def exp_value(self, state, cDepth, index):
        v = 0
        actions = state.getLegalActions(index)
        for action in actions:
            if index == state.getNumAgents() - 1:
                v += self.myValue(state.generateSuccessor(index, action), cDepth + 1, 0)
            else:
                v += self.myValue(state.generateSuccessor(index, action), cDepth, index + 1)
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # "*** YOUR CODE HERE ***"
    # newPos = currentGameState.getPacmanPosition()
    # newFood = currentGameState.getFood()  # newFood has the function asList()
    # newGhostStates = currentGameState.getGhostStates()
    # newCapsules = currentGameState.getCapsules()
    # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #
    # "*** YOUR CODE HERE ***"
    # foods = newFood.asList()
    # foodsNum = len(foods)
    # min = 10000
    # minCap = 10000
    # minfood = 10000
    # scores = currentGameState.getScore()
    # foodWeight = foodsNum
    # # print("foodWeight: " + str(foodWeight))
    # ghostWeight = 0
    # distcap = 0
    # timetemp = 0
    #
    # for food in foods:
    #     dist = util.manhattanDistance(newPos, food)
    #     if dist < minfood:
    #         minfood = dist
    #
    # if len(newCapsules) == 1:
    #     for cap in newCapsules:
    #         minCap = util.manhattanDistance(newPos, cap)
    # elif len(newCapsules) > 1:
    #     for cap in newCapsules:
    #         dist = util.manhattanDistance(newPos, cap)
    #         if minCap > dist:
    #             minCap = dist
    # distcap += 2 * minCap
    # # print("distcap: " + str(distcap))
    #
    # for ghost in newGhostStates:
    #     dist = util.manhattanDistance(newPos, ghost.getPosition())
    #     if dist < min:
    #         min = dist
    # ghostWeight += min
    #
    # for temp in newScaredTimes:
    #     timetemp = temp
    #     if temp > 0:
    #         # print("!!!!!!!!!!!!!!!!!!!")
    #         ghostWeight = 0.1 * ghostWeight
    #
    # # print("ghostWeight: " + str(ghostWeight))
    #
    # scores = scores - foodWeight - distcap + ghostWeight ** (2) + timetemp
    # # print("final scores: " + str(scores))
    # # print("-------------------------------")
    # return scores

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()  # newFood has the function asList()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newCapsule = currentGameState.getCapsules()

    foods = newFood.asList()
    foodsNum = len(foods)
    foodmax = 0
    capmin = 0
    foodWeight = 0
    capWeight = 0

    if len(newCapsule) > 0:
        capmin = util.manhattanDistance(newPos, newCapsule[0])

    if foodsNum > 0:
        foodmax = util.manhattanDistance(newPos, foods[0])


    for food in foods:
        dist = util.manhattanDistance(newPos, food)
        if dist < foodmax:
            foodmax = dist

    if foodmax > 0:
        foodWeight = 1.0 / foodmax

    for cap in newCapsule:
        dist = util.manhattanDistance(newPos, cap)
        if dist < capmin:
            capmin = dist

    if capmin > 0:
        capWeight = 50.0 / capmin

    min = util.manhattanDistance(newPos, newGhostStates[0].getPosition())
    for temp in newScaredTimes:
        if temp > 0:
            # print("temp: " + str(temp))
            # return 100000
            # return currentGameState.getScore() + foodWeight
            min = -util.manhattanDistance(newPos, newGhostStates[0].getPosition())
        # elif temp > 0:
            # print("temp: " + str(temp))
            # return 100000
            # return currentGameState.getScore() + foodWeight
        else:
            min = util.manhattanDistance(newPos, newGhostStates[0].getPosition())

    minScore = 0
    if min > 0:
        minScore = -1000.0 / min

    scores = currentGameState.getScore() + foodWeight + minScore + capWeight
    return scores

# Abbreviation
better = betterEvaluationFunction
