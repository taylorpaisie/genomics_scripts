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
# from pysradb import SRAweb


db = pysradb.SRAweb()


def sample_ids(args):
    samples = open(args.ids, 'r')
    sra = samples.read()
    sra_list = sra.split('\n')
    print(sra_list)

    sras = []

    for meta in sra_list:
          metadata = db.sra_metadata(meta)
          sras.append(metadata)
    print(sras)

    meta_json = json.dumps([m.to_dict(orient="records")[0] for m in sras], indent=2)
    print(meta_json)

    with open(args.output, "w") as outfile:
        outfile.write(meta_json)





def main():
	parser=argparse.ArgumentParser(description="Get all the SRA files! Give me a list of SRA accessions, and I shall extract their corresponding metadta.")
	parser.add_argument("-i",help="List of SRA Accessions to extract metadata info from.", dest="ids", type=str, required=True)
	parser.add_argument("-o",help="Output SRA metadata json file.", dest="output", type=str, required=True)
	parser.set_defaults(func=sample_ids)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
