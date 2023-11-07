#!/usr/bin/env python
"""This script is to download SRA metadata from a list of SRA Accessions.
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
from pysradb import SRAweb


db = SRAweb()


def sample_ids(args):
    samples = open(args.ids, 'r')
    sra = samples.read()
    sra_list = sra.split('\n')
    print(sra_list)

    for data in sra_list:
        try:
            df = db.sra_metadata(data, detailed=True)
            df.to_csv(data+".tsv", sep="\t", index=False)
        except:
            sys.stderr.write("Error with {}\n".format(data))
            time.sleep(0.5)
        time.sleep(0.5)
    # print(df)

    # combine all the metadata files into one
    # all tsv files must be in the working directory
    tsv_files = glob.glob('*.tsv')
    df_append = pd.DataFrame()
    for file in tsv_files:
         df_temp = pd.read_csv(file, header=0)
         df_append = df_append.append(df_temp, ignore_index=True)
    # print(df_append)
    df_append.to_csv(args.output, sep=',', index=False, header=True)




def main():
	parser=argparse.ArgumentParser(description="Get all the SRA files! Give me a list of SRA accessions, and I shall extract their corresponding metadta.")
	parser.add_argument("-i",help="List of SRA Accessions to extract metadata info from.", dest="ids", type=str, required=True)
	parser.add_argument("-o",help="Output SRA metadta csv file.", dest="output", type=str, required=True)
	parser.set_defaults(func=sample_ids)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
