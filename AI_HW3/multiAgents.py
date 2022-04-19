from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

INF = 999999999
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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    '''
    Your minimax agent (Part 1)
    '''
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)

        def countmax(depth,gameState,index_agent):
            '''
            depth means the depth this state in.
            gameState means the state that is going to be execute this time.
            index_agent means the index of the agent, 
            pacman is 0, ghosts are 1~num_agents-1
            countmax will return the bestscore and bestmove
            bestscore is either min/max score in ghost/pacman.
            bestmove is only matters when it comes to pacman(index_agent=0)
            '''
            num_agents = gameState.getNumAgents() #number of agents 
            legalMoves = gameState.getLegalActions(index_agent)#legal moves of the executing state
            if len(legalMoves)==0:#done with game at the state(either win or lose)
                return self.evaluationFunction(gameState),"0" #return the points

            #In each condition, scores means all the scores of childstates
            #Take all posibile childstates from legalmove and count the min/max of it.           
            if depth ==1 and index_agent == num_agents-1:
                '''
                depth =1 and index = num_agents-1 means it is the terminal state.
                It is also the leaf process of the recursion function call.
                take scores from self.evaluationFunction easily, since it's the terminal state.
                return bestScore, which is the minimum score of all posible scores.
                '''
                scores = []
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(self.evaluationFunction(GameState))
                bestScore=min(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return bestScore,legalMoves[chosenIndex]
            elif index_agent==0:
                '''
                index_agent=0 means it is the time when pacman(max_player)'s time.
                countmax(depth,Gamestate,1) is used because I start from the ghost with index 1.
                return bestScore(max score of scores) 
                and 
                bestMove(which matters because the original get_action function relies on it)
                '''
                scores = []
                for action in legalMoves:
                    GameState = gameState.getNextState(0,action)
                    scores.append(countmax(depth,GameState,1))
                bestScore = max(scores)[0]
                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return bestScore,legalMoves[chosenIndex]
            elif index_agent == num_agents-1:
                '''
                index_agent=num_agents-1 but depth not equal to 1 means the childstate is pacman in the next depth.
                Therefore, countmax(depth-1,Gamestate,0) is used instead of countmax(depth,Gamestate,index_agent+1)
                return bestScore, which is the minimum of scores.
                '''
                scores=[]
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(countmax(depth-1,GameState,0))
                bestScore = min(scores)[0]
                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return bestScore,legalMoves[chosenIndex]
            else:
                '''
                Those 0<index_agent<num_agent-1 (no matter depth is 1 or not) would be execute here.
                countmax(depth,Gamestate,index_agent+1) is used since there is no need to change depth,
                and the next agent to be executed is index_agent+1.
                '''
                scores=[]
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(countmax(depth,GameState,index_agent+1))
                bestScore = min(scores)[0]
                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = random.choice(bestIndices)
                return bestScore,legalMoves[chosenIndex]

        # Take the best move from function countmax(recursively)
        bestScore,bestmove = countmax(self.depth,gameState,0)
        
        return bestmove
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """
    

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        def countmax(depth,gameState,index_agent,alpha_beta):
            #alpha_beta[0] means alpha
            #alpha_beta[1] means beta
            num_agents = gameState.getNumAgents()
            legalMoves = gameState.getLegalActions(index_agent)
            if len(legalMoves)==0:
                return self.evaluationFunction(gameState),"0"
            if depth ==1 and index_agent == num_agents-1:
                '''
                this is a min_player, so update beta and prune if bestScore(v) is less than alpha
                the updated alpha_beta list will be changed in the function that call this function,
                because list is mutable.
                '''
                scores = []
                bestScore = INF
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    thisScore = self.evaluationFunction(GameState)
                    scores.append(thisScore)
                    bestScore = min(bestScore,thisScore)
                    if bestScore<alpha_beta[0]:
                        return bestScore, action
                    alpha_beta[1] = min(alpha_beta[1],bestScore)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = bestIndices[-1]
                return bestScore,legalMoves[chosenIndex]

            elif index_agent==0:
                '''
                this is a max_player, so update alpha and prune if bestScore is larger than beta.
                the updated alpha_beta list will be changed in the function that call this function,
                because list is mutable.
                alpha_beta1 is used in order not to chanage the beta's value.
                (since this is a max_player, value of beta shouldn't be changed)
                '''
                scores = []
                bestScore = -INF
                
                for action in legalMoves:
                    GameState = gameState.getNextState(0,action)
                    alpha_beta1 = [alpha_beta[0],alpha_beta[1]]
                    thisScore = countmax(depth,GameState,1,alpha_beta1)
                    scores.append(thisScore)
                    bestScore = max(bestScore,thisScore[0])
                    if bestScore>alpha_beta[1]:
                        return bestScore, action
                    alpha_beta1[0] = max(alpha_beta1[0],bestScore)
                    alpha_beta[0] = alpha_beta1[0]
                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = bestIndices[-1]
                return bestScore,legalMoves[chosenIndex]
            elif index_agent == num_agents-1:
                '''
                this is a min_player, so update beta and prune if bestScore(v) is less than alpha
                the updated alpha_beta list will be changed in the function that call this function,
                because list is mutable.
                '''
                scores=[]
                bestScore = INF
                for action in legalMoves:
                    alpha_beta1 = [alpha_beta[0],alpha_beta[1]]
                    GameState = gameState.getNextState(index_agent,action)
                    
                    thisScore = countmax(depth-1,GameState,0,alpha_beta1)
                    scores.append(thisScore)
                    bestScore = min(bestScore,thisScore[0])
                    if bestScore<alpha_beta[0]:
                        return bestScore, action
                    alpha_beta1[1] = min(alpha_beta1[1],bestScore)
                    alpha_beta[1] = alpha_beta1[1]
                
                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = bestIndices[-1]
                
                return bestScore,legalMoves[chosenIndex]
            else:
                '''
                this is a min_player, so update beta and prune if bestScore(v) is less than alpha
                the updated alpha_beta list will be changed in the function that call this function,
                because list is mutable.
                '''
                scores=[]
                bestScore = INF
                for action in legalMoves:
                    alpha_beta1 = [alpha_beta[0],alpha_beta[1]]
                    GameState = gameState.getNextState(index_agent,action)
                    
                    thisScore = countmax(depth,GameState,index_agent+1,alpha_beta1)
                    scores.append(thisScore)
                    bestScore = min(bestScore,thisScore[0])
                    if bestScore<alpha_beta[0]:
                        return bestScore, action
                    alpha_beta1[1] = min(alpha_beta1[1],bestScore)
                    alpha_beta[1] = alpha_beta1[1]

                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = bestIndices[-1]
                
                return bestScore,legalMoves[chosenIndex]
        #alpha_beta is send as a parameter, which is new from minimax
        bestScore,bestmove = countmax(self.depth,gameState,0,[-INF,INF])
        return bestmove
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """


    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        def countmax(depth,gameState,index_agent):
            num_agents = gameState.getNumAgents()
            legalMoves = gameState.getLegalActions(index_agent)
            if len(legalMoves)==0:
                return self.evaluationFunction(gameState),"0"
            if depth ==1 and index_agent == num_agents-1:
                scores = []
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(self.evaluationFunction(GameState))

                total = 0
                for value in scores:
                    total+=value
                bestScore = total/len(scores)
                '''
                Instead of finding the minimum of the scores,
                find the average score as the best score
                bestmove is not importent here, so just return legalMoves[0] it's ok.
                '''
                return bestScore,legalMoves[0]
            elif index_agent==0:
                scores = []
                for action in legalMoves:
                    GameState = gameState.getNextState(0,action)
                    scores.append(countmax(depth,GameState,1))
                bestScore = max(scores)[0]
                bestIndices = [index for index in range(len(scores)) if scores[index][0] == bestScore]
                chosenIndex = random.choice(bestIndices)
                '''
                the max_player, which is the pacman, remains the same as minimaxAgent
                '''
                return bestScore,legalMoves[chosenIndex]
            elif index_agent == num_agents-1:
                scores=[]
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(countmax(depth-1,GameState,0))
                total = 0
                for value in scores:
                    total+=value[0]
                bestScore = total/len(scores)
                '''
                Instead of finding the minimum of the scores,
                find the average score as the best score
                bestmove is not importent here, so just return legalMoves[0] it's ok.
                '''
                return bestScore,legalMoves[0]
            else:

                scores=[]
                for action in legalMoves:
                    GameState = gameState.getNextState(index_agent,action)
                    scores.append(countmax(depth,GameState,index_agent+1))
                total=0
                for value in scores:
                    total+=value[0]
                bestScore = total/len(scores)
                '''
                Instead of finding the minimum of the scores,
                find the average score as the best score
                bestmove is not importent here, so just return legalMoves[0] it's ok.
                '''
                return bestScore,legalMoves[0]
        
        bestScore,bestmove = countmax(self.depth,gameState,0)
        return bestmove
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    '''
    take the score, position, food, Ghoststates, from currentGameState
    using the function used in the reflexagent.
    '''
    nowScore = currentGameState.getScore()
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    SacredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    #count the minGhostDistance using manhattanDistance, 
    #manhattanDistance is useful since pacman only go top,left,right,or down.
    minGhostDistance = min([manhattanDistance(Pos, state.getPosition()) for state in GhostStates])
    #count nearestfood distances
    FoodsDistances = [manhattanDistance(Pos, food) for food in Food.asList()]
    nearestFoodDistance = 0 if not FoodsDistances else min(FoodsDistances)
    '''
    The evaluationFunction I came up myself.
    1.If there is a ghost that is sacred and near pacman, pacman will chase it
    because I give this situation high points.
    2.If there is a ghost near pacman that is not sacred, give 0 points.
    3.no ghost near pacman and nearestFoodDistance<1: 10points
    4.else 5 points.
    '''
    for i in range(len(GhostStates)):
        if SacredTimes[i]>0 and manhattanDistance(Pos, GhostStates[i].getPosition())<SacredTimes[i]:
            return 300+nowScore
        elif SacredTimes[i]<0 and  manhattanDistance(Pos, GhostStates[i].getPosition())<2:
            return 0+nowScore
    if minGhostDistance<2:
        return 0+nowScore
    elif nearestFoodDistance<1:
        return 10+nowScore
    else:
        return 5+nowScore

    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
