"""Generates a Node for use in searching a maze"""

class Node():
    """
    The node class works in conjunction with the Frontier class to complete search problems
    within the Maze class.

    The node stores a current state, a parent node, the action taken to pass from the state of
    the parent node to the current state, the number of steps taken to reach the current state,
    and, optionally, an estimated cost reach the goal state from the current state.

    :param parent: Parent node
    :type parent: Node
    :param state: Location in maze
    :type param: tuple (int, ...)
    :param action: Action taken to reach node as (dim, action)
    :type action: tuple of (int, str)
    :param steps: Steps to reach node instance
    :type steps: int
    :param cost: Estimated cost to reach goal
    :type cost: int
    """
    def __init__(self, parent=None, state=None, action=None):
        self._parent = parent
        self._state = state
        self._action = action
        if parent:
            self._steps = parent.steps + 1
        else:
            self._steps = 0

    def __str__(self):
        return f"parent={self.parent}\nstate={self.state}\naction={self.action}\n"

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        if not parent:
            raise ValueError("Missing parent")
        self._parent = parent

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if not state:
            raise ValueError("Missing state")
        self._state = state

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        if not action:
            raise ValueError("Missing action")
        self._action = action

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, steps):
        if not steps:
            raise ValueError("Missing steps")
        self._steps = steps

    @property
    def cost(self):
        return self._cost

    @steps.setter
    def cost(self, cost):
        self._cost = cost

    def initialize(self, parent=None, state=None, action=None):
        """
        Initializes the node
        """
        self._parent = parent
        self._state = state
        self._action = action
        if parent:
            self._steps = parent.steps + 1
        else:
            self._steps = 0
        

