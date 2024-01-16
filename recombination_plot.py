#!/bin/env python
import sys, os
import matplotlib.pyplot as plt
import pandas as pd
from Bio import Phylo
import numpy as np

# Since the environment has been reset, let's start by re-reading the GFF file to get the full recombination data.
gff_file_path = 'gubbins.recombination_predictions.gff'

# Read the GFF file
with open(gff_file_path, 'r') as file:
    gff_lines = file.readlines()

# Parse the GFF file to extract recombination data
recombination_data = []

for line in gff_lines:
    if line.startswith('#'):
        continue  # Skip header lines
    parts = line.split('\t')
    taxa = parts[-1].split(';')[2].split('=')[1].strip('\"') 
    start = int(parts[3])
    end = int(parts[4])
    recombination_data.append([taxa, start, end])

# Convert the parsed data into a DataFrame
full_recombination_df = pd.DataFrame(recombination_data, 
                                     columns=['Taxa', 'Start', 'End'])

# Ensure all unique taxa from the list are represented
taxa_list = [
    "3001284746", "3001964113", "3002023864", "3002023865", "3002023871",
    "3002023874", "3002023876", "3002023878", "3003781053", "3003781054",
    "3003787861", "3003787862", "3003787863", "3003787894", "3003787895",
    "3003787897", "3003787898", "3003787899", "3003787907", "3003787912",
    "3003787937", "GCF_000959265.1", "GCF_001885195.1", "GCF_002110925.1",
    "GCF_002110945.1", "GCF_002110965.1", "GCF_002110985.1", "GCF_002111005.1",
    "GCF_002111025.1", "GCF_002111045.1", "GCF_002111065.1", "GCF_002111085.1",
    "GCF_002111105.1", "GCF_002111125.1", "GCF_002111145.1", "GCF_002111165.1",
    "GCF_002111185.1", "GCF_002111205.1", "GCF_002111245.1", "GCF_002111265.1",
    "GCF_002111285.1", "GCF_002111305.1", "GCF_002111325.1", "GCF_002111345.1",
    "GCF_002111385.1", "GCF_002113945.1", "GCF_002115385.1", "GCF_003583425.1",
    "GCF_003583435.1", "GCF_003584055.1", "GCF_003584065.1", "GCF_003813825.1",
    "GCF_003813945.1", "GCF_003854325.1", "GCF_003858035.1", "GCF_003944665.1",
    "GCF_006542565.1", "GCF_006542585.1", "GCF_007995115.1", "GCF_013265625.1",
    "GCF_013265665.1", "GCF_013265695.1", "GCF_015714675.1", "GCF_016092155.1",
    "GCF_016617505.1", "GCF_023383335.1"
]

# Filtering the DataFrame to only include the taxa from the provided list
filtered_recombination_df = full_recombination_df[full_recombination_df['Taxa'].isin(taxa_list)]

# Create a mapping of taxa to y-axis values for plotting
filtered_taxa_to_y = {taxa: i for i, taxa in enumerate(taxa_list)}

# Creating the enhanced plot
plt.figure(figsize=(10, 6))  # Adjusting figure size


# Generating a colormap
n_taxa = len(taxa_list)
cmap_name = 'twilight'  # You can use other colormaps like 'viridis', 'inferno', etc.
cmap = plt.get_cmap(cmap_name)

# Create a list of evenly spaced values to map to colors
color_values = np.linspace(0, 1, n_taxa)

# Plotting the recombination events as color blocks with unique colors
for i, (taxa, group) in enumerate(filtered_recombination_df.groupby('Taxa')):
    color = cmap(color_values[i])  # Use the color_values to map to colors in the colormap
    for _, row in group.iterrows():
        y = filtered_taxa_to_y[row['Taxa']]
        plt.fill_between([row['Start'], row['End']], 
                         y - 0.4, y + 0.4, color=color, alpha=0.75)

# Setting up the plot aesthetics
plt.yticks(range(len(taxa_list)), taxa_list, fontsize=5)  # Increased font size for y-ticks
plt.xlabel('Sequence Position', fontsize=12)
plt.ylabel('Taxa', fontsize=12)
plt.title('Recombination Events for Provided Taxa', fontsize=14)
plt.grid(True)  # Enabling grid lines

# Saving the enhanced plot
plot_path = 'recombination_plot_enhanced.png'
plt.savefig(plot_path)
