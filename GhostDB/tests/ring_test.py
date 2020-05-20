from GhostDB.ring import Ring
import unittest
import pkgutil
import os

class TestRing(unittest.TestCase):
    def test_keys_mapping_to_correct_nodes(self):
        """
        Test that keys are being mapped to the correct nodes in the ring
        """

        hash_ring = Ring(replicas=1)

        hash_ring.add("10.23.20.2") # Hash Key - 0xd80ceccd
        hash_ring.add("10.23.34.4") # Hash Key - 0x8eda8641

        test_key_1 = "ATestingKey" # Hash Key - 0x2269b0e
        test_key_2 = "AnotherTestingKey" # Hash Key - 0xd3918bd2

        # Test Key 1 should map to server 2 - 10.23.34.4
        #    - This servers Hash Key (0x8eda8641) is
        #      next node on the ring that is greater
        #      than the Hash Key of test key 1 (0x2269b0e)
        node_for_requset_1 = hash_ring.get_point_for(test_key_1)
        ip_address = node_for_requset_1.node

        self.assertEqual(ip_address, "10.23.34.4")

        # Test Key 2 should map to server 1 - 10.23.20.2
        #    - This servers Hash Key (0xd80ceccd) is
        #      next node on the ring that is greater
        #      than the Hash Key of test key 2 (0xd3918bd2)
        node_for_requset_2 = hash_ring.get_point_for(test_key_2)
        ip_address = node_for_requset_2.node

        self.assertEqual(ip_address, "10.23.20.2")

    def test_ring_building_from_node_config_file(self):
        """
        Test that the ring is being created automatically from the node config file
        """
        node_conf_data = pkgutil.get_data("GhostDB", "tests/ghostdb_test.conf")
        node_conf_data = node_conf_data.replace(b'\r', b'')
        data = node_conf_data.decode("utf-8")
        print(data)   
        with open("node_data.conf ", "a") as f:
            f.write(data)

        hash_ring = Ring(node_config="node_data.conf " , replicas=1)

        keys = hash_ring.ring.preorder_traverse()
        self.assertEqual(keys, ['0xd80ceccd', '0x8eda8641'])

        os.remove("node_data.conf ")

if __name__=="__main__":
    unittest.main()
