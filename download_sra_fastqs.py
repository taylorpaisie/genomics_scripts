#!/bin/env python
import sys
import os
import ftplib

# Load the list of accessions from a file
with open(sys.argv[1], 'r') as file:
    accessions = [line.strip() for line in file]

# Base URL for ENA FTP server
base_url = "ftp.sra.ebi.ac.uk"

# Function to download a single file via FTP
def download_file(ftp_path, local_filename):
    with ftplib.FTP(base_url) as ftp:
        ftp.login()
        try:
            with open(local_filename, 'wb') as local_file:
                ftp.retrbinary(f"RETR {ftp_path}", local_file.write)
            return True
        except ftplib.error_perm as e:
            print(f"Failed to download {local_filename}: {e}")
            return False

# Iterate over accessions and download the corresponding FASTQ files
for accession in accessions:
    # Construct the file paths
    ftp_path_1 = f"/vol1/fastq/{accession[:6]}/00{accession[-1]}/{accession}/{accession}_1.fastq.gz"
    ftp_path_2 = f"/vol1/fastq/{accession[:6]}/00{accession[-1]}/{accession}/{accession}_2.fastq.gz"

    # Download the files
    download_successful_1 = download_file(ftp_path_1, f"{accession}_1.fastq.gz")
    download_successful_2 = download_file(ftp_path_2, f"{accession}_2.fastq.gz")

    if not (download_successful_1 and download_successful_2):
        print(f"Download failed for one or both files of {accession}")


