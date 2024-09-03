#!/bin/env python
import dendropy
from dendropy.calculate import treecompare
import csv

# Create a shared taxon namespace
taxon_namespace = dendropy.TaxonNamespace()

# Define the tree file paths
tree_files = {
    "FastTree": "fasttree/SNPs_fasttree.tree",
    "iqtree JC69": "iqtree/JC69/SNPs_iqtree_JC69.fa.tree",
    "iqtree JC69+ASC": "iqtree/JC69_ASC/SNPs.fa.varsites.phy_iqtree_JC69_ASC.tree",
    "iqtree GTR": "iqtree/GTR/SNPs_iqtree_GTR.fa.tree",
    "iqtree GTR+ASC": "iqtree/GTR_ASC/SNPs.fa.varsites.phy_iqtree_GTR_ASC.tree"
}

# Load trees into a dictionary
trees = {name: dendropy.Tree.get_from_path(path, "newick", taxon_namespace=taxon_namespace) for name, path in tree_files.items()}

# Encode bipartitions for each tree
for tree in trees.values():
    tree.encode_bipartitions()

# Prepare to write the output to a CSV file
output_file = 'tree_comparison_results.csv'
with open(output_file, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write the header row
    csv_writer.writerow(["Tree 1", "Tree 2", "Euclidean Distance", "Robinson-Foulds Distance"])

    # Compare each tree with every other tree
    tree_names = list(trees.keys())
    for i in range(len(tree_names)):
        for j in range(i + 1, len(tree_names)):  # Compare each pair only once
            t1, t2 = tree_names[i], tree_names[j]
            euclidean_distance = treecompare.euclidean_distance(trees[t1], trees[t2])
            rf_distance = treecompare.robinson_foulds_distance(trees[t1], trees[t2])

            # Print the distances
            print(f"{t1} vs. {t2} Euclidean distance: {euclidean_distance}")
            print(f"{t1} vs. {t2} Robinson-Fould's distance: {rf_distance}")

            # Write the results to the CSV file
            csv_writer.writerow([t1, t2, euclidean_distance, rf_distance])

print(f"Comparison results have been saved to '{output_file}'.")
