"""Class to simplify numbers with varying bases"""

class Dimensions:
    """
    Dimensions allows the user to work with a number  where each position can have a different basis. For
    example, a number with bases 4,2,3 would count
    001, 002, 010, 011, 012, 100, 101, ..., 312, 000 (roll over). In decimal, these numbers are
    001, 002, 003, 004, 005, 006, 007, ..., 023, 024 (not rolled over).

    :param self._dim: Base for each dimension
    :type self._dim: tuple(int, ...)
    :param self._count: Current counter
    :type self._count: list(int, ...)
    """

    def __init__(self):
        self._dim = None
        self._count = None

    def __str__(self):
        if not self._dim:
            return ""
        s = ""
        n = len(self._dim)
        for i in range(n - 1):
            s += f"{self._dim[i]},"
        s += f"{self._dim[n - 1]}"
        return s
        
    @property
    def dim(self):
        return self._dim

    @dim.setter
    def dim(self, dim):
        self._dim = dim
        
    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count
            
    def set_dimensions(self, dim):
        """
        Set the dimensions and re-initialize the counter
        """
        self._dim = tuple(dim)
        self._count = [0] * self.dims()

    def dims(self):
        """
        Return the number of dimensions in the basis set
        """
        return len(self._dim)

    def enumerate(self):
        """
        Return a list of every number from zero to the maximum under the current basis set
        """

        """If there are no dimensions currenty set, return an empty list"""
        if not self._dim:
            return []
        dims = self.dims()
        """Initialize the counter"""
        count = [0] * dims
        s = []
        while True:
            """Append current number"""
            s.append([*count])
            """Increment the current number"""
            count[dims - 1] += 1
            """Carry the one"""
            for i in range(dims - 1, 0, -1):
                if count[i] >= self._dim[i]:
                    count[i] = 0
                    count[i-1] += 1
            """If the most significant position rolls over, break"""
            if count[0] >= self._dim[0]:
                break
        return s

    def increment(self):
        """
        Increment the internal counter by one
        """

        """If dimension is not yet set, end"""
        if not self._dim:
            return
        dims = self.dims()
        """Increment"""
        self._count[dims - 1] += 1
        """Carry the one"""
        for i in range(dims - 1, 0, -1):
            if self._count[i] >= self._dim[i]:
                self._count[i] = 0
                self._count[i-1] += 1
        """If the most significant digit exceeds the max, roll to zero"""
        if self._count[0] >= self._dim[0]:
            self._count[0] = 0
        return self._count

    def decimal(self, number=None):
        """
        Return a given number in decimal. If no number is given, convert the internal counter by default
        """
        if not number:
            number = self.count()
        factor=1
        n=0
        for base, num in zip(list(reversed(self.dim)), list(reversed(number))):
            n += num * factor
            factor *= base
        return n
        
