"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import argparse
import logging
import sys
from collections import defaultdict
from itertools import chain, combinations
from pathlib import Path
from typing import Iterator, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def subsets(arr) -> chain:
    """Returns non-empty subsets of arr.

    Args:
        arr: Input array to generate subsets from

    Returns:
        Chain iterator of all non-empty subsets
    """
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(
    itemSet: set[frozenset],
    transactionList: list[frozenset],
    minSupport: float,
    freqSet: defaultdict,
) -> set[frozenset]:
    """Calculates the support for items and returns subset meeting minimum support.

    Args:
        itemSet: Set of candidate itemsets
        transactionList: List of all transactions
        minSupport: Minimum support threshold (0.0-1.0)
        freqSet: Frequency set to update with item counts

    Returns:
        Set of itemsets that meet the minimum support threshold
    """
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet: set[frozenset], length: int) -> set[frozenset]:
    """Join a set with itself and returns the n-element itemsets.

    Args:
        itemSet: Set of itemsets to join
        length: Target length of joined itemsets

    Returns:
        Set of n-element itemsets
    """
    return {i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length}


def getItemSetTransactionList(data_iterator: Iterator) -> tuple[set[frozenset], list[frozenset]]:
    """Extract itemsets and transaction list from data iterator.

    Args:
        data_iterator: Iterator yielding transaction records

    Returns:
        Tuple of (itemSet, transactionList) where itemSet contains all
        1-itemsets and transactionList contains all transactions
    """
    transactionList = []
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(
    data_iter: Iterator, minSupport: float, minConfidence: float
) -> tuple[list[tuple], list[tuple]]:
    """Run the Apriori algorithm on transaction data.

    Args:
        data_iter: Iterator of transaction records
        minSupport: Minimum support threshold (0.0-1.0)
        minConfidence: Minimum confidence threshold (0.0-1.0)

    Returns:
        Tuple of (items, rules) where:
        - items: List of (itemset_tuple, support)
        - rules: List of ((antecedent_tuple, consequent_tuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set():
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item: frozenset) -> float:
        """Local function which returns the support of an item.

        Args:
            item: Itemset to calculate support for

        Returns:
            Support value (0.0-1.0)
        """
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items: list[tuple], rules: list[tuple]) -> None:
    """Prints the generated itemsets sorted by support and rules sorted by confidence.

    Args:
        items: List of (itemset, support) tuples
        rules: List of ((antecedent, consequent), confidence) tuples
    """
    for item, support in sorted(items, key=lambda x: x[1]):
        print(f"item: {item} , {support:.3f}")
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print(f"Rule: {pre} ==> {post} , {confidence:.3f}")


def to_str_results(items: list[tuple], rules: list[tuple]) -> tuple[list[str], list[str]]:
    """Converts itemsets and rules to string format for display.

    Args:
        items: List of (itemset, support) tuples
        rules: List of ((antecedent, consequent), confidence) tuples

    Returns:
        Tuple of (item_strings, rule_strings) lists
    """
    i, r = [], []
    for item, support in sorted(items, key=lambda x: x[1]):
        x = f"item: {item} , {support:.3f}"
        i.append(x)

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        x = f"Rule: {pre} ==> {post} , {confidence:.3f}"
        r.append(x)

    return i, r


def dataFromFile(fname: str | Path) -> Iterator[frozenset]:
    """Function which reads from the file and yields a generator.

    Args:
        fname: Path to the input CSV file

    Yields:
        Frozenset of items for each transaction
    """
    file_path = Path(fname)
    with file_path.open("r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(line.split(","))
            yield record


def main() -> None:
    """Main entry point for the Apriori CLI application."""
    parser = argparse.ArgumentParser(
        description="Simple Python implementation of the Apriori Algorithm"
    )
    parser.add_argument(
        "-f",
        "--inputFile",
        dest="input",
        help="filename containing csv",
        default=None,
        type=str,
    )
    parser.add_argument(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.15,
        type=float,
    )
    parser.add_argument(
        "-c",
        "--minConfidence",
        dest="minC",
        help="minimum confidence value",
        default=0.6,
        type=float,
    )

    args = parser.parse_args()

    inFile: Optional[Iterator] = None
    if args.input is None:
        inFile = sys.stdin
    else:
        inFile = dataFromFile(args.input)

    minSupport = args.minS
    minConfidence = args.minC

    logger.info(f"Running Apriori with minSupport={minSupport}, minConfidence={minConfidence}")
    items, rules = runApriori(inFile, minSupport, minConfidence)

    printResults(items, rules)


if __name__ == "__main__":
    main()
