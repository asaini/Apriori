"""
Python implementation of the Apriori Algorithm
Author : Abhinav Saini
Email  : abhi488@gmail.com

Usage:
	$python apriori.py DATASET.csv minSupport minConfidence

"""
import sys
import re
from itertools	 import chain, combinations
from collections import defaultdict


def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr,i + 1) for i,a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
	"""calculates the support for items in the itemSet and returns a subset of the itemSet 
	each of whose elements satisfies the minimum support"""
	_itemSet = set()
	localSet = defaultdict(int)

	for item in itemSet:
		for transaction in transactionList:
			if item.issubset(transaction):
				freqSet[item] 	+= 1
				localSet[item]	+= 1
	
	for item,count in localSet.items():
		support = float(count)/len(transactionList)
		
		if support >= minSupport:
			_itemSet.add(item)
	
	return _itemSet



def joinSet(itemSet,length):
	"""Join a set with itself and returns the n-element itemsets"""
	return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


if __name__ == "__main__":

	if len(sys.argv) < 4:
		print 'Insufficient Arguments'
	dataFile 	= open(sys.argv[1],'r')
	data		= dataFile.read()

	minSupport	= float(sys.argv[2])
	minConfidence	= float(sys.argv[3])

	#print minSupport, minConfidence

	transactionList	= list()
	itemSet		= set()
	freqSet		= defaultdict(int)
	largeSet	= dict()				# Global dictionary which stores (key=n-itemSets,value=support) which satisfy minSupport
	assocRules 	= dict()				# Dictionary which stores Association Rules

	data_split	= re.split('\r\n|\r|\n',data)	
	for line in data_split:
		line = line.rstrip(',')				# Remove trailing comma
		transaction = frozenset(line.split(','))
		transactionList.append(transaction)
		#print transaction	
		for item in transaction:
			itemSet.add(frozenset([item]))		# Generate 1-itemSets
			#print item

	oneCSet		= returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)

	currentLSet	= oneCSet
	k = 2
	while(currentLSet != set([])):
		largeSet[k-1] = currentLSet
		currentLSet = joinSet(currentLSet,k)
		currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
		currentLSet = currentCSet
		#print currentLSet
		#print '\n\n'
		k = k + 1


	def getSupport(item):
		"""Returns the support of an item"""
		return float(freqSet[item])/len(transactionList)

	print 'Large ItemSets, minSupport = ', minSupport, '\n'
	for key,value in largeSet.items():
		for item in value:
			output = repr(item)
			output = re.sub('"','',output)
			output = re.sub("(frozenset|\(|\)|')",'',output)
			
			if len(item) > 1:
				_subsets = [x for x in subsets(item)]
				#print output, getSupport(item), map(frozenset,_subsets)
				print output, ',', getSupport(item)
			else:
				print output, ',', getSupport(item)

		#print '\n'
	
	for key,value in largeSet.items()[1:]:
		for item in value:
			_subsets = map(frozenset,[x for x in subsets(item)])
			for element in _subsets:
				assocRule = set()
				remain = item.difference(element)
				if len(remain)>0:
					confidence = getSupport(item)/getSupport(element)
					if confidence >= minConfidence:
						output = repr(element) + ' ==> ' + repr(remain)
						output = re.sub('"','',output)
						output = re.sub("(frozenset|\(|\)|')",'',output)
						assocRules[output] = (confidence,getSupport(item))

	print '\n\nHigh Confidence Association Rules, minConfidence = ', minConfidence, '\n'
	for item in sorted(assocRules, key = assocRules.get, reverse = True):
		print item,'(Conf:',assocRules[item][0],' Supp:',assocRules[item][1],')'

