#!/bin/env python
import os, sys

def change_fasta_headers(directory):
    """
    Changes the headers in all FASTA files within the specified directory.

    :param directory: Path to the directory containing FASTA files.
    """
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".fasta") or filename.endswith(".fa"):
            filepath = os.path.join(directory, filename)
            
            # Extract the part of the filename before the first underscore
            prefix = filename.split("_")[0]
            
            # Read the original file
            with open(filepath, "r") as file:
                lines = file.readlines()
            
            # Process each line to change headers
            new_lines = []
            for line in lines:
                if line.startswith(">"):
                    # Create the new header using the prefix and the original header
                    original_header = line[1:].strip()
                    new_header = f"{prefix}_{original_header}"
                    new_lines.append(f">{new_header}\n")
                else:
                    new_lines.append(line)
            
            # Write the changes to a new file or overwrite the original
            with open(filepath, "w") as file:
                file.writelines(new_lines)

# Usage
directory_path = sys.argv[1]  # Update with your directory path
change_fasta_headers(directory_path)

print("FASTA headers have been updated successfully.")
