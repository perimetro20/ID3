import sys
from math import log2


class Node:
    def __init__(self, label):
        self.attribute = None
        self.label = label
        self.childs = {}


attribute_values = {}
attribute_list = []
data = []
data_reading = False


def calculate_best_attribute(examples, attributes):
    best_information_gain = -100000.00
    best_attribute = None

    for attribute in attributes:
        info_gain = calculate_information_gain(examples, attribute)
        if info_gain > best_information_gain:
            best_information_gain = info_gain
            best_attribute = attribute

    if attribute:
        return best_attribute

def calculate_information_gain(examples, attribute):
    current_entropy = calculate_entropy(examples)
    index_of_attribute = attribute_list.index(attribute)

    proporcionate_total = 0.0

    for value in attribute_values[attribute]:
        subset = []
        count = 0.0
        for example in examples:
            if example[index_of_attribute] == value:
                subset.append(example)
                count += 1.0

        px = count / float(len(example))
        proporcionate_total += px * calculate_entropy(subset)

    return current_entropy - proporcionate_total


def calculate_entropy(examples):
    counts = {}
    total_entropy = 0.0

    for row in examples:
        counts[row[-1]] = counts.get(row[-1], 0) + 1

    for key, value in counts.items():
        px = float(value) / float(len(examples))
        total_entropy += -1 * px * log2(px)

    return total_entropy


def id3(examples, attributes):
    # Create a root node for the tree
    root = Node(None)

    results = []
    for example in examples:
        results.append(example[-1])

    # if all examples are the same, return
    # the single-node tree Root, with label
    # the single answer.
    if len(set(results)) == 1:
        root.label = results[0]
        return root

    # If number of predicting attributes is empty
    # then Return the single node tree Root, with
    # label = most common value of the target
    # attribute in the examples.
    
    counts = {}
    for element in results:
        counts[element] = counts.get(element, 0) + 1
    
    most_common = None
    most_appearances = -1
    for key, value in counts.items():
        if value > most_appearances:
            most_appearances = value
            most_common = key

    if len(attributes) == 0:
        root.label = most_common
        return root

    # Otherwise Begin
    a = calculate_best_attribute(examples, attributes)
    root.attribute = a
    index_of_attribute = attribute_list.index(a)
    for vi in attribute_values[a]:
        subset = []
        for example in examples:
            if example[index_of_attribute] == vi:
                subset.append(example)

        if len(subset) == 0:
            root.childs[vi] = Node(most_common)
        else:
            root.childs[vi] = id3(subset, attributes - set([a]))

    return root


def print_tree(tree, number_of_tabs):

    tabs = ' ' * 2 * number_of_tabs
    if len(tree.childs) == 0:
        print('{}ANSWER: {}'.format(tabs, tree.label))
    else:
        for child, node in tree.childs.items():
            print('{}{}: {}'.format(tabs, tree.attribute, child))
            print_tree(node, number_of_tabs + 1)
            

for line in sys.stdin:
    if line[0] is not '%':
        line = line.strip()
        if len(line):
            if data_reading:
                line = line.split(',')
                data.append(line)
            elif line.startswith('@relation'):
                line = line.split()
                relation = line[1]
            elif line.startswith('@attribute'):
                line = line[11:]
                line = line.replace('{', "")
                line = line.replace('}', "")
                line = line.replace(',', "")
                line = line.split()
                attribute = line[0]
                attribute_values[attribute] = line[1:]
                attribute_list.append(attribute)
            elif line.startswith('@data'):
                data_reading = True

attribute_list = attribute_list[:-1]
decision_tree = id3(data, set(attribute_list))

print_tree(decision_tree, 0)