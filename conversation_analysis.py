import subprocess
import os

# Assuming you already have a fasta file containing all sequences
input_fasta = "sequences.fasta"

# Perform multiple sequence alignment to find conservative regions among sequences of the same protein family
msa_output = "multiple_alignment.fasta"

# Check if the multiple sequence alignment file already exists and ask the user if they want to overwrite it
if os.path.isfile(msa_output):
    overwrite_prompt = input(f"File '{msa_output}' already exists. Do you want to overwrite it? (yes/no): ")
    if overwrite_prompt.lower() != 'yes':
        exit("User chose not to overwrite the existing file.")

# Print a message indicating that multiple sequence alignment is in progress
print("Performing multiple sequence alignment...")

# Run the Clustalo tool with the --force option to force overwrite
clustalo_cmd = f"clustalo -i {input_fasta} -o {msa_output} --force"
clustalo_result = subprocess.run(clustalo_cmd, shell=True)

# Check if multiple sequence alignment was successful
if clustalo_result.returncode != 0:
    exit(f"Clustalo returned an error: {clustalo_result.stderr}")

# Check if the multiple sequence alignment file exists
if not os.path.isfile(msa_output):
    exit("Multiple sequence alignment file not found.")

# Generate a conservation plot using the Plotcon tool
plotcon_cmd = f"plotcon -sequence {msa_output} -graph svg"
plotcon_result = subprocess.run(plotcon_cmd, shell=True)

# Check if the conservation plot was successfully generated (Plotcon has built-in error checking)
if plotcon_result.returncode != 0:
    exit(f"Plotcon returned an error: {plotcon_result.stderr}")

