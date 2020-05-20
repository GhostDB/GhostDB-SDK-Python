class VirtualPoint():
    """
    Virtual Point represents a point of a GhostDB cache on the hash ring
    """
    def __init__(self, node, index):
        self.node = node
        self.index = index

    def __str__(self):
        return "====\nNode: {:s}\nIndex: {:s}\n====".format(self.node, self.index) 

    def set_index(index):
        self.index = index
