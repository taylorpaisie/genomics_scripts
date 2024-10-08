#!bin/env python
import os, sys

# Path to your text file containing the list of SRA IDs
sra_id_file = sys.argv[1]

# Directory containing the downloaded FASTQ files
fastq_directory = sys.argv[2]

# Output text files for downloaded and missing SRA IDs
downloaded_output_file = "downloaded_sra_ids.txt"
missing_output_file = "missing_sra_ids.txt"

# Read the SRA IDs from the text file
with open(sra_id_file, 'r') as file:
    sra_ids = {line.strip() for line in file}  # Use a set for efficient lookup

# List all FASTQ files in the directory
fastq_files = os.listdir(fastq_directory)

# Extract SRA IDs from the fastq filenames (assuming a naming convention like SRRXXXXXX_1.fastq, SRRXXXXXX_2.fastq)
downloaded_sra_ids = set()

for filename in fastq_files:
    # Extract the SRA ID from the filename (before the underscore)
    sra_id = filename.split('_')[0]
    downloaded_sra_ids.add(sra_id)

# Find which SRA IDs have already been downloaded
downloaded = sra_ids.intersection(downloaded_sra_ids)

# Find which SRA IDs are missing
missing = sra_ids.difference(downloaded_sra_ids)

# Write the downloaded SRA IDs to a text file
with open(downloaded_output_file, 'w') as f_downloaded:
    for sra_id in downloaded:
        f_downloaded.write(sra_id + '\n')

# Write the missing SRA IDs to a text file
with open(missing_output_file, 'w') as f_missing:
    for sra_id in missing:
        f_missing.write(sra_id + '\n')

print(f"Downloaded SRA IDs saved to {downloaded_output_file}")
print(f"Missing SRA IDs saved to {missing_output_file}")
