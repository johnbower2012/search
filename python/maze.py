import sys
import re
from node import Node
from frontier import Frontier
from dimensions import Dimensions
import random

"""SEED the random search function"""
SEED=None

class Maze:
    """
    Initializes an instance of Maze

    :param start_char: Represents the starting point
    :type start_char: char/str
    :param goal_char: Represents the goal point
    :type goal_char: char/str
    :param state_char: Represents present state
    :type state_char: char/str
    :param space_char: Represents traversable space
    :type space_char: char/str
    :param wall_char: Represents non-tranversable space
    :type wall_char: char/str
    :param sep_char: Represents a division in dimensions
    :type sep_char: char/str
    :param actions: List of actions that can be taken in a single dimension
    :type actions: list(str, str)
    """

    start_char = 'A'
    goal_char = 'B'
    state_char = 'O'
    space_char = ' '
    wall_char = '#'
    sep_char = '\n'
    actions = ["up", "down"]
    
    def __init__(self, filename=None):
        """
        Initializes a Maze instance using built in functionality.
        """
        if filename:
            self.load(filename)
            self.set_dim()
            self.set_actions()
            self.build()
        else:
            self.dims = []
            self.dimensions = 0

    def __str__(self):
        """
        Returns the contents loaded from file
        """
        if not self.contents:
            raise Exception("Maze not yet loaded")
        return self.contents

    def print(self, big=1):
        """
        Returns a string representing the maze that can be printed to screen. The string uses the class
        variable characters and a big factor to construct the visual representation. The big factor
        increases the size of the maze by repeating each character big * big times in a square with side
        of length big, e.g., for big=1 the maze is normal, for big=2 the maze is twice as tall and twice
        as wide, etc.

        :param counter: Tracks current state in maze
        :type counter: Dimensions class
        :param s: Representation of maze to be returned
        :type s: string
        :param big: Big factor used to determine maze magnification
        :type big: int
        """
        
        s = ""
        counter = Dimensions()
        counter.set_dimensions(self.dims)
        row = ""
        """Loop over all possible states using counter until counter rolls over to all zeros"""
        while True:
            current = tuple(counter.count)
            """State checking to ensure each state is properly represeted using the cls variable chars"""
            if current == self.start:
                row += self.start_char * big
            elif current == self.goal:
                row += self.goal_char * big
            elif self.value(self.maze, current):
                row += self.wall_char * big
            else:
                row += self.space_char * big

            counter.increment()
            next = tuple(counter.count)
            """Tracks correct dimensional representation in s by inserting 'sep_char's"""
            if counter.count[self.dimensions - 1] == 0:
                row += self.sep_char
                s += row * big
                row = ""
                """Check for higher dimensional shifts and insert the appropriate nunber of sep_char"""
                diff = list()
                for c, n in zip(current, next):
                    diff.append(n - c)
                for i in range(self.dimensions):
                    if diff[i] == 1:
                        s += self.sep_char * (self.dimensions - 2 - i)
                        break
            """Once counter reads all zeros, every state has been included in the representation"""
            if all(n == 0 for n in next):
                break
        return s

    def print_state(self, state, big=1):
        """
        Print_state functions precisely as print, with the additional functionality of including a
        current state within the representation. For additional documentation, please see print above.

        :param state: Current state to be represented
        :param type: tuple(int, ...)
        """
        s = ""
        counter = Dimensions()
        counter.set_dimensions(self.dims)
        row = ""
        while True:
            current = tuple(counter.count)
            """As print, but also check whether the counter state is the state to be included in the representation"""
            if current == self.start:
                row += self.start_char * big
            elif current == self.goal:
                row += self.goal_char * big
            elif current == state:
                row += self.state_char * big
            elif self.value(self.maze, counter.count):
                row += self.wall_char * big
            else:
                row += self.space_char * big

            counter.increment()
            next = tuple(counter.count)
            if counter.count[self.dimensions - 1] == 0:
                row += self.sep_char
                s += row * big
                row = ""
                diff = list()
                for c, n in zip(current, next):
                    diff.append(n - c)
                for i in range(self.dimensions):
                    if diff[i] == 1:
                        s += self.sep_char * (self.dimensions - 2 - i)
                        break
            if all(n == 0 for n in next):
                break
        return s

    def load(self, filename):
        """
        Loads the contents of a file into the class instance. Current implementation allows for only
        a single start state and a single goal state.

        In theory, both multiple start states and multiple goal states could currently be allowed by
        removing the below error checking. As is, the program would terminate upon finding any goal state
        and return the solution to the one found. With slight modification, multiple start points could
        be included, perhaps where one is chosen at random for a particular search.

        :param filename: Name of the file to be read
        :type filename: string
        :param contents: Contents of the file to be kept as self.contents
        :type contents: string
        """
        with open(filename) as file:
            contents = file.read()
        if contents.count(self.start_char) != 1:
            raise Exception("Maze does not have one start")
        if contents.count(self.goal_char) != 1:
            raise Exception("Maze does not have one goal")
        self.contents = contents.strip('\n')

    def det_dim(self, contents, index=0):
        """
        det_dim is called by set_dim to determine the maximum length of each dimension. det_dim works
        recursively given 'contents' and an 'index' that represents both the current level of recursion and
        the current dimension. The 'sep_char' class variable is used to differentiate dimensions, e.g.,
        a single instance of sep_char divides two rows of the maze, two contiguous sep_chars divide two
        sets of rows (2D submazes) of the maze, etc. More generally, n instances of sep_char separate two n-dimensional
        sub-mazes in the higher dimensional maze.

        For visual simplicity in the text file, the sep_char is '\n' by default.

        :param contents: Representation of the maze that is given to parse
        :type contents: string
        :param index: Current level of recursion and dimension
        :type index: int
        """
        """If the current dimension is not yet at the deepest level, continue to recur"""
        if index < self.dimensions - 1:
            current = self.dimensions - 1 - index
            """Split the current section of contents into its deeper constituent parts"""
            contents = re.split(self.sep_char * (current), contents)
            """Find the maximum length along the current dimensionm"""
            if len(contents) > self.dims[index]:
                self.dims[index] = len(contents)
            """For each sub-maze, call det_dim and increment the index by one"""
            for content in contents:
                self.det_dim(content.strip('\n'), index + 1)
        elif index == self.dimensions - 1:
            """For the final dimension, determine maximum length """
            if len(contents) > self.dims[index]:
                self.dims[index] = len(contents)
        
    def set_dim(self):
        """
        Determine the number of dimensions and the maximum length of each dimension. set_dim calls
        det_dim to find the maximum length of each dimension.

        :param self.dimensions: Number of dimensions in the maze
        :type self.dimensions: int
        :param self.dims: Maximum length of each dimension
        :type self.dims: list of ints
        """
        """If contentes is empty, set dimensions to zero and dims to an empty list"""
        if not self.contents:
            self.dimensions = 0
            self.dims = []
        else:
            """The number of dimensions is determined by the longest string of sep_char"""
            dims = re.findall(f"{self.sep_char}+", self.contents)
            """If no sep_char in contents, the maze is one dimensional"""
            if not dims:
                self.dimensions = 1
                self.dims = [len(self.contents)]
            else:
                """Set the number of dimensions and initialize self.dims before calling det_dim"""
                self.dimensions = len(max(dims)) + 1
                self.dims = [0] * self.dimensions
                self.det_dim(self.contents)
                
    def assemble(self, contents, index=0):
        """
        assemble is called by build to construct a boolean representation of the maze and functions
        recursively

        :param contents: Representation of the maze to be parsed
        :type contents: string
        :param index: current level of recursion
        :type index: int
        :param maze: boolean representation of the maze
        :type maze: nested lists of booleans
        """
        maze = []
        dims = self.dimensions - 1 - index
        """If not yet at the deepest level, recur"""
        if dims > 0:
            """Split to the next deeper level"""
            pieces = re.split(self.sep_char * dims, contents)
            """Check each subsegment for the presence of the start and goal states"""
            for i, piece in enumerate(pieces):
                if self.start_char in piece:
                    """Set the index of the start state along current dimension"""
                    self.start[index] = i
                if self.goal_char in piece:
                    """Set the index of the goal state along current dimension"""
                    self.goal[index] = i
                """Parse and append the subsegment of the maze"""
                maze.append(self.assemble(piece, index + 1))
        else:
            """If at deepest level, parse the subsegment of maze based on each character"""
            for i, char in enumerate(contents):
                if char == self.start_char:
                    """Set the index of the start state along final dimension"""
                    self.start[index] = i
                    maze.append(False)
                elif char == self.goal_char:
                    """Set the index of the goal state along final dimension"""
                    self.goal[index] = i
                    maze.append(False)
                elif char == self.space_char:
                    maze.append(False)
                else:
                    """Any character that is not explicitly the start_char, goal_char, or space_char is interpreted as a wall_char"""
                    maze.append(True)
        return maze

    def build(self):
        """
        Construct a boolean representation of the maze stored in self.contents. I
        initialize start and goal as zeroed lists to be updated in assemble.
        Call assemble to construct the maze and determine the start and goal states.
        Convert state and goal to tuples.

        :param self.start: Start state
        :type self.start: tuple
        :param self.goal: Goal state
        :type self.goal: tuple
        :param self.maze: Representation of the maze
        :type self.maze: nested lists of booleans
        """
        self.start = [0] * self.dimensions
        self.goal = [0] * self.dimensions
        self.maze = self.assemble(self.contents)
        self.start = tuple(self.start)
        self.goal = tuple(self.goal)

    def set_actions(self):
        """
        Construct the action set to be used in expand, of form [(dim_0, "up"), (dim_0, "down"), ...].

        :param action_set: Set of actions that can be taken from a generic state
        :type action_set: list(tuple(int, string), ...)
        """
        self.action_set = []
        for dim in range(self.dimensions):
            for action in self.actions:
                self.action_set.append((dim, action))
        
    def value(self, maze, state):
        """
        Simple recursive way to access the value stored at state in maze.
        If the state attempts to access a place in maze that is out of index, assume it is a wall character.
        This is done to allow and handle non-uniform lengths along like dimensions. For example, for a typical
        2D maze, this allows variable length rows.

        :param maze: Representation of the maze
        :type maze: nested lists of booleans
        :param state: Representation of the current state
        :type state: tuple
        :param value: Value stored at state in maze
        :type value: boolean
        """
        try:
            for i in range(self.dimensions):
                maze = maze[state[i]]
            return maze
        except:
            return True
        
    def expand(self, node):
        """
        Returns a list of nodes containing the valid states reachable from the given state

        :param node: Current node from which to seek valid states
        :type node: Node
        :param nodes: List of nodes containing valid states
        :type nodes: list of Nodes
        """
        nodes = []
        """Loop over all actions in the action_set"""
        for action in self.action_set:
            dim, act = action
            """Determine state reached by the action, if any"""
            next = self.transition(node, dim, act)
            """If a valid state was reached, append it to the list"""
            if next != None:
                nodes.append(next)
        return nodes

    def transition(self, node, dim, action):
        """
        Check if the state reached by attempting 'action' along dimension 'dim' from state 'node.state'
        is valid, and if so, return an node with the appropriate information. One quirk is that since for
        a 2D maze (0,0) is at the top left visually, the first dimension counts from the top of the
        screen. This extrapolates to the penultimate dimension in n-dimensions, and is handled below to
        avoid confusion when reading actions taken in the solution.

        :param node: Node containing the current state
        :type node: Node
        :param dim: Dimension along which to attempt action
        :type dim: int
        :param aciton: Action to be taken
        :type action: string
        """
        """Ensure action is a valid action"""
        if action in self.actions:
            """Generate mutable copy of the current state"""
            state = list(node.state)
            """Handle that along the penultimate dimension 0 is at the top visually"""
            if dim == self.dimensions - 2:
                if action == "down":
                    state[dim] += 1
                else:
                    state[dim] -= 1
            else:
                if action == "up":
                    state[dim] += 1
                else:
                    state[dim] -= 1
            check = True
            """Ensure state is still within the proper range along each dimension"""
            for i in range(self.dimensions):
                if 0 <= state[i] < self.dims[i]:
                    continue
                else:
                    check = False
                    break
            if check:
                """Ensure the state is traversable, i.e., not a wall"""
                """If out of bounds, assume it's a wall"""
                try:
                    if not self.value(self.maze, state):
                        """If the state exists and is traversable, return a node with the proper parent, state, and action"""
                        return Node(parent=node, state=tuple(state), action=(dim,action))
                except:
                    return None
            return None
        else:
            raise Exception("action not in actions")
            
    def goal(self, state):
        """
        Tests if the given state is the goal state. If so, return True, else False.

        :param state: Representation of the current state
        :type state: tuple(int, ...)
        """
        return state == self.goal

    def manhatten_distance(self, state):
        """
        Calcualtes the manhatten distance between the given state and the goal state stored in the class
        instance.

        :param state: Representation of the current state
        :type state: tuple(int, ...)
        """
        diff = 0
        for g, c in zip(self.goal, tuple(state)):
            diff += (abs(g-c))
        return diff

    def breadth_search(self):
        """
        Conducts a breadth search (queue-like frontier) of the maze beginning from the start state
        seeking the goal state, then stores the solution as a tuple of the action list and state list
        that reaches the goal state: (actions, states).

        To increase efficiency the states are tested as they are added to the frontier instead of as
        they are popped from the frontier.

        :param self.solution: Representation of the solution, including actions and states
        :type self.solution: tuple(list((int, string), ...), list(tuple(int, ...), ...))
        """

        """Test if the start and goal states are the same"""
        if self.start == self.goal:
            actions = None
            states = self.goal
            self.solution = (actions, states)

        """Initialize the frontier using a root node storing the start state"""
        root = Node(parent=None, state=self.start, action=None)
        frontier = Frontier(root)
        """Initialize the solution"""
        self.solution = None
        """Initialize the explored set"""
        explored = set()

        """Loop until either the solution is found or the frontier is empty"""
        while True:
            try:
                """If the frontier is empty, all states have been explored and there is no solution"""
                if frontier.empty():
                    return
                """Breadth search uses a queue-like (FIFO) frontier of nodes"""
                current = frontier.remove(0)
                """Once is state is chosen to be explored, add to the explored set"""
                explored.add(current.state)
                """Determine the states reachable from the chosen state"""
                nodes = self.expand(current)
                for node in nodes:
                    """If the state is the goal state, construct the solution and end"""
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
                        """If not the goal state and not explored before, add it to the frontier"""
                        if not tuple(node.state) in explored:
                            frontier.add(node)
            except:
                raise Exception("Error in solving")

    def depth_search(self):
        """
        Conducts a depth search (stack-like frontier) of the maze beginning from the start state seeking
        the goal state, then stores the solution as a tuple of the action list and state list that
        reaches the goal state: (actions, states).

        To increase efficiency the states are tested as they are added to the frontier instead of as they
        are popped from the frontier.

        Functions as the breadth_search, with the exception of the frontier behavior.

        :param self.solution: Representation of the solution, including actions and states
        :type self.solution: tuple(list((int, string), ...), list(tuple(int, ...), ...))
        """

        """Test if the start and goal states are the same"""
        if self.start == self.goal:
            actions = None
            states = self.goal
            self.solution = (actions, states)

        """Initialize the frontier using a root node storing the start state"""
        root = Node(parent=None, state=self.start, action=None)
        frontier = Frontier(root)
        
        """Initialize the solution"""
        self.solution = None
        """Initialize the explored set"""
        explored = set()

        """Loop until either the solution is found or the frontier is empty"""
        while True:
            try:
                """If the frontier is empty, all states have been explored and there is no solution"""
                if frontier.empty():
                    return
                """Depth search uses a stack-like (LIFO) frontier of nodes"""
                current = frontier.remove()
                """Once is state is chosen to be explored, add to the explored set"""
                explored.add(current.state)
                """Determine the states reachable from the chosen state"""
                nodes = self.expand(current)
                for node in nodes:
                    """If the state is the goal state, construct the solution and end"""
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
                        """If not the goal state and not explored before, add it to the frontier"""
                        if not tuple(node.state) in explored:
                            frontier.add(node)
            except:
                raise Exception("Error in solving")

    def greedy_search(self):
        """
        Conducts a greedy search of the maze beginning from the start state seeking
        the goal state, then stores the solution as a tuple of the action list and state list that
        reaches the goal state: (actions, states). The greedy search selects from the frontier by
        determining which state in the frontier has the lowest estimated cost to the goal state. Here,
        the estimate is generated using the manhatten distance.

        To increase efficiency the states are tested as they are added to the frontier instead of as they
        are popped from the frontier.

        Functions as the breadth_search, with the exception of the frontier behavior.

        :param self.solution: Representation of the solution, including actions and states
        :type self.solution: tuple(list((int, string), ...), list(tuple(int, ...), ...))
        """

        """Test if the start and goal states are the same"""
        if self.start == self.goal:
            actions = None
            states = self.goal
            self.solution = (actions, states)

        """Initialize the frontier using a root node storing the start state"""
        root = Node(parent=None, state=self.start, action=None)
        root.cost = self.manhatten_distance(root.state)
        frontier = Frontier(root)

        """Initialize the solution"""
        self.solution = None
        """Initialize the explored set"""
        explored = set()

        """Loop until either the solution is found or the frontier is empty"""
        while True:
            try:
                """If the frontier is empty, all states have been explored and there is no solution"""
                if frontier.empty():
                    return
                """Greedy search uses the manhatten distance to pop a node from the frontier"""
                index = frontier.greedy_index()
                current = frontier.remove(index)
                """Once is state is chosen to be explored, add to the explored set"""
                explored.add(current.state)
                """Determine the states reachable from the chosen state"""
                nodes = self.expand(current)
                for node in nodes:
                    """If the state is the goal state, construct the solution and end"""
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
                        """If not the goal state and not explored before, add it to the frontier"""
                        if not tuple(node.state) in explored:
                            node.cost = self.manhatten_distance(node.state)
                            frontier.add(node)
            except:
                raise Exception("Error in solving")

    def astar_search(self):
        """
        Conducts an astar search of the maze beginning from the start state seeking
        the goal state, then stores the solution as a tuple of the action list and state list that
        reaches the goal state: (actions, states). The astar search selects from the frontier by
        determining which state in the frontier has the lowest steps plus estimated cost to the goal
        state. Here, the steps are calculated as the number of actions from the start state and the
        estimated cost is generated using the manhatten distance.

        To increase efficiency the states are tested as they are added to the frontier instead of as they
        are popped from the frontier.

        Functions as the breadth_search, with the exception of the frontier behavior.

        :param self.solution: Representation of the solution, including actions and states
        :type self.solution: tuple(list((int, string), ...), list(tuple(int, ...), ...))
        """

        """Test if the start and goal states are the same"""
        if self.start == self.goal:
            actions = None
            states = self.goal
            self.solution = (actions, states)

        """Initialize the frontier using a root node storing the start state"""
        root = Node(parent=None, state=self.start, action=None)
        root.cost = self.manhatten_distance(root.state)
        frontier = Frontier(root)

        """Initialize the solution"""
        self.solution = None
        """Initialize the explored set"""
        explored = set()

        """Loop until either the solution is found or the frontier is empty"""
        while True:
            try:
                """If the frontier is empty, all states have been explored and there is no solution"""
                if frontier.empty():
                    return
                """Astar search uses steps taken + manhatten distance to pop a node from the frontier"""
                index = frontier.astar_index()
                current = frontier.remove(index)
                """Once is state is chosen to be explored, add to the explored set"""
                explored.add(current.state)
                """Determine the states reachable from the chosen state"""
                nodes = self.expand(current)
                for node in nodes:
                    """If the state is the goal state, construct the solution and end"""
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
                        if not tuple(node.state) in explored:
                            """If not the goal state and not explored before, add it to the frontier"""
                            node.cost = self.manhatten_distance(node.state)
                            frontier.add(node)
            except:
                raise Exception("Error in solving")

    def random_search(self):
        """
        Conducts a random search of the maze beginning from the start state seeking
        the goal state, then stores the solution as a tuple of the action list and state list that
        reaches the goal state: (actions, states). The random search selects from the frontier by
        randomly.

        To increase efficiency the states are tested as they are added to the frontier instead of as they
        are popped from the frontier.

        Functions as the breadth_search, with the exception of the frontier behavior.

        :param self.solution: Representation of the solution, including actions and states
        :type self.solution: tuple(list((int, string), ...), list(tuple(int, ...), ...))
        """

        """Test if the start and goal states are the same"""
        if self.start == self.goal:
            actions = None
            states = self.goal
            self.solution = (actions, states)

        """Initialize the frontier using a root node storing the start state"""
        root = Node(parent=None, state=self.start, action=None)
        frontier = Frontier(root)
        """Seed the random generator"""
        if SEED:
            random.seed(SEED)
        
        """Initialize the solution"""
        self.solution = None
        """Initialize the explored set"""
        explored = set()

        """Loop until either the solution is found or the frontier is empty"""
        while True:
            try:
                """If the frontier is empty, all states have been explored and there is no solution"""
                if frontier.empty():
                    return
                """Random search pops a node randomly from the frontier"""
                index = random.randrange(len(frontier.frontier))
                current = frontier.remove(index)
                """Once is state is chosen to be explored, add to the explored set"""
                explored.add(current.state)
                """Determine the states reachable from the chosen state"""
                nodes = self.expand(current)
                for node in nodes:
                    """If the state is the goal state, construct the solution and end"""
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
                        """If not the goal state and not explored before, add it to the frontier"""
                        if not tuple(node.state) in explored:
                            frontier.add(node)
            except:
                raise Exception("Error in solving")


