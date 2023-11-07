import subprocess

def format_species_name(species):
    parts = species.split()
    if len(parts) >= 2:
        formatted_species = parts[0].capitalize() + " " + " ".join(p.lower() for p in parts[1:])
    else:
        formatted_species = species.capitalize()
    return formatted_species

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

# 保存序列数据到文件
sequences_file = "sequences.fasta"
with open(sequences_file, "w") as file:
    file.write(sequence_data)

# 进行其他分析，如聚类、BLAST、保守性分析等

print("Analysis complete. Results saved to", sequences_file)

