#!/usr/bin/env python
"""This script is to parse and extract SRA metadata from a json file. 
This will make a text file with your wanted SRA metadata.
Author: Taylor K. Paisie <ltj8@cdc.gov>
Version: 0.1.0
Date: 2023-11-08
"""

__version="0.1.0"

args = ''
import os, sys, operator, logging, argparse
import numpy, urllib, time
import time, json, csv
import pandas as pd
import glob
import pysradb

def parse_json(args):
    with open(args.input, 'r') as file:
        # Parse the JSON content into a Python data structure (list of dictionaries)
        data = json.load(file)

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
    parser.add_argument("-i", help="JSON file with data", dest="input", type=str, required=True)
    parser.add_argument('-q1', help="First metadata query of interest.", dest="query1", type=str, required=True)
    parser.add_argument('-q2', help="Second metadata query of interest.", dest="query2", type=str, required=True)
    parser.add_argument("-o", help="Output file for writing columns", dest="output", type=str, required=True)
    parser.set_defaults(func=parse_json)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
