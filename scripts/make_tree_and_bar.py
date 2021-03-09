import csv
import pickle
import json
import os
import sys

# Dependencies:
# This function automates the creation of a json tree to be displayed using d3 in react from the output of phyloPGM
# Input: df_pgm.csv (or equivalent), species_converter.pkl for converting to english species names
# Output: data.json (or equivalent), a hierarchical json tree that is d3-digestible

input_path = sys.argv[1]


with open(input_path, newline='') as csvfile:
    df_pgm = csv.reader(csvfile, delimiter=',')
    phylo_in = list(df_pgm)

with open('./scripts/species_converter.pkl', 'rb') as f:
    species_converter = pickle.load(f)

# Make a list of all the species that have been output

leaves = []

for each in phylo_in[0]:
    # Hardcoding away the non-species entries... should be okay?
    if each == '' or each == 'ratio_root' or each == 'sanity_sum' or each == 'pgm_pred' or each == 'y':
        continue

    if not each.isupper() and 'branch' not in each:
        leaves.append(each)

# Find the root and make a list of all the extinct species

root = ''
extinct = []

for each in phylo_in[0]:
    if each.isupper():
        extinct.append(each)
        if len(each) > len(root):
            root = each

    if 'branch' in each:
        intermediate = each.split()

# Sorting by length... just to help me understand recursion further down
extinct = sorted(extinct, key=len, reverse=True)

# Parsing the branches that were output by phyloPGM
branch_list = []
for i in range(len(phylo_in[0])):
    if 'branch' in phylo_in[0][i]:
        split = phylo_in[0][i].split('_')
        branch_list.append([split[1], split[2], phylo_in[1][i]])

# Ordering the human-containing nodes that might be flipped:
for each in branch_list:
    if each[0].isupper() and each[1].isupper() and len(each[0]) > len(each[1]):
        each[0], each[1] = each[1], each[0]

    if 'hg38' in each:
        each[0], each[1] = each[1], each[0]

# Making branch_list into a dictionary: child: parent, branch-to-parent value, node value
branches = {}

for each in branch_list:
    branches[each[0]] = [each[1], each[2]]

# Adding the node values
for species in leaves:
    for i in range(len(phylo_in[0])):
        if species == phylo_in[0][i]:
            index = i
            break

    branches[species].append(phylo_in[1][index])

for species in extinct:
    if species == root:
        continue

    for i in range(len(phylo_in[0])):
        if species == phylo_in[0][i]:
            index = i
            break

    branches[species].append(phylo_in[1][index])

# Checkpoint: Now, branches is a dictionary containing all nodes, following the aforementioned [parent, branch val,
# node val]

# Making parents: dictionary as follows, internal node: [child 1, child 2]. This is used for forming the binary tree.
parents = {}
for each in extinct:
    parents[each] = []
    for every in branch_list:
        if each == every[1]:
            parents[each].append(every[0])

# Ordering the children of the parents so that the upper layer is always the prefix
for key in parents:
    child1 = parents[key][0]
    child2 = parents[key][1]

    if child1.isupper() and child2.isupper():
        if not key.startswith(child1):
            parents[key] = [child2, child1]

    elif child1[0].upper() != child2[0].upper():
        # If they have a different first letter, make sure the letters match
        # Note: if they have the same first letter, then it doesn't matter...
        if not key.startswith(child1[0].upper()):
            parents[key] = [child2, child1]

# Now to make the tree
# Note that since the root is excluded from branches, I hardcoded its node score into the starting tree.
tree = {
    'name': root,
    'node_score': phylo_in[1][phylo_in[0].index(root)],
    'children': []
}


# TODO: Add branch weights (each child is given the branch weight between its parent and itself)
# TODO: Fix Rhesus macaque in species conversion
# TODO: Automate inputs and outputs as system I/O for integration into the project

def make_tree_structure(id):
    # This simple function just fills in a hierarchical tree structure rooted at node 'id'
    if id.isupper():
        filled_data = {
            'name': id,
            'node_score': branches[id][2],
            'children': []
        }

    else:
        filled_data = {'name': species_converter[id], 'node_score': branches[id][2]}
    return filled_data


def make_internal_nodes(dicto):
    ancestor = dicto['name']

    if ancestor in parents.keys():
        children = parents[ancestor]

        dicto['children'].append(make_tree_structure(children[0]))
        dicto['children'].append(make_tree_structure(children[1]))

        if children[0].isupper():
            go_up = dicto['children'][0]
            make_internal_nodes(go_up)

        if children[1].isupper():
            go_down = dicto['children'][1]
            make_internal_nodes(go_down)

    return


make_internal_nodes(tree)

# Finally, change the name of the root to Common Ancestor
tree['name'] = 'Common Ancestor'


####
# Making the bar chart
####

# init_score is the initial score of the root (human) before phyloPGM (the ratio)
# sanity_sum is the sum of all scores of the branches by phyloPGM
# pgm_pred is the sum of init_score + alpha*sanity_sum (see main working equation)
# if pgm_pred>0, y is positive (yes label), else negative (no label)

# Extract ratio root and pgm_pred basically

for index in range(len(phylo_in[0])):
    if phylo_in[0][index] == 'ratio_root':
        init_score = float(phylo_in[1][index])

    if phylo_in[0][index] == 'pgm_pred':
        final_score = float(phylo_in[1][index])

    if phylo_in[0][index] == 'sanity_sum':
        sanity_sum = 0.1*float(phylo_in[1][index]) # alpha = 0.1

# print(init_score)
# print(sanity_sum)
# print(final_score)
# print(init_score + sanity_sum)

results = [init_score, final_score, sanity_sum]


# Last but not least...
# Export the tree and bar


with open('./src/client/tree_data.json', 'w') as out:
    json.dump(tree, out)

with open('./src/client/bar_data.json', 'w') as out_two:
    json.dump(results, out_two)