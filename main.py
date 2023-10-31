from collections import defaultdict
import time
start_time = time.time()
class FPNode:
    def __init__(self, item, count=1):
        self.item = item
        self.count = count
        self.parent = None
        self.children = {}
        self.link = None  # New attribute for maintaining link references


def construct_fptree(transactions, min_support):
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1

    frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}
    frequent_items_sorted = sorted(frequent_items, key=lambda x: frequent_items[x], reverse=True)

    root = FPNode('null', 0)
    header_table = {item: [None, None] for item in frequent_items_sorted if item != 'null'}  # Only initialize for frequent items

    for transaction in transactions:
        sorted_items = [item for item in transaction if item in frequent_items]
        sorted_items.sort(key=lambda x: (frequent_items[x], x), reverse=True)
        current_node = root

        for item in sorted_items:
            if item in current_node.children:
                current_node = current_node.children[item]
                current_node.count += 1
            else:
                new_node = FPNode(item, 1)
                current_node.children[item] = new_node
                new_node.parent = current_node
                current_node = new_node

                # Update the link references in the header table
                if header_table.get(item):
                    if header_table[item][0] is None:
                        header_table[item][0] = new_node
                    else:
                        last_node = header_table[item][1]
                        last_node.link = new_node
                    header_table[item][1] = new_node

    return root, header_table


def generate_conditional_pattern_base(node):
    conditional_pattern_base = []
    while node is not None:
        path = []
        parent = node.parent
        while parent.item != 'null':
            path.append(parent.item)
            parent = parent.parent
        if path:
            conditional_pattern_base.append(path[::-1])
        node = node.link
    return conditional_pattern_base


def generate_conditional_transactions(conditional_pattern_base, min_support):
    item_counts = defaultdict(int)
    for path in conditional_pattern_base:
        for item in path:
            item_counts[item] += 1

    conditional_transactions = []
    for path in conditional_pattern_base:
        transaction = [item for item in path if item_counts[item] >= min_support]
        if transaction:
            conditional_transactions.append(transaction)

    return conditional_transactions



def mine_frequent_patterns(header_table, prefix, min_support, frequent_patterns, pattern_lengths):
    sorted_items = sorted(header_table.keys(), key=lambda x: header_table[x][0].count)
    for item in sorted_items:
        support = header_table[item][0].count
        if support >= min_support and item != 'null':
            new_frequent_set = prefix.copy()
            new_frequent_set.add(item)
            frequent_patterns.append((new_frequent_set, support))

            # Update pattern_lengths based on the length of new_frequent_set
            pattern_lengths.setdefault(len(new_frequent_set), 0)
            pattern_lengths[len(new_frequent_set)] += 1

            conditional_root = header_table[item][0]
            conditional_pattern_base = generate_conditional_pattern_base(conditional_root)
            conditional_transactions = generate_conditional_transactions(conditional_pattern_base, min_support)

            if conditional_transactions:
                conditional_root, conditional_header_table = construct_fptree(conditional_transactions, min_support)
                mine_frequent_patterns(conditional_header_table, new_frequent_set, min_support, frequent_patterns, pattern_lengths)


root, header_table = construct_fptree(transactions, min_support)
frequent_patterns = []
pattern_lengths = {}  # Initialize pattern_lengths dictionary
mine_frequent_patterns(header_table, set(), min_support, frequent_patterns, pattern_lengths)

# Count the total number of patterns
total_patterns = sum(pattern_lengths.values())

# Print the counts of patterns of different lengths
for length, count in pattern_lengths.items():
    print(f"Number of {length}-length patterns: {count}")

print(f"Total number of patterns: {total_patterns}")


min_support = 50
transactions = []
item_list = defaultdict(int)






end_time = time.time()
execution_time = end_time - start_time

print(f"Execution time: {execution_time} seconds")

with open("pumsb_star.dat.txt") as f:
    for line in f:
        transaction = line.strip().split()
        transactions.append(transaction)
        for item in transaction:
            item_list[item] += 1

output_file = open("output_file.txt", "w")


def print_tree(node, indent=''):
    if node.item is not None:
        print(indent + str(node.item) + ' ' + str(node.count), file=output_file)
        indent += '  '
        for child in node.children.values():
            print_tree(child, indent)


def printTranc():
    for inc, x in enumerate(transactions):
        if not x:
            continue
        print("Transaction {}: ".format(inc), end="", file=output_file)
        x.sort()
        print(' '.join(x), file=output_file)


def headertable():
    print(file=output_file)
    print('Header Table', file=output_file)
    print(file=output_file)
    for item, count in item_list.items():
        if count >= min_support:
            support = count
            print("Item: {}, Support: {}".format(item, support), file=output_file)


def print_frequent_patterns(frequent_patterns):
    print("Frequent Patterns:", file=output_file)
    for pattern, support in frequent_patterns:
        pattern_str = ', '.join(pattern)
        print("Pattern: {}, Support: {}".format(pattern_str, support), file=output_file)


numoftran = len(transactions)  # Update the number of transactions
transactions = transactions[:numoftran]  # Remove empty initial elements

for i in range(numoftran):
    transactions[i].sort()

printTranc()
headertable()

root, header_table = construct_fptree(transactions, min_support)
frequent_patterns = []
#mine_frequent_patterns(header_table, set(), min_support, frequent_patterns)

print_frequent_patterns(frequent_patterns)
print_tree(root)

output_file.close()

