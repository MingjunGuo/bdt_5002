class node(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []

    def add(self, nodes):
        self.children=nodes

    def change_to_node(self, name):
        '''
        change key to node
        :param name: key
        :return: node
        '''
        if name == self.name:
            return self
        else:
            for i in range(len(self.children)):
                t = self.children[i].change_to_node(name)
                if t != None:
                    return t
            return None


# step1: construct the tree
tree = node('abcde', 12)
# layeer1:
node10 = node('abcd', 9)
node11 = node('abce', 10)
node12 = node('abde', 8)
node13 = node('acde', 7)
node14 = node('bcde', 4)
tree.add([node10, node11, node12, node13, node14])

# layer2:
node20 = node('abc', 2.5)
node21 = node('abd', 3)
node22 = node('abe', 5)
node23 = node('acd', 2.8)
node24 = node('ace', 3)
node25 = node('ade', 2.2)
node26 = node('bcd', 2)
node27 = node('bce', 1.9)
node28 = node('bde', 1.7)
node29 = node('cde', 3.7)
node10.add([node20, node21, node22, node23])
node11.add([node20, node22, node24, node27])
node12.add([node21, node22, node25, node28])
node13.add([node23, node24, node25, node29])
node14.add([node26, node27, node28, node29])

# layer3:
node30 = node('ab', 1.9)
node31 = node('ac', 2.1)
node32 = node('ad', 0.5)
node33 = node('ae', 2.1)
node34 = node('bc', 0.7)
node35 = node('bd', 0.3)
node36 = node('be', 1.4)
node37 = node('cd', 0.4)
node38 = node('ce', 1.7)
node39 = node('de', 0.6)
node20.add([node30, node31, node34])
node21.add([node30, node32, node35])
node22.add([node30, node33, node36])
node23.add([node31, node32, node37])
node24.add([node31, node33, node38])
node25.add([node32, node33, node39])
node26.add([node34, node35, node37])
node27.add([node34, node36, node38])
node28.add([node35, node36, node39])
node29.add([node37, node38, node39])

node40 = node('a', 0.1)
node41 = node('b', 0.3)
node42 = node('c', 0.1)
node43 = node('d', 0.2)
node44 = node('e', 0.2)
node30.add([node40, node41])
node31.add([node40, node42])
node32.add([node40, node43])
node33.add([node40, node44])
node34.add([node41, node42])
node35.add([node41, node43])
node36.add([node41, node44])
node37.add([node42, node43])
node38.add([node42, node44])
node39.add([node43, node44])

dict = {'a': 0.1, 'b': 0.3, 'c': 0.1, 'd': 0.2, 'e': 0.2,
        'ab': 1.9, 'ac': 2.1, 'ad': 0.5, 'ae': 2.1, 'bc': 0.7, 'bd': 0.3, 'be': 1.4, 'cd': 0.4, 'ce': 1.7, 'de': 0.6,
        'abc': 2.5, 'abd': 3, 'abe': 5, 'acd': 2.8, 'ace': 3, 'ade': 2.2, 'bcd': 2, 'bce': 1.9, 'bde': 1.7, 'cde': 3.7,
        'abcd': 9, 'abce': 10, 'abde': 8, 'acde': 7, 'bcde': 4,
        'abcde': 12}

initdict = {}
for key in dict:
    initdict[key]=12

maxgain = 0
node_1 = 'a'
node_2 = 'b'
node_3 = 'c'


def cal_gain(initdict, temdict):
    '''
    compute the gain after choosing three nodes.
    :param initdict: the initialization dict
    :param temdict: the temperate dict
    :return: the minus gain
    '''
    gain = 0
    for node in dict.keys():
        gain = gain + initdict[node]-temdict[node]
    return gain


def replace_value(node, temdict, value):
    '''
    change the value from initdict to temdict
    :param node: node
    :param temdict: temdict
    :param value: value for choose node
    :return:
    '''
    if node.children == []:
        return temdict
    for i in range(len(node.children)):
        if temdict[node.children[i].name]>value:
            temdict[node.children[i].name]=value
        temdict = replace_value(node.children[i], temdict, value)
    return temdict


for key1 in dict.keys():
    for key2 in dict.keys():
        if key1 == key2:
            continue
        for key3 in dict.keys():
            if key1 == key3 or key2 == key3:
                continue
            temdict = initdict.copy()
            temdict[key1] = dict[key1]
            temdict[key2] = dict[key2]
            temdict[key3] = dict[key3]
            node1 = tree.change_to_node(key1)
            node2 = tree.change_to_node(key2)
            node3 = tree.change_to_node(key3)
            if node1 != None:
                temdict = replace_value(node1, temdict, temdict[key1])
            if node2 != None:
                temdict = replace_value(node2, temdict, temdict[key2])
            if node3 != None:
                temdict = replace_value(node3, temdict, temdict[key3])
            gain = cal_gain(initdict, temdict)
            if gain > maxgain:
                maxgain = gain
                node_1 = key1
                node_2 = key2
                node_3 = key3

print('the k=3 views are:', node_1, node_2, node_3)
print('MaxGain is:', maxgain)


