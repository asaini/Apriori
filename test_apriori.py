from collections import defaultdict
from itertools import chain
import unittest

from apriori import (
    getItemSetTransactionList,
    joinSet,
    returnItemsWithMinSupport,
    subsets,
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

    def test_join_set_and_get_two_element_itemsets(self):
        itemSet = set([
            frozenset(['apple']),
            frozenset(['beer']),
            frozenset(['chicken']),
            frozenset(['mango']),
            frozenset(['milk']),
            frozenset(['rice'])
        ])

        result = joinSet(itemSet, 2)

        expected = set([
            frozenset(['chicken', 'mango']),
            frozenset(['rice', 'apple']),
            frozenset(['beer', 'apple']),
            frozenset(['rice', 'milk']),
            frozenset(['beer', 'rice']),
            frozenset(['chicken', 'apple']),
            frozenset(['beer', 'milk']),
            frozenset(['chicken', 'rice']),
            frozenset(['beer', 'mango']),
            frozenset(['beer', 'chicken']),
            frozenset(['apple', 'milk']),
            frozenset(['mango', 'milk']),
            frozenset(['mango', 'apple']),
            frozenset(['rice', 'mango']),
            frozenset(['chicken', 'milk'])
        ])
        self.assertEqual(result, expected)

    def test_join_set_and_get_three_element_itemsets(self):
        itemSet = set([
            frozenset(['apple', 'beer']),
            frozenset(['beer']),
            frozenset(['chicken']),
            frozenset(['mango']),
            frozenset(['milk']),
            frozenset(['rice'])
        ])

        result = joinSet(itemSet, 3)

        expected = set([
            frozenset(['beer', 'mango', 'apple']),
            frozenset(['beer', 'apple', 'chicken']),
            frozenset(['beer', 'apple', 'milk']),
            frozenset(['beer', 'rice', 'apple'])
        ])
        self.assertEqual(result, expected)

    def test_get_itemset_and_transaction_list_from_data_iterator(self):
        data_iterator = [
            frozenset(['beer', 'rice', 'apple', 'chicken']),
            frozenset(['mango', 'beer']),
        ]

        itemSet, transactionList = getItemSetTransactionList(data_iterator)

        expected = set([
            frozenset(['chicken']),
            frozenset(['apple']),
            frozenset(['beer']),
            frozenset(['rice']),
            frozenset(['mango'])
        ])
        self.assertEqual(itemSet, expected)

        expected = data_iterator
        self.assertEqual(transactionList, expected)


if __name__ == '__main__':
    unittest.main()
