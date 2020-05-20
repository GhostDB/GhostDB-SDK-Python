class Node():
    def __init__(self, key, vp):
        self.key = key
        self.vp = vp
        self.left = None
        self.right = None


class AVLTree():
    """
    The `AVLTree()` object used by the `Ring` object to
    implement the consistent hashing ring. 
    """

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0


    def insert(self, key, vp):
        """
        The `insert()` method inserts a key/value pair into
        the AVL tree.

        The `key` parameter is the hexidecimal representation 
        of the CRC32 hash of the GhostDB node IP address.

        The `vp` parameter is the `VirtualPoint` being inserted
        into the tree.
        """

        node = Node(key, vp)

        # Tree is empty, initialize root
        if self.node == None:
            self.node = node
            self.node.left = AVLTree()
            self.node.right = AVLTree()
        # Insert into left subtree
        elif key < self.node.key:
            self.node.left.insert(key, vp)
        # Insert into right subtree
        elif key > self.node.key:
            self.node.right.insert(key, vp)
        
        # Rebalance if needed
        self.__rebalance()


    def remove(self, key):
        """
        The `remove()` method removes a key/value pair from the
        tree where the `value` is a `VirtualPoint` object.

        The `key` parameter is the hexidecimal representation 
        of the CRC32 hash of the GhostDB node IP address.
        """

        if self.node != None:
            # Found the node delete it
            if self.node.key == key:
                # Node is a leaf node - Just remove
                if not self.node.left.node and not self.node.right.node:
                    self.node = None
                # Node has only one subtree - the right subtree - replace root with that
                elif not self.node.left.node:
                    self.node = self.node.right.node
                # Node has only one subtree - the left subtree - replace root with that
                elif not self.node.right.node:
                    self.node = self.node.left.node
                else:
                    # Find successor as smallest node in the right subtree or
                    # predecessor as largest node in left subtree
                    successor = self.node.right.node
                    while successor and successor.left.node:
                        successor = successor.left.node

                    if successor:
                        self.node.key = successor.key
                        # Delete successor from the replaced node right subtree
                        self.node.right.remove(successor.key)

            # Remove from left subtree
            elif key < self.node.key:
                self.node.left.remove(key)
            # Remove from right subtree
            elif key > self.node.key:
                self.node.right.remove(key)
            
            # Rebalance if needed
            self.__rebalance()


    def minimum_pair(self):
        """
        the `minimum_pair()` method returns the key with the 
        smallest key value.
        """
        
        if self.node == None:
            return None
        
        current_node = self.node
        while current_node.left.node != None:
            current_node = current_node.left.node

        return (current_node.key, current_node.vp)


    def next_gte_pair(self, key):
        """
        The `next_gte_pair()` method retrieves the next GhostDB 
        node in the tree that follows the provided key in sorted
        order.

        The `key` parameter is the hexidecimal representation 
        of the CRC32 hash of the GhostDB node IP address.
        """

        node = self.__next_gte_node(self.node, key)

        if node == None:
            return None, None
        return (node.key, node.vp)


    def is_balanced(self):
        """
        The `is_balanced()` method returns `True` if the `AVLTree`
        instance is balanced, otherwise it returns `False`
        """
        
        if self.node is None:
            return True
        
        # Left subtree height
        lst = self.node.left.height
        # Right subtree height
        rst = self.node.right.height

        if (abs(lst - rst) <= 1) and self.node.left.is_balanced() is True and self.node.right.is_balanced() is True:
            return True

        return False


    def get_nodes(self):
        """
        The `get_nodes()` method returns a list of all `VirtualPoint`
        objects in the tree.
        """

        nodes = []

        if not self.node:
            return nodes
        
        nodes.extend(self.node.left.get_nodes())
        nodes.append(self.node.vp)
        nodes.extend(self.node.right.get_nodes())

        return nodes


    def inorder_traverse(self):
        """
        The `inorder_traverse()` method returns a list of all keys
        in the tree in in-order order
        """

        keys = []

        if not self.node:
            return keys
        
        keys.extend(self.node.left.inorder_traverse())
        keys.append(self.node.vp.index)
        keys.extend(self.node.right.inorder_traverse())

        return keys

    def preorder_traverse(self):
        """
        The `preorder_traverse()` method returns a list of all keys
        in the tree in pre-order order
        """
        
        keys = []

        if not self.node:
            return keys
        
        keys.append(self.node.vp.index)
        keys.extend(self.node.left.preorder_traverse())
        keys.extend(self.node.right.preorder_traverse())

        return keys


    def postorder_traverse(self):
        """
        The `postorder_traverse()` method returns a list of all keys
        in the tree in post-order order
        """

        keys = []

        if not self.node:
            return keys
        
        keys.extend(self.node.left.postorder_traverse())
        keys.extend(self.node.right.postorder_traverse())
        keys.append(self.node.vp.index)

        return keys


    def __next_gte_node(self, node, key):
        # Gets the first node with a key greater than provided key
        if node == None:
            return None
        
        if key < node.key:
            if node.left:
                after = self.__next_gte_node(node.left.node, key)
                if after == None:
                    after = node
        elif key > node.key:
            if node.right:
                after = self.__next_gte_node(node.right.node, key)           
        elif node.key == key:
            after = node

        return after


    def __rebalance(self):

        # Update the trees height and balance values
        self.__update_heights(recursive=True)
        self.__update_balances(True)

        # If balance is < -1 or > 1 then rotations are still necessary to perform
        while self.balance < -1 or self.balance > 1:
            # Left subtree is larger than right subtree so rotate to the left
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.__rotate_left()
                    self.__update_heights()
                    self.__update_balances()
                
                self.__rotate_right()
                self.__update_heights()
                self.__update_balances()
            
            # Right subtree larger than left subtree so rotate to the right
            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.__rotate_right()
                    self.__update_heights()
                    self.__update_balances()
                
                self.__rotate_left()
                self.__update_heights()
                self.__update_balances()


    def __update_heights(self, recursive=True):
        # Height is max height of left or right subtrees + 1 for the root
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.__update_heights()
                if self.node.right:
                    self.node.right.__update_heights()
            self.height = 1 + max(self.node.left.height, self.node.right.height)
        else:
            self.height = -1


    def __update_balances(self, recursive=True):
        # Calculate the balance factor of the tree
        # Balance factor calculated as follows:
        #     BF = height(left_subtree) - height(right_subtree)
        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.__update_balances()
                if self.node.right:
                    self.node.right.__update_balances()
            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0


    def __rotate_right(self):
        # Set self as the subtree of the left subtree

        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

 
    def __rotate_left(self):
        # Set self as the left subtree of the right subtree

        new_root = self.node.right.node
        new_left_sub =new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root
