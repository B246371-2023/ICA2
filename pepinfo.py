import subprocess
import webbrowser
import random
import os

def load_fasta(filename):
    """Read a FASTA file and return a dictionary with sequence headers as keys and sequences as values."""
    sequences = {}
    with open(filename, 'r') as file:
        sequence_id = ''
        sequence = ''
        for line in file:
            if line.startswith('>'):
                if sequence_id:
                    sequences[sequence_id] = sequence
                sequence_id = line.strip()
                sequence = ''
            else:
                sequence += line.strip()
        if sequence_id:
            sequences[sequence_id] = sequence
    return sequences

def random_select(sequences, number):
    """Randomly select a specified number of sequences from a dictionary of sequences."""
    selected_ids = random.sample(list(sequences.keys()), number)
    return {seq_id: sequences[seq_id] for seq_id in selected_ids}

def save_fasta(sequences, filename):
    """Save a dictionary of sequences to a FASTA file."""
    with open(filename, 'w') as file:
        for seq_id, seq in sequences.items():
            file.write(f"{seq_id}\n{seq}\n")

def run_pepinfo(input_fasta, output_folder, graph_type='png'):
    # 确保输出文件夹存在
    output_folder_path = os.path.join(os.getcwd(), output_folder)
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    pepinfo_output = os.path.join(output_folder_path, "pepinfo_output." + graph_type)

    print("Running pepinfo...")
    pepinfo_cmd = f"pepinfo -sequence '{input_fasta}' -graph {graph_type} -outfile '{pepinfo_output}'"
    subprocess.run(pepinfo_cmd, shell=True, check=True)

    print(f"Pepinfo analysis completed. Output saved in {pepinfo_output}")

    try:
        file_path = os.path.abspath(pepinfo_output)
        webbrowser.open(file_path)
        print(f"Opened {file_path} in the default web browser.")
    except Exception as e:
        print(f"Could not open the file: {e}")

def run(input_fasta):
    output_folder = "pepinfo"

    all_sequences = load_fasta(input_fasta)
    total_sequences = len(all_sequences)
    print(f"There are {total_sequences} sequences in the file.")

    process_all = input("Do you want to process all sequences? (yes/no): ").lower()

    if process_all != 'yes':
        number_of_sequences = int(input("Enter the number of sequences you want to select: "))
        selected_sequences = random_select(all_sequences, number_of_sequences)
        selected_fasta = os.path.join(output_folder, "selected_sequences.fasta")
        save_fasta(selected_sequences, selected_fasta)
        input_fasta = selected_fasta

    run_pepinfo(input_fasta, output_folder)

# Example usage
run('sequences.fasta')
