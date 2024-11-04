# You are allowed to import any modules whatsoever (not even numpy, sklearn etc)
# The use of file IO is forbidden. Your code should not read from or write onto files

# SUBMIT YOUR CODE AS TWO PYTHON (.PY) FILES INSIDE A ZIP ARCHIVE
# THE NAME OF THE PYTHON FILES MUST BE index.py and execute.py

# DO NOT CHANGE THE NAME OF THE METHODS my_index BELOW
# THESE WILL BE INVOKED BY THE EVALUATION SCRIPT. CHANGING THESE NAMES WILL CAUSE EVALUATION FAILURE

# You may define any new functions, variables, classes here
# For example, functions to create indices or statistics
def build_tuples(tuples):
    tuples.sort(key=lambda x: (x[1], x[2]))
    grouped_by_name = []
    disk = list(tuple[0] for tuple in tuples)
    grouped_by_name.append([tuples[0][1], [0, 0], [tuples[0][2]]])
    cur_name = tuples[0][1]
    index = 0
    tuple_index = 1
    while tuple_index < len(tuples):
        if tuples[tuple_index][1] == cur_name:
            grouped_by_name[index][1][1] = tuple_index
            grouped_by_name[index][2].append(tuples[tuple_index][2])
        else:  
            grouped_by_name.append(
                [tuples[tuple_index][1], [tuple_index, tuple_index], [tuples[tuple_index][2]]]
            )
            cur_name = tuples[tuple_index][1]
            index += 1
        tuple_index += 1
    tuples.sort(key=lambda x: (x[2], x[1]))
    disk_years = list(tuple[0] for tuple in tuples)
    disk.extend(disk_years)
    return disk, grouped_by_name

def build_by_year(tuples):
    # Sort tuples if not already sorted by year
    group_by_year = []
    current_index = 0
    total = len(tuples)
    
    for year in range(1900, 2101):
        start = current_index
        
        # Find the range of indices in `tuples` where the year matches `year`
        while current_index < total and tuples[current_index][2] == year:
            current_index += 1
        
        end = current_index - 1 if start < current_index else start - 1
        group_by_year.append([start, end])
    
    return group_by_year


class Node:
    def __init__(self, leaf=False):
        self.ind = 0
        self.leaf = leaf
        self.n_child = 0
        self.children = []
        self.keys = []
        self.next = None


class BTree:
    def __init__(self, n=10):
        self.n = n
        self.leaves = []

    def dfs(self, node):
        if node.leaf == False:
            node.next = None
            for i in node.children:
                self.dfs(i)
        else:
            self.leaves.append(node)
            l = len(self.leaves)
            node.next = None
            node.ind = l - 1

    def create(self, name_group):
        n = self.n
        ind = 0
        while ind < len(name_group):
            if ind == 0:
                cur_name = name_group[0][0]
                head = Node(leaf=True)
                head.keys.append(cur_name)
                head.children.append(name_group[0])
                head.n_child += 1
                cur_node = head
                ind += 1
            else:
                if cur_node.n_child == n:
                    new_node = Node(leaf=True)
                    # cur_node.children.append(new_node)
                    cur_node.next = new_node
                    cur_node = new_node
                cur_node.keys.append(name_group[ind][0])
                cur_node.children.append(name_group[ind])
                cur_node.n_child += 1
                ind += 1
        # leaf nodes created with header = head

        while head.next != None:
            head2 = Node(leaf=False)
            cur_node = head2
            while head.next != None:
                if cur_node.n_child == n:
                    new_node = Node(leaf=False)
                    cur_node.next = new_node
                    cur_node = new_node
                cur_node.keys.append(head.keys[0])
                cur_node.children.append(head)
                cur_node.n_child += 1
                head = head.next
            cur_node.keys.append(head.keys[0])
            cur_node.children.append(head)
            head = head2

        self.dfs(head)
        self.root = head

    def search_level_name(self, name, node):
        if node.leaf == True:
            found = 0
            for i in range(len(node.keys)): 
                if node.keys[i] == name:
                    found = 1
                    break
            if found == 1:
                return node.children[i]
            else:
                return []
        else:
            if node.keys[0] > name:
                return []
            for i in range(1, len(node.keys)):
                if node.keys[i] > name:
                    return self.search_level_name(name, node.children[i - 1])
            return self.search_level_name(name, node.children[len(node.keys) - 1])

    def search_name(self, name):
        root = self.root
        n = self.n
        return self.search_level_name(name, root)

    def lower_bound(self, pattern, node):
        if node.leaf:
            found = 0
            ind = 0
            for i in range(len(node.keys)):  # optimise this task
                if node.keys[i] >= pattern:
                    found = 1
                    return [i, node]
            # node=node.next
            node = self.leaves[node.ind + 1]
            return [0, node]
        else:
            if node.keys[0] >= pattern:
                return self.lower_bound(pattern, node.children[0])
            for i in range(1, len(node.keys)):  # optimise this task
                if node.keys[i] >= pattern:
                    return self.lower_bound(pattern, node.children[i - 1])
            return self.lower_bound(pattern, node.children[len(node.keys) - 1])

    def upper_bound(self, pattern, node):
        if node.leaf:
            for i in range(len(node.keys)):
                if node.keys[i] > pattern:
                    return [i - 1, node]
            return [len(node.keys) - 1, node]
        else:
            if node.keys[0] > pattern:
                return [0, None]
            for i in range(1, len(node.keys)):
                if node.keys[i] > pattern:
                    return self.upper_bound(pattern, node.children[i - 1])
            return self.upper_bound(pattern, node.children[len(node.children) - 1])

    def pattern_search(self, pattern):
        patt_st = pattern[:-1]
        patt_en = patt_st + "zzzzzzzzzzzzzz"
        lb = self.lower_bound(patt_st, self.root)
        ub = self.upper_bound(patt_en, self.root)
        return [lb, ub]




################################
# Non Editable Region Starting #
################################
def my_index(tuples):
################################
#  Non Editable Region Ending  #
################################

    data_size = len(tuples)
    disk, name_group = build_tuples(tuples)
    year_group = build_by_year(tuples)
    btree = BTree(10)
    btree.create(name_group)
    idx_stat = [btree, year_group, data_size]

    return disk, idx_stat