"""
Deprecated code -- Updated coded uses mazes.py
"""

import abc
from dimensions import Dimensions
from node import Node
from frontier import BreadthFrontier, Frontier

"""Network stores information to be searched"""
class Network(metaclass=abc.ABCMeta):
    """
    The Network class is an abstract base class meant to provide inheritance to implementation-specific
    search classes. These classes load information to be searched and provide functionality to perform
    the search.
    """
    @abc.abstractmethod
    def load(self, filename=None):
        """
        Load accepts the file name from which to load the information and is implementation dependent.
        """
        pass

    def expand(self, node):
        """
        Expand accepts a node and returns a list of nodes representing valid states reachable from the
        state stored in the given node
        """
        nodes = []
        for action in self._action_set:
            next = self.transition(node, action)
            if next != None:
                nodes.append(next)
        return nodes
    
    @abc.abstractmethod
    def transition(self, node, action):
        """
        Transition determines the state resulting from a current state and action, and returns a node
        representing the state. Transition is implementation specific.
        """
        pass
        
    def goal(self, state):
        """
        Goal tests if the given state is the goal state. If so, return True, else False.
        """
        return state == self.goal

"""Maze stores a text-based maze to find a path from 'start' to 'goal'"""
class Maze(Network):
    """
    The Maze class loads an n-dimensional maze stored as a text file and determines a solution using one
    of several search algorithms.
    """
    def __init__(self, filename=None):
        """
        Initializes an instance of Maze

        :param network: Maze stored as True/False for walls/open space
        :type network: Nested lists of boolean values
        :param open_char: Represents traversable space
        :type open_char: char/str
        :param wall_char: Represents non-tranversable space
        :type wall_char: char/str
        :param start_char: Represents the starting point
        :type start_char: char/str
        :param goal_char: Represents the goal point
        :type goal_char: char/str
        :param state_char: Represents present state
        :type state_char: char/str
        """
        self.network = []
        self._open_char = ' '
        self._wall_char = '#'
        self._start_char = 'A'
        self._goal_char = 'B'
        self._state_char = 'O'
        
        if filename == None:
            self.dimensions = Dimensions()
            self.start = None
            self.goal = None
        else:
            self.load(filename)
        
    def __str__(self):
        string = ""
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) == self.start:
                    string += self._start_char
                elif (i,j) == self.goal:
                    string += self._goal_char
                elif self.network[i][j]:
                    string += self._wall_char
                else:
                    string += self._open_char
            string += '\n'
        return string

    def print(self, big=1):
        string = ""
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                if (i,j) == self.start:
                    row += self._start_char * big
                elif (i,j) == self.goal:
                    row += self._goal_char * big
                elif self.network[i][j]:
                    row += self._wall_char * big
                else:
                    row += self._open_char * big
            row += '\n'
            string += row * big
        return string


    def print_state(self, state, big=1):
        string = ""
        for i in range(self.height):
            row = ''
            for j in range(self.width):
                if (i,j) == self.start:
                    row += self._start_char * big
                elif (i,j) == self.goal:
                    row += self._goal_char * big
                elif (i,j) == state:
                    row += self._state_char * big
                elif self.network[i][j]:
                    row += self._wall_char * big
                else:
                    row += self._open_char * big
            row += '\n'
            string += row * big
        return string

    def load(self, filename):
        """
        Loads a maze from the file named by filename into self.network, loads state of start
        named by 'A', and loads state of goal named by 'B'. Self.network consists of True values
        for walls (any character not 'A', 'B', or whitespace) and False values for traversable
        spaces. Also sets height as the number of lines in the file, and width as the length of
        the longest line.
        """
        with open(filename) as file:
            network = file.read()

        if network.count(self._start_char) != 1:
            raise Exception("Network has no start")

        if network.count(self._goal_char) != 1:
            raise Exception("Network has no goal")

        
        network = network.strip().split("\n\n")
        temp = []
        for net in network:
            line = net.split("\n")
            temp.append(line)

        self.height = len(network)
        self.width = max(len(net) for net in network)

        self.network = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if network[i][j] == self._start_char:
                        self.start = (i, j)
                        row.append(False)
                    elif network[i][j] == self._goal_char:
                        self.goal = (i, j)
                        row.append(False)
                    elif network[i][j] == self._open_char:
                        row.append(False)
                    else:
                        row.append(True)
                except:
                    row.append(False)
            self.network.append(row)

        if self.start == self.goal:
            raise Exception("Start and Goal are the same")

    
    def transition(self, node, action):
        """

        Transition function is simple here, with one key note. The maze reads from the top left as (0,0),
        so action 'up' is col - 1, and 'down' is col + 1.

        Transition tests that action is in the action_set, generates the new states base on the given
        state and action, then tests whether the new state is valid. If so, return a node based on the
        parent, state, and action.
        
        """
        if action in self.action_set:
            row, col = node.state
            """Transition kernel"""
            actions = {
                "up":    (row - 1, col),
                "down":  (row + 1, col),
                "right": (row, col + 1),
                "left":  (row, col - 1)
            }
            row, col = actions[action]
            if 0 <= row < self.height and 0 <= col < self.width and not self.network[row][col]:
                return Node(parent=node, state=(row,col), action=action)
            else:
                return None
        else:
            raise Exception("Action not in action_set")


