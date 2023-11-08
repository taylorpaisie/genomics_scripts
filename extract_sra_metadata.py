#!/usr/bin/env python
"""This script is to download SRA metadata json file from a list of SRA Accessions. 
This will download json files related to SRA Accession.
Author: Taylor K. Paisie <ltj8@cdc.gov>
Version: 0.1.0
Date: 2023-11-06
"""

__version="0.1.0"

args = ''
import os, sys, operator, logging, argparse
import numpy, urllib, time
import time, json, csv
import pandas as pd
import glob
import pysradb

def extract_meta(args):
    samples = open(args.ids, 'r')
    sra = samples.read()
    sra_list = sra.split('\n')
    print(sra_list)

    sras = []
    db = pysradb.SRAweb()

    for meta in sra_list:
        metadata = db.sra_metadata(meta)
        sras.append(metadata)
    print(sras)

    meta_json = json.dumps([m.to_dict(orient="records")[0] for m in sras], indent=2)
    # Parse the JSON string into a list of dictionaries
    data = json.loads(meta_json)
    # Create a dictionary with "run_accession" as the key
    result_dict = {item["run_accession"]: item for item in data}

    with open(args.output, 'w') as output_file:
        # Write column headers to the output file
        output_file.write("SRR Accession\t" + args.query1 + "\t" + args.query2 + "\n")
        # Iterate through the data and write the desired columns
        for accession, item in result_dict.items():
            meta_value1 = item.get(args.query1, "N/A")  # Use .get() to provide a default value if the key is not found
            meta_value2 = item.get(args.query2, "N/A")  # Use .get() to provide a default value if the key is not found
            output_file.write(f"{accession}\t{meta_value1}\t{meta_value2}\n")


def main():
    parser = argparse.ArgumentParser(description="Parse a JSON file and output desired columns to a text file.")
    parser.add_argument("-i", help="List of SRA Accessions to extract metadata info from.", dest="ids", type=str, required=True)
    parser.add_argument('-q1', help="First metadata query of interest.", dest="query1", type=str, required=True)
    parser.add_argument('-q2', help="Second metadata query of interest.", dest="query2", type=str, required=True)
    parser.add_argument("-o", help="Output text file for SRA metadata of interest.", dest="output", type=str, required=True)
    parser.set_defaults(func=extract_meta)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

