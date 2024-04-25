 #!/bin/env python
import vcf
import sys


def create_snp_fasta_with_reference(vcf_path, output_path):
    # Function to parse VCF records
    def parse_vcf_record(record):
        fields = record.strip().split('\t')
        chrom, pos, id_, ref, alt, qual, filter_, info, format_, *samples = fields
        alts = alt.split(',')
        return ref, alts, samples

    # Initialize a dictionary to hold sequences for each sample
    with open(vcf_path, 'r') as file:
        sequences = {}
        reference_sequence = []
        for line in file:
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    samples = line.strip().split('\t')[9:]
                    sequences = {sample: [] for sample in samples}
            else:
                ref, alts, genotype_data = parse_vcf_record(line)
                reference_sequence.append(ref)  # Add the reference allele to the reference sequence
                for sample, genotype_info in zip(samples, genotype_data):
                    genotype = genotype_info.split(':')[0]  # Get the genotype part only
                    if '.' in genotype:
                        allele = 'N'  # Missing data
                    else:
                        gt_indices = list(map(int, genotype.split('/')))
                        if gt_indices[0] == gt_indices[1]:
                            allele = ref if gt_indices[0] == 0 else alts[gt_indices[0] - 1]
                        else:
                            # Heterozygous, select alternate allele
                            allele = alts[max(gt_indices) - 1]
                    sequences[sample].append(allele)

    # Write to a FASTA file
    with open(output_path, 'w') as fasta_file:
        fasta_file.write(">Reference\n")
        fasta_file.write(''.join(reference_sequence) + "\n")
        for sample, seq in sequences.items():
            fasta_file.write(f">{sample}\n")
            fasta_file.write(''.join(seq) + "\n")

# File paths
vcf_file_path = 'norm_2nd_variant_calls.vcf'
output_fasta_path = 'snp_alignment_with_reference.fasta'

# Call the function
create_snp_fasta_with_reference(vcf_file_path, output_fasta_path)

output_fasta_path