class Maze2D(Maze):
    _action_set = ["up", "down", "right", "left"]
    
    @property
    def action_set(self):
        return self._action_set

    def __init__(self, filename=None):
        self.network = []
        self._open_char = ' '
        self._wall_char = '#'
        self._start_char = 'A'
        self._goal_char = 'B'
        self._state_char = 'O'
        
        if filename == None:
            self.height = 0
            self.width = 0
            self.start = None
            self.goal = None
        else:
            self.load(filename)

        
    def __str__(self):
        string = ""
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) == self.start:
                    string += self._start_char
                elif (i,j) == self.goal:
                    string += self._goal_char
                elif self.network[i][j]:
                    string += self._wall_char
                else:
                    string += self._open_char
            string += '\n'
        return string


    def print(self, big=1):
        string = ""
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                if (i,j) == self.start:
                    row += self._start_char * big
                elif (i,j) == self.goal:
                    row += self._goal_char * big
                elif self.network[i][j]:
                    row += self._wall_char * big
                else:
                    row += self._open_char * big
            row += '\n'
            string += row * big
        return string


    def print_state(self, state, big=1):
        string = ""
        for i in range(self.height):
            row = ''
            for j in range(self.width):
                if (i,j) == self.start:
                    row += self._start_char * big
                elif (i,j) == self.goal:
                    row += self._goal_char * big
                elif (i,j) == state:
                    row += self._state_char * big
                elif self.network[i][j]:
                    row += self._wall_char * big
                else:
                    row += self._open_char * big
            row += '\n'
            string += row * big
        return string

    def load(self, filename):
        """
        Loads a maze from the file named by filename into self.network, loads state of start
        named by 'A', and loads state of goal named by 'B'. Self.network consists of True values
        for walls (any character not 'A', 'B', or whitespace) and False values for traversable
        spaces. Also sets height as the number of lines in the file, and width as the length of
        the longest line.
        """
        with open(filename) as file:
            network = file.read()

        if network.count(self._start_char) != 1:
            raise Exception("Network has no start")

        if network.count(self._goal_char) != 1:
            raise Exception("Network has no goal")

        network = network.splitlines()
        self.height = len(network)
        self.width = max(len(net) for net in network)

        self.network = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if network[i][j] == self._start_char:
                        self.start = (i, j)
                        row.append(False)
                    elif network[i][j] == self._goal_char:
                        self.goal = (i, j)
                        row.append(False)
                    elif network[i][j] == self._open_char:
                        row.append(False)
                    else:
                        row.append(True)
                except:
                    row.append(False)
            self.network.append(row)

        if self.start == self.goal:
            raise Exception("Start and Goal are the same")

    
    def transition(self, node, action):
        """

        Transition function is simple here, with one key note. The maze reads from the top left as (0,0),
        so action 'up' is col - 1, and 'down' is col + 1.

        Transition tests that action is in the action_set, generates the new states base on the given
        state and action, then tests whether the new state is valid. If so, return a node based on the
        parent, state, and action.
        
        """
        if action in self.action_set:
            row, col = node.state
            """Transition kernel"""
            actions = {
                "up":    (row - 1, col),
                "down":  (row + 1, col),
                "right": (row, col + 1),
                "left":  (row, col - 1)
            }
            row, col = actions[action]
            if 0 <= row < self.height and 0 <= col < self.width and not self.network[row][col]:
                return Node(parent=node, state=(row,col), action=action)
            else:
                return None
        else:
            raise Exception("Action not in action_set")

        


class DepthMaze2D(Maze2D):
    def search(self):
        """
        Search for a path from start to goal
        """

        initial_node = Node(parent=None, state=self.start, action=None)
        frontier = Frontier(initial_node)

        self.solution = None
        explored = set()
        
        while True:
            try:
                if frontier == []:
                    return
                current = frontier.remove()
                explored.add(current.state)
                nodes = self.expand(current)
                for node in nodes:
                    if node.state == self.goal:
                        actions = []
                        states = []
                        while node.parent is not None:
                            actions.append(node.action)
                            states.append(node.state)
                            node = node.parent
                        actions = list(reversed(actions))
                        states = list(reversed(states))
                        self.solution = (actions, states)
                        return
                    else:
                        if not node.state in explored:
                            frontier.add(node)
            except:
                raise Exception("Error in solving")


class BreadthMaze2D(Maze2D):
    def search(self):
        """
        Search for a path from start to goal
        """

        initial_node = Node(parent=None, state=self.start, action=None)
        frontier = BreadthFrontier(initial_node)

        self.solution = None
        explored = set()
        
        while True:
            try:
                if frontier == []:
                    return
                current = frontier.remove(0)
                explored.add(current.state)
                nodes = self.expand(current)
                for node in nodes:
                    if node.state == self.goal:
                        actions = []
                        states = []
                        while node.parent is not None:
                            actions.append(node.action)
                            states.append(node.state)
                            node = node.parent
                        actions = list(reversed(actions))
                        states = list(reversed(states))
                        self.solution = (actions, states)
                        return
                    else:
                        if not node.state in explored:
                            frontier.add(node)
            except:
                raise Exception("Error in solving")

