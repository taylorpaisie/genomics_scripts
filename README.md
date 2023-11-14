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

Here is an example of running the `extract_sra_metadata.py` script with a list of SRA Accessions as a text file and wanting the instrument and library layout (ex., PAIRED or SINGLE) metadata from the SRA Accessions listed in the text file and outputed in a text file with the name of your choosing:  

`python extract_sra_metadata.py -i sra_ids.txt -q instrument library_layout -o sra_meta.txt`

It will then proceed to print out the information as well as save it to a tab-deliminted text file, such as this:

```
SRR Accession   instrument      library_layout
SRR11097771     NextSeq 500     PAIRED
SRR11097772     NextSeq 500     PAIRED
SRR11097773     NextSeq 500     PAIRED
SRR11097774     NextSeq 500     PAIRED
```

If you are only interested in extracting metadata from one sample, you can use the `-s` option to only specificy that SRA Accession, as follows:  

`python extract_sra_metadata.py -s SRR11097771 -q instrument library_layout -o sra_meta.txt`

The `-s` option will also accept more than one SRA Accession, with a space between each one, such as:  

`python extract_sra_metadata.py -s SRR11097771 SRR11097772 -q instrument library_layout -o sra_meta.txt`

Any questions feel free to contact me!
