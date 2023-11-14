# genomics_scripts
Python scripts for various manipulation and downloading for genomics.

# extract_sra_metadata.py Script

This python script requires the python package `pysradb` as a depencency.

I suggest creating a conda environment to install `pysradb` with this command:

`conda create -c bioconda -n pysradb PYTHON=3.10 pysradb`
`conda activate pysradb`

Once the conda environment is set up, you should be ready to run the script!  The script pulls from metadata from the [NCBI SRA Database](https://www.ncbi.nlm.nih.gov/sra) from user-given SRA Accessions.

```
usage: extract_sra_metadata.py [-i INPUT_FILE] [-q QUERIES [QUERIES ...]] [-o OUTPUT] [-h] [-s INPUT_STRING [INPUT_STRING ...]] [--display-all-fields]                                                                                                                                                                                                                                                                            Extract metadata from SRA Accessions and write to a text file.                                                                                                                                                                                                                                                                                                                                                                    Required:                                                                                                                                                                                                          -i INPUT_FILE         List of SRA Accessions to extract metadata info from.                                                                                                                                      -q QUERIES [QUERIES ...]                                                                                                                                                                                                               Metadata query or queries of interest. Provide one or two queries.                                                                                                                         -o OUTPUT             Output text file for SRA metadata of interest.                                                                                                                                                                                                                                                                                                                                                            Optional:                                                                                                                                                                                                          -h, --help            show this help message and exit                                                                                                                                                            -s INPUT_STRING [INPUT_STRING ...]                                                                                                                                                                                                     SRA Accessions as a string.                                                                                                                                                                --display-all-fields  Display all fields present in the generated JSON file.  
```

The script will take and either a text file with a list of SRA Accessions `-i` or an SRA Accession or multiple SRA Accessions as a string using `-s`, with a space separating each SRA Accession. 

