# -*-coding:utf-8-*-
import time
import csv

def loadDataDict():
    """
    load data from file
    :param filename: filename
    :return:  Dataset is a dict{(transcation):count,...}
    """
    Data_itemsets = [[1, 2, 4], [1, 2, 9], [1, 3, 5], [1, 3, 9], [1, 4, 7], [1, 5, 8], [1, 6, 7],
               [1, 7, 9], [1, 8, 9], [2, 3, 5], [2, 4, 7], [2, 5, 6], [2, 5, 7], [2, 5, 8],
               [2, 6, 7], [2, 6, 8], [2, 6, 9], [2, 7, 8], [3, 4, 5], [3, 4, 7], [3, 5, 7],
               [3, 5, 8], [3, 6, 8], [3, 7, 9], [3, 8, 9], [4, 5, 7], [4, 5, 8], [4, 6, 7],
               [4, 6, 9], [4, 7, 8], [5, 6, 7], [5, 7, 9], [5, 8, 9], [6, 7, 8], [6, 7, 9]]
    # Data_itemsets = [[1, 4, 5], [1, 2, 5], [4, 5, 8], [1, 3, 6], [2, 3, 4],
    #                  [5, 6, 7], [3, 4, 5], [3, 5, 6], [3, 5, 7], [6, 8, 9], [3, 6, 7]]

    return Data_itemsets


class HNode:
    """
    abstract a HNode, representing the node in a hash tree,contains 3 attribute:
        (1)isLeaf, when instantiate a new Node, the default is True
        (2) bucket, the item will be contained in the bucket before the number smaller than the max_leaf_cnt
        (3) when the number in bucket exceed the max_leaf_cnt, the item in bucket will be split into different children
            (based on the remainder divided by max_child_cnt)
    """
    def __init__(self):
        self.children = {}
        self.isLeaf = True
        self.bucket ={}
        self.extralist = []


class HTree:
    """
    Wrapper class for HTree instance
    """
    def __init__(self, max_child_cnt, max_leaf_cnt):
        self.root = HNode()  # the root is a HNode
        self.max_child_cnt = max_child_cnt
        self.max_leaf_cnt = max_leaf_cnt

    def insert(self, itemset):
        """
        set can't be hashed we need to convert this into tuple
        which can be easily hashed in leaf node buckets
        :param itemset: type is list[]
        :return: itemset: type is tuple()
        """
        itemset = tuple(itemset)
        self.recur_insert(self.root, itemset, 0, 0)

    def hash(self, value):
        """
        operate the hash function
        :param value: the value that should be operated
        :return: the remainder
        """
        remainder = value % self.max_child_cnt
        return remainder

    def recur_insert(self, node, itemset, index, cnt):
        """
        Recursively adds nodes inside the tree and if required splits leaf node and
        redistributes itemsets among child converting itself into intermediate node.
        :param node: the node(position) that should be inserted
        :param itemset: the itemset that should be inserted
        :param index: the position of itemset that should be divided to choose the route
        :param cnt: the number of items now in node.bucket
        :return:
        """
        if node.isLeaf:
            if itemset in node.bucket:
                node.bucket[itemset] += cnt
            else:
                node.bucket[itemset] = cnt
            # bucket has reached its maximum capacity and its intermediate node so
            # split and redistribute entries.
            if len(node.bucket) > self.max_leaf_cnt:
                for old_itemset, old_cnt in node.bucket.items():
                    if index < 3:
                        hash_key = self.hash(old_itemset[index])
                        if hash_key not in node.children:
                            node.children[hash_key] = HNode()
                        new_index = index + 1
                        if new_index <= len(old_itemset):
                            self.recur_insert(node.children[hash_key], old_itemset, new_index, old_cnt)
                    else:
                        node.extralist.append(old_itemset)
                # until now,all the items in the bucket have been splited into different children,
                # so we can delete the bucket
                del node.bucket
                # when the node have children, the node will not be leafNode
                node.isLeaf = False
        else:
            if index < 3:
                hash_key = self.hash(itemset[index])
                if hash_key not in node.children:
                    node.children[hash_key] = HNode()
                new_index = index + 1
                if new_index <= len(itemset):
                    self.recur_insert(node.children[hash_key], itemset, new_index, cnt)
            else:
                node.extralist.append(itemset)


def generate_hash_tree(Data_itemsets, length, max_leaf_cnt=3, max_child_cnt=3):
    """
    This function generates hash tree of itemsets with each node having no more than child_max_length
    childs and each leaf node having no more than max_leaf_length.
    :param Data_itemsets: the itemsets that should be inserted into the tree
    :param length: length of each itemset
    :param max_leaf_cnt:
    :param max_child_cnt:
    :return: htree
    """
    htree = HTree(max_child_cnt, max_leaf_cnt)
    for itemset in Data_itemsets:
        htree.insert(itemset)
    return htree


def nested_list(htree):
    """
    output the nested list of the hash tree
    :param htree: the generated HTree
    :return:
    """
    node = htree.root
    nested_list = print_tree(node)
    return nested_list


def print_tree(node):
    """
    put the list in all hierarchical of node into the list
    :param node: the node
    :return:
    """
    lst = []
    # Step1: if the node.isLeaf is still True, means all the list of it contained in the bucket
    if node.isLeaf:
        itemset = node.bucket.keys()
        for item in itemset:
            item = list(item)
            lst.append(item)
    # Step2: if the node.isLeaf is not true, means the node has been splited,and may have 2 condition:
    # (1) the node still have children, then we should Recursive process
    # (2) the node don't have children(the node can't be splited by index),
    # means all the list of it contained in the extralist
    else:
        if node.children:
            for i in sorted(range(len(node.children))):
                lst.append(print_tree(node.children[i]))
        else:
            lst.append(node.extralist)
    if len(lst) == 1:
        lst = lst[0]
    return lst


def data_write_csv(filename, datas):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for data in datas:
            writer.writerow([data])
    print('save file successfully')


if __name__ == '__main__':
    start = time.clock()
    Data_itemsets = loadDataDict()
    htree = generate_hash_tree(Data_itemsets, length=3, max_leaf_cnt=3, max_child_cnt=3)
    nested_list = nested_list(htree)
    elapsed_1 = time.clock() - start
    data_write_csv('submissive_1.csv', nested_list)
    print("Running time is:", elapsed_1)
    print(nested_list)



