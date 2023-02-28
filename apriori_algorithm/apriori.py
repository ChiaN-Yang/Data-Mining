"""Implementation of the Apriori Algorithm"""
import argparse
from itertools import chain, combinations
from collections import defaultdict


def subsets(arr):
    """Returns non empty subsets of array."""
    return chain(*[combinations(arr, i + 1) for i, _ in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """Calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support.
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


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets."""
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """run the apriori algorithm. data_iter is a record iterator.

    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        currentLSet = currentCSet
        k += 1

    def getSupport(item):
        """Local function which Returns the support of an item."""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for value in largeSet.values():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])

    toRetRules = []
    for value in list(largeSet.values())[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item) / getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """Prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))


def toStrResults(items, rules):
    """Prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    i, r = [], []
    for item, support in sorted(items, key=lambda x: x[1]):
        x = "%s , %.3f" % (str(item), support)
        i.append(x)

    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        x = "%s ==> %s , %.3f" % (str(pre), str(post), confidence)
        r.append(x)

    return i, r


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, "r") as file_iter:
        for line in file_iter:
            record = frozenset(map(int, line.split()))
            yield record


def getParser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--inputFile",
        dest="input",
        help="filename containing csv",
        default="input.txt",
        type=str
    )
    parser.add_argument(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.5,
        type=float,
    )
    parser.add_argument(
        "-c",
        "--minConfidence",
        dest="minC",
        help="minimum confidence value",
        default=0.66,
        type=float,
    )
    return parser.parse_args()


def main():
    args = getParser()
    inFile = dataFromFile(args.input)
    items, rules = runApriori(inFile, args.minS, args.minC)
    printResults(items, rules)
    _, rule = toStrResults(items, rules)
    with open(f'result_{args.input}','w') as tfile:
	    tfile.write('\n'.join(rule))


if __name__ == "__main__":
    main()
