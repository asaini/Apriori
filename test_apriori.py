from collections import defaultdict
from itertools import chain
import unittest

from apriori import (
    subsets,
    returnItemsWithMinSupport,
)


class AprioriTest(unittest.TestCase):
    def test_subsets_should_return_empty_subsets_if_input_empty_set(self):
        result = tuple(subsets(frozenset([])))

        self.assertEqual(result, ())

    def test_subsets_should_return_non_empty_subsets(self):
        result = tuple(subsets(frozenset(['beer', 'rice'])))

        self.assertEqual(result[0], ('beer',))
        self.assertEqual(result[1], ('rice',))
        self.assertEqual(result[2], ('beer', 'rice',))

    def test_return_items_with_min_support(self):
        itemSet = set([
            frozenset(['apple']),
            frozenset(['beer']),
            frozenset(['chicken']),
            frozenset(['mango']),
            frozenset(['milk']),
            frozenset(['rice'])
        ])
        transactionList = [
            frozenset(['beer', 'rice', 'apple', 'chicken']),
            frozenset(['beer', 'rice', 'apple']),
            frozenset(['beer', 'apple']),
            frozenset(['mango', 'apple']),
            frozenset(['beer', 'rice', 'milk', 'chicken']),
            frozenset(['beer', 'rice', 'milk']),
            frozenset(['beer', 'milk']),
            frozenset(['mango', 'milk'])
        ]
        minSupport = 0.5
        freqSet = defaultdict(int)

        result = returnItemsWithMinSupport(
            itemSet,
            transactionList,
            minSupport,
            freqSet
        )

        expected = set([
            frozenset(['milk']),
            frozenset(['apple']),
            frozenset(['beer']),
            frozenset(['rice'])
        ])
        self.assertEqual(result, expected)

        expected = defaultdict(
            int,
            {
                frozenset(['apple']): 4,
                frozenset(['beer']): 6,
                frozenset(['chicken']): 2,
                frozenset(['mango']): 2,
                frozenset(['milk']): 4,
                frozenset(['rice']): 4
            }
        )
        self.assertEqual(freqSet, expected)


if __name__ == '__main__':
    unittest.main()
