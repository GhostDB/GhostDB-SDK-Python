from GhostDB.avl_tree import AVLTree
from GhostDB.virtual_point import VirtualPoint
import unittest

class TestAVLTree(unittest.TestCase):
    def test_avl_inorder_traversal(self):
        """
        Test that it traverses tree in in-order correctly
        """

        avl = AVLTree()

        point = VirtualPoint("10.128.20.1", 20)
        avl.insert(20, point)

        point = VirtualPoint("10.128.20.2", 4)
        avl.insert(4, point)

        point = VirtualPoint("10.128.20.3", 3)
        avl.insert(3, point)

        point = VirtualPoint("10.128.20.4", 9)
        avl.insert(9, point)

        point = VirtualPoint("10.128.20.5", 10)
        avl.insert(10, point)

        point = VirtualPoint("10.128.20.6", 15)
        avl.insert(15, point)

        keys = avl.inorder_traverse()

        # Expected order of keys when in-order traversal applied
        expected_key_order = [3, 4, 9, 10, 15, 20]
        self.assertEqual(keys, expected_key_order)


    def test_avl_preorder_traversal(self):
        """
        Test that it traverses tree in pre-order correctly
        """

        avl = AVLTree()

        point = VirtualPoint("10.128.20.1", 20)
        avl.insert(20, point)

        point = VirtualPoint("10.128.20.2", 4)
        avl.insert(4, point)

        point = VirtualPoint("10.128.20.3", 3)
        avl.insert(3, point)

        point = VirtualPoint("10.128.20.4", 9)
        avl.insert(9, point)

        point = VirtualPoint("10.128.20.5", 10)
        avl.insert(10, point)

        point = VirtualPoint("10.128.20.6", 15)
        avl.insert(15, point)

        keys = avl.preorder_traverse()

        # Expected order of keys when pre-order traversal applied
        expected_key_order = [10, 4, 3, 9, 20, 15]
        self.assertEqual(keys, expected_key_order)

    def test_avl_postorder_traversal(self):
        """
        Test that it traverses tree in post-order correctly
        """

        avl = AVLTree()

        point = VirtualPoint("10.128.20.1", 20)
        avl.insert(20, point)

        point = VirtualPoint("10.128.20.2", 4)
        avl.insert(4, point)

        point = VirtualPoint("10.128.20.3", 3)
        avl.insert(3, point)

        point = VirtualPoint("10.128.20.4", 9)
        avl.insert(9, point)

        point = VirtualPoint("10.128.20.5", 10)
        avl.insert(10, point)

        point = VirtualPoint("10.128.20.6", 15)
        avl.insert(15, point)

        keys = avl.postorder_traverse()

        # Expected order of keys when post-order traversal applied
        expected_key_order = [3, 9, 4, 15, 20, 10]
        self.assertEqual(keys, expected_key_order)

    def test_avl_is_balancing_correctly(self):
        """
        Test that it is balancing correctly
        """
        avl = AVLTree()

        point = VirtualPoint("10.128.20.1", 20)
        avl.insert(20, point)

        point = VirtualPoint("10.128.20.2", 4)
        avl.insert(4, point)

        point = VirtualPoint("10.128.20.3", 3)
        avl.insert(3, point)

        point = VirtualPoint("10.128.20.4", 9)
        avl.insert(9, point)

        point = VirtualPoint("10.128.20.5", 10)
        avl.insert(10, point)

        point = VirtualPoint("10.128.20.6", 15)
        avl.insert(15, point)

        bal = avl.is_balanced()

        self.assertEqual(bal, True)

    def test_avl_is_removing_and_balancing_correctly(self):
        """
        Test that it is balancing correctly after removal of a node
        """
        avl = AVLTree()

        point = VirtualPoint("10.128.20.1", 20)
        avl.insert(20, point)

        point = VirtualPoint("10.128.20.2", 4)
        avl.insert(4, point)

        point = VirtualPoint("10.128.20.3", 3)
        avl.insert(3, point)

        point = VirtualPoint("10.128.20.4", 9)
        avl.insert(9, point)

        point = VirtualPoint("10.128.20.5", 10)
        avl.insert(10, point)

        point = VirtualPoint("10.128.20.6", 15)
        avl.insert(15, point)

        avl.remove(20) # Will cause tree to rebalance

        bal = avl.is_balanced()

        self.assertEqual(bal, True)

if __name__=="__main__":
    unittest.main()