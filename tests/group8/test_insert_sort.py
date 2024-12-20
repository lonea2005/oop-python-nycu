#insert sort python test file
import unittest
from lec12_sortings import insert_sort as g8_insert_sort

class TestInsertSort(unittest.TestCase):
    
        def test_insert_sort(self):
            self.assertEqual(g8_insert_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
            self.assertEqual(g8_insert_sort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])
            self.assertEqual(g8_insert_sort([1, 3, 2, 5, 4]), [1, 2, 3, 4, 5])
            self.assertEqual(g8_insert_sort([1, 2, 3, 5, 4]), [1, 2, 3, 4, 5])
            self.assertEqual(g8_insert_sort([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            self.assertEqual(g8_insert_sort([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            self.assertEqual(g8_insert_sort([1, 3, 2, 5, 4, 7, 6, 9, 8, 10]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            self.assertEqual(g8_insert_sort([1, 2, 3, 5, 4, 7, 6, 9, 8, 10]), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

if __name__ == '__main__':
      
    unittest.main()