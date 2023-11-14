#!/usr/bin/env python
"""This script takes a list of SRA Accessions in the format of a text file. 
This will get and parse the json file related to SRA Accession and output
the queries of interest into a text file. 
BEFORE RUNNING SCRIPT, MUST INSTALL PYSRADB
conda create -c bioconda -n pysradb PYTHON=3.10 pysradb
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


def extract_meta(args):
    if args.input_file:
        # Read SRA Accessions from the input file
        with open(args.input_file, 'r') as file:
            sra = file.read()
    elif args.input_string:
        # Use the provided SRA Accessions as a string
        sra = ' '.join(args.input_string)
    else:
        print("Error: You must provide either an input file or a string.")
        sys.exit(1)

    sra_list = sra.split()  # Split by whitespace
    print(sra_list)

    sras = []
    db = pysradb.SRAweb()

    for meta in sra_list:
        metadata = db.sra_metadata(meta)
        if not metadata.empty:  # Check if the DataFrame is not empty
            sras.append(metadata)
    print(sras)

    if args.display_all_fields:
        all_fields = set()
        for item in sras:
            all_fields.update(item.columns)
        print("\nAll Fields in Metadata:")
        print("\t".join(all_fields))
    else:
        meta_json = json.dumps([m.to_dict(orient="records")[0] for m in sras if not m.empty], indent=2)
        # Parse the JSON string into a list of dictionaries
        data = json.loads(meta_json)
        # Create a dictionary with "run_accession" as the key
        result_dict = {item["run_accession"]: item for item in data}

        with open(args.output, 'w') as output_file:
            # Write column headers to the output file
            column_headers = ["SRR Accession"]
            if args.queries:
                for query in args.queries:
                    column_headers.append(query)
            output_file.write("\t".join(column_headers) + "\n")

            # Iterate through the data and write the desired columns
            for accession, item in result_dict.items():
                values = [accession]
                for query in args.queries:
                    meta_value = item.get(query, "N/A")
                    values.append(meta_value)
                output_file.write("\t".join(values) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Extract metadata from SRA Accessions and write to a text file.",
                                     add_help=False)
    req = parser.add_argument_group('Required')
    req.add_argument("-i", help="List of SRA Accessions to extract metadata info from.",
                     dest="input_file", type=str)
    req.add_argument('-q', help="Metadata query or queries of interest. Provide one or two queries.",
                     dest="queries", type=str, nargs='+')
    req.add_argument("-o", help="Output text file for SRA metadata of interest.",
                      dest="output", type=str)
    opt = parser.add_argument_group('Optional')
    opt.add_argument('-h', '--help', action='help',
                     help='show this help message and exit')
    opt.add_argument('-s', help="SRA Accessions as a string.",
                     dest="input_string", nargs='+')
    opt.add_argument('-d', '--display-all-fields', action='store_true',
                     help="Display all fields present in the generated JSON file.")

    parser.set_defaults(func=extract_meta)
    args = parser.parse_args()

    if args.display_all_fields:
        args.queries = None
        args.output = None

    if not args.input_file and not args.input_string:
        parser.error("You must provide either an input file or a string.")
    if args.queries and len(args.queries) > 2:
        parser.error("Please provide one or two queries using -q.")

    args.func(args)

if __name__ == "__main__":
    main()
    