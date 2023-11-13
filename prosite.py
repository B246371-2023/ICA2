import subprocess
import os

def extract_sequences(fasta_file):
    """
    Extracts individual sequences from a fasta file.
    Returns a list of tuples: [(header, sequence), ...]
    """
    sequences = []
    with open(fasta_file, 'r') as file:
        sequence_data = file.read().split('>')[1:]
        for seq in sequence_data:
            parts = seq.split('\n', 1)
            header = parts[0].strip()
            sequence = parts[1].replace('\n', '').strip()
            sequences.append((header, sequence))
    return sequences

def run_patmatmotifs(sequence, header, output_folder):
    """
    Runs patmatmotifs for a given sequence.
    """
    # Create a temporary fasta file
    temp_fasta = f"{output_folder}/temp.fasta"
    with open(temp_fasta, 'w') as file:
        file.write(f">{header}\n{sequence}")

    # Generate a safe output file name by replacing spaces with underscores
    safe_header = header.replace(' ', '_').replace(',', '').replace('[', '').replace(']', '')
    output_file = f"{output_folder}/{safe_header}.patmatmotifs"

    # Run patmatmotifs
    cmd = f"patmatmotifs -sequence '{temp_fasta}' -outfile '{output_file}' -full -auto"
    subprocess.run(cmd, shell=True)

    # Remove temporary fasta file
    os.remove(temp_fasta)

# Main script
input_fasta = "sequences.fasta"
output_folder = "patmatmotifs_results"

# Create output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Extract sequences from fasta file
sequences = extract_sequences(input_fasta)

# Run patmatmotifs for each sequence
for header, sequence in sequences:
    print(f"Running patmatmotifs for {header}...")
    run_patmatmotifs(sequence, header, output_folder)

print("All patmatmotifs analyses are completed.")

