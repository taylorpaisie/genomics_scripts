#!/usr/bin/env python
"""This script takes a list of SRA Accessions in the format of a text file. 
This will get and parse the json file related to SRA Accession and output
the queries of interest into a text file. 
BEFORE RUNNING SCRIPT, MUST INSTALL PYSRADB
conda create -c bioconda -n pysradb PYTHON=3.10 pysradb
Author: Taylor K. Paisie <ltj8@cdc.gov>
Version: 0.1.0
Date: 2023-11-09
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
        column_headers = ["SRR Accession"]
        if args.query1:
            column_headers.append(args.query1)
        if args.query2:
            column_headers.append(args.query2)
        output_file.write("\t".join(column_headers) + "\n")
        
        # Iterate through the data and write the desired columns
        for accession, item in result_dict.items():
            values = [accession]
            if args.query1:
                meta_value1 = item.get(args.query1, "N/A")
                values.append(meta_value1)
            if args.query2:
                meta_value2 = item.get(args.query2, "N/A")
                values.append(meta_value2)
            output_file.write("\t".join(values) + "\n")

def main():
    parser = argparse.ArgumentParser(description="Extract metadata from SRA Accessions and write to a text file.", 
                                     add_help=False)
    req = parser.add_argument_group('Required')
    req.add_argument("-i", help="List of SRA Accessions to extract metadata info from.", 
                     dest="ids", type=str, required=True)
    req.add_argument('-q1', help="First metadata query of interest.", 
                     dest="query1", type=str, required=True)
    req.add_argument("-o", help="Output text file for SRA metadata of interest.", 
                        dest="output", type=str, required=True)
    opt = parser.add_argument_group('Optional')
    opt.add_argument('-h', '--help', action='help',
                help='show this help message and exit')
    opt.add_argument('-q2', help="Second metadata query of interest.", 
                     dest="query2", type=str)

    
    parser.set_defaults(func=extract_meta)
    args = parser.parse_args()

    if not args.query1 and not args.query2:
        parser.error("You must provide at least one query with either -q1 or -q2.")

    args.func(args)

if __name__ == "__main__":
    main()
