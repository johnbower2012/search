from node import Node
import numpy as np

"""Stores nodes on the frontier of a search"""
class Frontier():
    """
    The Frontier stores nodes as they become available during a search and includes functionality to
    add a node, remove a node, and find the index a node fulfiling various criteria.

    :param frontier: List of nodes 
    :type frontier: list(node, ...)
    """

    def __init__(self, initial_node=None):
        if initial_node:
            self._frontier = [initial_node]
        else:
            self._frontier = []

    def __str__(self):
        s = ""
        for node in self._frontier:
            s += f"{node}\n"
        return s
            
    @property
    def frontier(self):
        return self._frontier
    
    @frontier.setter
    def frontier(self, frontier):
        if not frontier:
            raise ValueError("Missing frontier")
        self._frontier = frontier
    
    @frontier.deleter
    def frontier(self):
        del self._frontier

    def initialize(self, initial_node):
        if not initial_node:
            raise ValueError("Missing initial node")
        self._frontier = [initial_node]

    def length(self):
        """
        Returns the number of nodes in the frontier
        """
        return len(self._frontier)

    def empty(self):
        """
        Returns True if the frontier is empty, otherwise returns False
        """
        if self.length() > 0:
            return False
        else:
            return True    

    def remove(self, index=-1):
        """
        Remove and return a node from the frontier based on the given index
        Defaults to stack-like behavior if no index is given
        """
        try:
            return self.frontier.pop(index)
        except:
            raise ValueError("Unable to remove from frontier")
        
    def add(self, node):
        """
        Append the node to the end of the list
        """
        self.frontier.append(node)

    def greedy_index(self):
        """
        Returns the index of the node with the lowest cost
        """
        index = -1
        min_cost = np.inf
        for i, node in enumerate(self.frontier):
            if min_cost > node.cost:
                min_cost = node.cost
                index = i
        return index

    def astar_index(self):
        """
        Returns the index of the node with the lowested steps + cost
        """
        index = -1
        min_cost = np.inf
        for i, node in enumerate(self.frontier):
            cost = node.steps + node.cost
            if min_cost > cost:
                min_cost = cost
                index = i
        return index
            
