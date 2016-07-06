import unittest
from itertools import chain

from apriori import subsets


class AprioriTest(unittest.TestCase):
    def test_subsets_should_return_empty_subsets_if_input_empty_set(self):
        result = tuple(subsets(set([])))

        self.assertEqual(result, ())

    def test_subsets_should_return_non_empty_subsets(self):
        result = tuple(subsets(set(['beer', 'rice'])))

        self.assertEqual(result[0], ('beer',))
        self.assertEqual(result[1], ('rice',))
        self.assertEqual(result[2], ('beer', 'rice',))


if __name__ == '__main__':
    unittest.main()
