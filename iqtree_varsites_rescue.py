#!/usr/bin/env python

import subprocess
import os

def run_iqtree(file_name):
    # The IQTree command
    iqtree_command = ['iqtree', '-s', file_name, '-m', 'GTR+ASC', '-bb', '1000', '-nt', '40']
    
    try:
        # Run the iqtree command
        result = subprocess.run(iqtree_command, capture_output=True, text=True)
        
        # Check if the process was successful
        if result.returncode == 0:
            print("IQTree ran successfully on {}!".format(file_name))
            return True
        else:
            print("IQTree failed with error on {}:".format(file_name))
            print(result.stderr)
            return False

    except Exception as e:
        print("An error occurred while running IQTree on {}: {}".format(file_name, e))
        return False

if __name__ == "__main__":
    # First attempt to run iqtree on SNPs.fa
    success = run_iqtree('SNPs.fa')
    
    if not success:
        # Check if the SNPs.fa.varsites.phy file was generated
        if os.path.exists('SNPs.fa.varsites.phy'):
            print("SNPs.fa.varsites.phy was generated. Attempting to run IQTree on it.")
            # Run iqtree on SNPs.fa.varsites.phy
            run_iqtree('SNPs.fa.varsites.phy')
        else:
            print("SNPs.fa.varsites.phy was not found. No further action will be taken.")


