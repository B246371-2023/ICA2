import subprocess

def format_species_name(species):
    parts = species.split()
    if len(parts) >= 2:
        formatted_species = parts[0].capitalize() + " " + " ".join(p.lower() for p in parts[1:])
    else:
        formatted_species = species.capitalize()
    return formatted_species

def get_species_from_fasta(fasta_data):
    species_set = set()
    for line in fasta_data.split('\n'):
        if line.startswith('>'):
            parts = line.split('[')
            if len(parts) > 1:
                species = parts[-1].split(']')[0]
                species_set.add(species)
    return species_set

# 用户输入界面
protein_family = input("Enter the protein family name: ")
taxonomic_group = input("Enter the taxonomic group: ")

# 格式化物种名称
formatted_taxonomic_group = format_species_name(taxonomic_group)

# 使用 esearch 搜索 NCBI 数据库
esearch_cmd = f"esearch -db protein -query '{protein_family}[Protein Name] AND {formatted_taxonomic_group}[Organism]' | efetch -format fasta"

# 执行 esearch 命令，并捕获输出
result = subprocess.run(esearch_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 处理错误
if result.returncode != 0:
    print("Error occurred:", result.stderr)
    exit()

# 获取序列数据
sequence_data = result.stdout

# 检查序列数量
sequence_count = sequence_data.count('>')

# 如果序列数量超过1000，警告用户
if sequence_count > 1000:
    print(f"Warning: The number of sequences ({sequence_count}) exceeds 1000.")
    continue_prompt = input("Do you want to continue with all sequences? (yes/no): ")
    if continue_prompt.lower() != 'yes':
        exit()

# 检测多物种
species_set = get_species_from_fasta(sequence_data)
if len(species_set) > 1:
    print("Multiple species detected in the sequences:")
    for species in species_set:
        print(species)
    
    continue_prompt = input("Do you want to continue with all species? (yes/no): ")
    
    if continue_prompt.lower() == 'yes':
        pass  # 如果用户选择继续，则包括所有物种
    else:
        # 用户选择特定物种进行分析
        selected_species_input = input("Enter the species you are interested in (separate by commas if multiple): ")
        selected_species_list = [sp.strip() for sp in selected_species_input.split(',')]
        
        # 只保留用户选择的物种的序列
        sequence_data = '\n'.join(
            sequence for sequence in sequence_data.split('\n\n') if any(species in sequence for species in selected_species_list)
        )
        sequence_count = sequence_data.count('>')

# 保存序列数据到文件
sequences_file = "sequences.fasta"
try:
    with open(sequences_file, "w") as file:
        file.write(sequence_data)
    print("Sequences saved to", sequences_file)
except IOError as e:
    print("An error occurred while writing sequences to file:", e)

# 进行其他分析，如聚类、BLAST、保守性分析等

# ... [这里可以添加进一步的分析代码]

print("Analysis complete.")

