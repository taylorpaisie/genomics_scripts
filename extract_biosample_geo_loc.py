#!/bin/env python

import requests, sys, os
from xml.etree import ElementTree

# Function to retrieve 'geo_loc_name' from a biosample ID using the NCBI API
def get_geo_loc_name(biosample_id, api_key=None):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "biosample",
        "id": biosample_id,
        "api_key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None

    tree = ElementTree.fromstring(response.content)
    for attribute in tree.findall('.//Attribute'):
        if attribute.get('attribute_name') == 'geo_loc_name':
            return attribute.text
    return None


# Replace 'your_ncbi_api_key' with your actual NCBI API key if you have one
api_key = "c213d2297c5c890297e3ae5af5c1b6c2d408"

# Read biosample IDs from the file
file_path = sys.argv[1]
with open(file_path, 'r') as file:
    biosample_ids = file.readlines()

# Output file path
output_file_path = sys.argv[2]

# Processing all biosample IDs from the list
with open(output_file_path, 'w') as output_file:
    for biosample_id in biosample_ids:
        biosample_id = biosample_id.strip()
        geo_loc_name = get_geo_loc_name(biosample_id, api_key=api_key)
        output_file.write(f"{biosample_id}\t{geo_loc_name}\n")
