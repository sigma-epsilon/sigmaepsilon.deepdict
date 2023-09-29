import unittest

from sigmaepsilon.deepdict import DeepDict


class TestCompliance(unittest.TestCase):
    
    def setUp(self):
        self.custom_dict = DeepDict()
    
    def test_set_and_get_item(self):
        # Test setting and getting items
        self.custom_dict['key1'] = 'value1'
        self.assertEqual(self.custom_dict['key1'], 'value1')
    
    def test_len(self):
        # Test the len() function
        self.custom_dict['key1'] = 'value1'
        self.custom_dict['key2'] = 'value2'
        self.assertEqual(len(self.custom_dict), 2)
    
    def test_keys(self):
        # Test the keys() method
        self.custom_dict['key1'] = 'value1'
        self.custom_dict['key2'] = 'value2'
        self.assertEqual(list(self.custom_dict.keys()), ['key1', 'key2'])
    
    def test_values(self):
        # Test the values() method
        self.custom_dict['key1'] = 'value1'
        self.custom_dict['key2'] = 'value2'
        self.assertEqual(list(self.custom_dict.values()), ['value1', 'value2'])
    
    def test_items(self):
        # Test the items() method
        self.custom_dict['key1'] = 'value1'
        self.custom_dict['key2'] = 'value2'
        self.assertEqual(list(self.custom_dict.items()), [('key1', 'value1'), ('key2', 'value2')])
    
    def test_contains(self):
        # Test the 'in' operator
        self.custom_dict['key1'] = 'value1'
        self.assertTrue('key1' in self.custom_dict)
        self.assertFalse('key2' in self.custom_dict)
    
    def test_delete_item(self):
        # Test deleting items
        self.custom_dict['key1'] = 'value1'
        del self.custom_dict['key1']
        self.assertNotIn('key1', self.custom_dict)

if __name__ == '__main__':
    unittest.main()
