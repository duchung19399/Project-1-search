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

import util

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
    return  [s, s, w, s, w, w, s, w]

class Node: #tạo 1 linklist node
    def __init__(self, state, pred, action, priority=0):
        self.state = state #vị trí node
        self.pred = pred #node trc do liên kết với nó
        self.action = action #node có thể đi qua từ node trước đó
        self.priority = priority
    def __repr__(self):
        return "State: {0}, Action: {1}".format(self.state, self.action)

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
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    passed = set() #tạo set lưu danh sách các ô đã đi qua
    fringe = util.Stack() #tạo stack lưu ô rìa của các tuyến đường đã qua
    #các ô được lưu vào stack nên sẽ tìm theo 1 đưòng đến khi không còn đường cụt quay lại điểm trước đó có thể rẽ
    fringe.push(Node(problem.getStartState(), None, None)) #thêm điểm bắt đầu là vị trí xuất phát của pacman
    while fringe.isEmpty() is not True:
        node = fringe.pop() #láy lần lượt các node trong fringe ra đến khí không còn
        
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None: #láy lần lượt các node từ dich đến di ngược vè điểm đầu, thêm action vào list
                actions.append(node.action)
                node = node.pred
            actions.reverse() #dảo ngược list để có kết quả chính xác
            return actions
        
        if node.state not in passed:#nếu node chưa đi qua bh thì đánh dấu là đã đi qua và thêm các node bên cạnh nó vào fringe
            passed.add(node.state)
            for s in problem.getSuccessors(node.state): #hàm getSuccessor xem tại searchAgent class PositionSearchProblem 
                fringe.push(Node(s[0], node, s[1])) #s[0] vị trí kế tiếp, node là vị trí trước đó, s[1] là hành động cần thược hiện để đi đến s[0] từ node
    return list() #trả về list rỗng nếu không tìm được đường đến food

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #tương tự DFS nhưng thay Stack bằng queue
    passed = set()
    fringe = util.Queue()
    fringe.push(Node(problem.getStartState(), None, None))
    while fringe.isEmpty() is not True:
        node = fringe.pop()
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions
        if node.state not in passed:
            passed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1]))
    return list()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    passed = set()
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState(), None, None), 0)
    while fringe.isEmpty() is not True:
        node = fringe.pop()
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions
        if node.state not in passed:
            passed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1], s[2]+node.priority),\
                            s[2]+node.priority)
    return list()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    passed = set()
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState(), None, None,\
                heuristic(problem.getStartState(), problem)),\
                heuristic(problem.getStartState(), problem))
    while fringe.isEmpty() is not True:
        node = fringe.pop()
        if problem.isGoalState(node.state) is True:
            actions = list()
            while node.action is not None:
                actions.append(node.action)
                node = node.pred
            actions.reverse()
            return actions
        if node.state not in passed:
            passed.add(node.state)
            for s in problem.getSuccessors(node.state):
                fringe.push(Node(s[0], node, s[1], s[2]+node.priority),\
                            s[2]+node.priority+\
                            heuristic(s[0], problem))
    return list()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
