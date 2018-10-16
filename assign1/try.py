# -*-coding:utf-8-*-
import csv
import time


def loadDataDict(filename):
    """
    load data from file
    :param filename: filename
    :return:  Dataset is a dict{(transcation):count,...}
    """
    filename = filename
    # load data from given file,type is list
    with open(filename) as f:
        DataSet = csv.reader(f)
    # transform the datatype to dict
        DataDict = {}
        for transaction in DataSet:
            if frozenset(transaction) in DataDict.keys():
                DataDict[frozenset(transaction)] += 1
            else:
                DataDict[frozenset(transaction)] = 1
    return DataDict


# define a tree,and save every node
class treeNode:
    """
    define a class, every node will have some attributes:
        name:the name of node
        count: the number of node occurance
        ParentNode : the ParentNode
        ChildrenNode: the ChildrenNode, the type is dict
        NodeLink: the similar node in different transaction, The default is None
     and some function:
        inc: plus the numOccurance
        disp: print the tree
    """
    def __init__(self, name, numOccur, ParentNode):
        self.name = name
        self.count = numOccur
        self.ParentNode = ParentNode
        self.ChildrenNode = {}
        self.NodeLink = None

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print(''*ind, self.name, '', self.count)
        for child in self.ChildrenNode.values():
            child.disp(ind + 1)


def updateHeader(originalNode, targetNode):
    """
    connecting the similar treeNode together
    :param originalNode: the treeNode
    :param targetNode: the treeNode that should be connected
    :return:
    """
    while(originalNode.NodeLink != None):
        originalNode = originalNode.NodeLink
    originalNode.NodeLink = targetNode


def updateTree(items, intree, headerTable, count):
    """
    Update Tree with every transaction, updating process can be split into three steps:
        (1) if the items[0] has already been the childrenNode of intree, then update the numOccur of Items[0]
        (2) else: construct the new treeNode,and update the headerTable
        (3) loop step(1) and step(2) until there is no item in items
    :param items: one transaction after filtering by minSup
    :param intree: the items[0]'s parentNode
    :param headerTable: headerTable:{item:[count, header of NodeLink],...}
    :param count: the count of this transaction
    :return:
    """
    # Step1:
    if items[0] in intree.ChildrenNode:
        intree.ChildrenNode[items[0]].inc(count)
    # Step2:
    else:
        intree.ChildrenNode[items[0]] = treeNode(items[0], count, intree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = intree.ChildrenNode[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], intree.ChildrenNode[items[0]])
    # Step3:
    if len(items) > 1:
        updateTree(items[1:], intree.ChildrenNode[items[0]], headerTable, count)


def createTree(DataDict, minSup=300):
    """
    creating FP-Tree can be split into three steps:
        (1) Traverse the DataSet, count the number of occurrences of each item, create a header-table
        (2) Remove items in the headerTable that do not meet the minSup
        (3) Traverse the DataSet again, create the FP-tree
    :param DataSet: dict{(transaction):count,...}
    :param minSup: minimum support
    :return:rootTree, headerTable
    """
    # Step 1:
    headerTable = {}
    for transaction in DataDict:
        for item in transaction:
            headerTable[item] = headerTable.get(item, 0) + DataDict[transaction]
    # del item whose value is Nan:
    key_set = set(headerTable.keys())
    for key in key_set:
        if key is '':
            del(headerTable[key])
    # Step 2:
    key_set = set(headerTable.keys())
    for key in key_set:
        if headerTable[key] < minSup:
            del(headerTable[key])
    # if the headerTable is None, then return None, None
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    # plus one value for the item to save the NodeLink
    for key in headerTable:
        headerTable[key] = [headerTable[key], None]
    # Instantiate the root node
    rootTree = treeNode('Null Set', 1, None)
    # Step 3:
    for transaction, count in DataDict.items():
        localID = {}
        for item in transaction:
            if item in freqItemSet:
                localID[item] = headerTable[item][0]
        if len(localID) > 0:
            orderedItems = [v[0] for v in sorted(localID.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, rootTree, headerTable, count)
    return rootTree, headerTable


def ascendTree(leafNode, prefixPath):
    """
    Treat every transaction as a line, connecting from leafnode to rootnode
    :param leafNode: leafnode
    :param prefixPath: path ending with leafnode
    :return:
    """
    if leafNode.ParentNode != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.ParentNode, prefixPath)


