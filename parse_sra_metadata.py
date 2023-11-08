#!/usr/bin/env python
"""This script is to parse SRA metadata output in a text file.
Author: Taylor K. Paisie <ltj8@cdc.gov>
Version: 0.1.0
Date: 2023-11-07
"""

__version="0.1.0"

args = ''
import os, sys, operator, logging, argparse
import numpy, urllib, time
import time, json, csv
import pandas as pd


def parse_meta(args):
    df = pd.read_csv(args.input, sep='\t', header=0)
    # print(df)
    feat = df[["run_accession", args.query]]
    print(feat)
	
    feat.to_csv(args.output, sep='\t', index=False, header=True)
	

def main():
	parser=argparse.ArgumentParser(description="Parse a text file with SRA metadata.")
	parser.add_argument("-i",help="Text file with SRA metadata", dest="input", type=str, required=True)
	parser.add_argument('-q', help="SRA metadata query of interest.", dest="query", type=str, required=True)
	parser.add_argument("-o",help="Output desired SRA metadata columns", dest="output", type=str, required=True)
	parser.set_defaults(func=parse_meta)
	args=parser.parse_args()
	args.func(args)

if __name__=="__main__":
	main()
