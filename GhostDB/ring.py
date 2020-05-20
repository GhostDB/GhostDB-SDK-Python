from GhostDB.avl_tree import AVLTree
from GhostDB.virtual_point import VirtualPoint
import binascii

class Ring():
    """
    The `Ring` object represents the consistent hashing ring.

    The `node_config` parameter defaults to `None`, however it
    should be provided by the `Cache` object

    The `replicas` parameter adds replicas for a virtual point
    in the tree. This defaults to `1` and it is not recommended
    to change this.
    """

    def __init__(self, node_config=None, replicas=1):
        self.replicas = replicas
        self.ring = AVLTree()
   
        if node_config:
            with open(node_config, 'r') as nodes:
                for node in nodes.readlines():
                    node = node.strip()
                    self.add(node)

    def __len__(self):
        return len(self.ring.get_nodes())


    def __str__(self):
        return self.ring.__str__()


    def add(self, node):
        """
        The `add()` method adds a GhostDB node to the
        consistent hashing ring.
        """

        for i in range(self.replicas):
            key = self.key_hash(node, i)
            vp = VirtualPoint(node, key)
            self.ring.insert(key, vp)
    

    def delete(self, node):
        """
        The `delete()` method removes a GhostDB node from the
        consistent hashing ring. This is typically performed
        if the GhostDB node is unreachable.
        """

        for i in range(self.replicas):
            key = self.key_hash(node, i)
            self.ring.remove(key)


    def get_point_for(self, key):
        """
        The `get_point_for()` method returns the correct 
        GhostDB node to send a request to for a given key.
        """

        if len(self) == 0:
            return None
        key = self.key_hash(key)
        node_key, node_value = self.ring.next_gte_pair(key)
        if not node_value:
            node_key, node_value = self.ring.minimum_pair()

        return node_value


    def get_points(self):
        """
        The `get_points()` method returns all GhostDB nodes
        in the consistent hashing ring.
        """
        
        return self.ring.get_nodes()

    def key_hash(self, key, index=None):
        """
        The `key_hash()` method generates and returns 
        the unsigned CRC32 hash for a provided key in 
        hexidecimal form.
        """

        if index:
            key = "{:s}:{:d}".format(key, index)
        s = binascii.crc32(bytes(key, 'utf-8'))
        return hex(s)