def findPrefixPath(baseitem, treeNode):
    """
    find conditional pattern base(collection of paths ending with baseitem being looked up) for every frequent item
    :param baseitem: frequent item
    :param treeNode: the header of NodeLink in headerTable
    :return: condPats:conditional pattern base
    """
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.NodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, prefix, freqItemList):
    """
    after constructing the FP-Tree and conditional FP-tree, loop for look for frequent ItemSets
    :param inTree: the dataset created by createTree
    :param headerTable: the FP-Tree
    :param minSup: the minimum support
    :param prefix: used to save current prefix, should be pass set([]) at first
    :param freqItemList: used to save frequent itemsets, should be pass list[] at first
    :return:
    """
    items = [v[0] for v in sorted(headerTable.items(), key=lambda p:p[1][0])]
    for baseitem in items:
        newFreqSet = prefix.copy()
        newFreqSet.append(baseitem)
        freqItemList.append(newFreqSet)
        condPats = findPrefixPath(baseitem, headerTable[baseitem][1])
        myCondTree, myHeadTable = createTree(condPats, minSup)
        if myHeadTable != None:
            mineTree(myCondTree, myHeadTable, minSup, newFreqSet, freqItemList)


def from_Itemset(freqItems, rootTree, headerTable, minSup):
    """
    Based on the result of frequent Itemset, print out those FP-conditional trees whose height is larger than 1
    :param freqItems: the result of finding frequent Itemset
    :return: the FP-conditional trees , put in one list
    """
    # Step1: find all the items that the FP-conditional trees whose height is larger than 1
    FP_items = []
    for items in freqItems:
        if len(items) > 1:
            FP_items.append(items[0])
    # Step2: Remove duplicates
    FP_items = list(set(FP_items))
    # Step3: find the conditional-tree of every item
    lst_all = []
    for baseitem in FP_items:
        condPats = findPrefixPath(baseitem, headerTable[baseitem][1])
        myCondTree, myHeadTable = createTree(condPats, minSup)
        lst = from_node(myCondTree)
        lst_all.append(lst)
    return lst_all


def from_node(node):
    """
    from every node whose conditional tree is higher than 1, print the conditional tree into list
    :param node:
    :return:
    """
    lst = []
    combination = node.name + ' ' + str(node.count)
    lst.append(combination)
    if node.ChildrenNode:
        lst_children = []
        Item_set = set(node.ChildrenNode.keys())
        for Item in Item_set:
            node_new = node.ChildrenNode[Item]
            lst_new = from_node(node_new)
            lst_children.append(lst_new)
        lst.append(lst_children)
    if len(lst) == 1:
        lst = lst[0]
    return lst


def fpTree(DataDict, minSup=300):
    """
    package all the function into the main function
    :param DataDict: the input file
    :param minSup: the minimum support
    :return: freqItems\FP-conditional trees
    """
    rootTree, headerTable = createTree(DataDict, minSup)
    freqItems = []
    prefix = []
    mineTree(rootTree, headerTable, minSup=300, prefix=prefix, freqItemList=freqItems)
    lst_all = from_Itemset(freqItems, rootTree, headerTable, minSup=300)
    # print_fp_all = print_fp(rootTree, headerTable, minSup=300)
    return freqItems, lst_all


def data_write_csv(filename, datas):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for data in datas:
            writer.writerow([data])
    print('save file successfully')


if __name__ == '__main__':
    start = time.clock()
    DataDict = loadDataDict('groceries.csv')
    freqItems, lst_all = fpTree(DataDict)
    data_write_csv('submissive_2.1.csv', freqItems)
    data_write_csv('submissive_2.2.csv', lst_all)
    elapsed_1 = time.clock() - start
    print("Running time is:", elapsed_1)
    print(freqItems)
    print(len(freqItems))
    print(len(lst_all))
    print(lst_all)













