import subprocess

#格式化用户输入数据
def format_species_name(species):
    parts = species.split()
    if len(parts) >= 2:
        formatted_species = parts[0].capitalize() + " " + " ".join(p.lower() for p in parts[1:])
    else:
        formatted_species = species.capitalize()
    return formatted_species

#
def get_user_input(prompt, type_cast=str, validation=lambda x: True, error_msg="Invalid input"):
    while True:
        user_input = input(prompt)
        if user_input.lower() in ['exit', 'cancel']:
            exit("User exited the input process.")
        try:
            value = type_cast(user_input)
            if validation(value):
                return value
            else:
                print(error_msg)
        except ValueError as e:
            print(f"Error: {e}. {error_msg}")

#函数用于询问用户是否对于搜索结果为0的情况进行重新输入（这里用到课上讲的lambda函数）           
def confirm_input(prompt, data):
    confirm = get_user_input(f"{prompt} Is this correct? (yes/no): ", str.lower, lambda x: x in ['yes', 'no'], "Please type 'yes' or 'no'.")
    return confirm == 'yes'

# 询问用户是否处理序列数量超过1000条如何处理，这个函数接收序列数据和序列计数作为参数，并根据用户的输入决定是继续处理还是退出程序。
# 如果用户选择继续，则函数将返回处理后的序列数据（如果序列数量超过1000，则仅返回前1000个序列）
def handle_large_sequence_count(sequence_data, sequence_count):
    if sequence_count > 1000:
        print(f"Warning: The number of sequences ({sequence_count}) exceeds 1000.")
        continue_prompt = input("Do you want to continue with all sequences? (yes/no)[we recommend no]: ")
        if continue_prompt.lower() != 'yes':
            exit()
        else:
            # 仅保留前1000个序列
            sequences = sequence_data.split('>', 1)[1].split('>')[:1000]
            return '>' + '\n>'.join(sequences)
    return sequence_data


#创建一个字典，实现数据集所包含的不同物种名称及其数量
def get_species_counts_from_fasta(fasta_data):
    species_counts = {}
    for line in fasta_data.split('\n'):
        if line.startswith('>'):
            parts = line.split('[')
            if len(parts) > 1:
                species = parts[-1].split(']')[0]
                species_counts[species] = species_counts.get(species, 0) + 1
    return species_counts

#函数接收原始的序列数据和物种计数字典作为参数。根据用户的输入，
#函数可以决定是继续处理所有物种的序列，还是仅处理用户指定的特定物种的序列。
def handle_multiple_species(sequence_data, species_counts):
    if len(species_counts) > 1:
        print("Multiple species detected in the sequences:")
        #我首先计算了物种名称中最长的长度（max_species_name_length），然后使用 .ljust(max_species_name_length) 方法将每个物种名称扩展或填充到这个最长长度。
        #这样做确保了物种名称在输出中左对齐，然后跟一个制表符和序列数量。这种格式化使得输出更加整洁和易于比较
        max_species_name_length = max(len(species) for species in species_counts)
        for species, count in species_counts.items():
            print(f"{species.ljust(max_species_name_length)}\t {count} sequence(s)")


        print("Number of unique species:", len(species_counts))

        continue_prompt = input("Do you want to continue with all species? (yes/no): ")
        if continue_prompt.lower() == 'yes':
            return sequence_data, None  # 返回原始数据和 None 作为选中的物种列表
        else:
            selected_species_input = input("Enter the species you are interested in (separate by commas if multiple): ")
            selected_species_list = [sp.strip() for sp in selected_species_input.split(',')]

            filtered_sequence_data = '\n'.join(
                sequence for sequence in sequence_data.split('\n\n') if any(f"[{species}]" in sequence for species in selected_species_list)
            )
            return filtered_sequence_data, selected_species_list
    else:
        return sequence_data, None

#检查序列中的N和X的数量
# Function to check sequence quality
def check_sequence_quality(sequence, max_unknowns_percentage=0.1):
    unknowns = sequence.count('N') + sequence.count('X')
    quality_pass = unknowns / len(sequence) <= max_unknowns_percentage
    return quality_pass, unknowns

#检查序列长度
# Function to check sequence length
def check_sequence_length(sequence, min_length=50):
    return len(sequence) >= min_length

#去除重复序列
# Function to remove duplicate sequences
def remove_duplicate_sequences(sequences):
    unique_sequences = {}
    for seq in sequences:
        # Assuming that seq is a tuple (header, sequence)
        if seq[1] not in unique_sequences:
            unique_sequences[seq[1]] = seq[0]
    return [(header, seq) for seq, header in unique_sequences.items()]

#函数可以用于调用前面的质量检查、序列长度和去除重复项的基础功能
def process_sequences(raw_sequence_data):
    quality_check_prompt = input("Do you want to perform quality checks on the sequences? (yes/no): ")
    
    if quality_check_prompt.lower() == 'yes':
        # Initialize counters
        removed_due_to_quality = 0
        removed_due_to_length = 0
        duplicate_sequences_removed = 0
        
        processed_sequences = []
        sequences = raw_sequence_data.split('>')[1:]  # Split the fasta data into sequences

        for sequence in sequences:
            header, seq = sequence.split('\n', 1)
            seq = seq.replace('\n', '')  # Remove newline characters from sequence

            # Check sequence quality
            pass_quality, unknowns = check_sequence_quality(seq)
            if not pass_quality:
                removed_due_to_quality += 1
                continue  # Skip the sequence if it doesn't pass the quality check

            # Check sequence length
            if not check_sequence_length(seq):
                removed_due_to_length += 1
                continue  # Skip the sequence if it doesn't have the minimum length

            processed_sequences.append((header, seq))

        # Remove duplicate sequences
        unique_sequences = remove_duplicate_sequences(processed_sequences)
        duplicate_sequences_removed = len(processed_sequences) - len(unique_sequences)

        # Print analysis summary
        print("Sequence quality analysis completed.")
        print(f"Removed {removed_due_to_quality} sequences due to quality issues.")
        print(f"Removed {removed_due_to_length} sequences due to insufficient length.")
        print(f"Removed {duplicate_sequences_removed} duplicate sequences.")

    else:
        # 用户选择跳过质量检测
        unique_sequences = []
        sequences = raw_sequence_data.split('>')[1:]  # Split the fasta data into sequences
        for sequence in sequences:
            if sequence.strip():  # 确保序列非空
                parts = sequence.split('\n', 1)
                header = parts[0].strip()
                seq = parts[1].replace('\n', '') if len(parts) > 1 else ''
                unique_sequences.append((header, seq))
        print("Quality checks skipped. Proceeding with the original sequences.")

    return unique_sequences

# 主程序循环，直到用户输入自己想要的正确的蛋白质家族名和分类群名
while True:
    # 获取蛋白家族名
    protein_family = get_user_input("Enter the protein family name(e.g. glucose-6-phosphatase): ")
    # 获取分类群名
    taxonomic_group = get_user_input("Enter the taxonomic group(e.g. Aves/birds): ")
    # 格式化物种名称，防止用户输出错误
    formatted_taxonomic_group = format_species_name(taxonomic_group)
    
    # 展示输入的信息供用户确认，这一步是为了让用户可以仔细检查自己的物种名称以防得不到正确的结果
    print(f"You have entered Protein Family: '{protein_family}' and Taxonomic Group: '{formatted_taxonomic_group}'.")
    if confirm_input("Confirm", [protein_family, formatted_taxonomic_group]):
        # 使用 esearch 搜索 NCBI 数据库
        esearch_cmd = f"esearch -db protein -query '{protein_family}[Protein Name] AND {formatted_taxonomic_group}[Organism]' | efetch -format fasta"
        print("Downloading target sequence...")
        # 执行 esearch 命令，并捕获输出
        result = subprocess.run(esearch_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 处理错误，如果用户没有得到任何序列，可以返回输入界面让用户重新输入想要的序列名
        
        # 检查是否有错误或无结果
        if result.returncode != 0 or not result.stdout.strip():
            if result.returncode != 0:
                print("Error occurred:", result.stderr)
            else:
                print("No sequences were found for the given input.")
            
            if get_user_input("Do you want to enter a different protein family and taxonomic group? (Y/N): ").lower() != 'y':
                break  # 用户不希望重新输入，退出程序
        else:
            # 输出结果并退出循环
            #print(result.stdout)
            print("Sequence download completed")
            break

# 获取序列数据
sequence_data = result.stdout

# 检查序列数量
sequence_count = sequence_data.count('>')

# 如果序列存在1000条以上的数据，询问是否继续处理，并告知会只处理前1000条序列
sequence_data = handle_large_sequence_count(sequence_data, sequence_count)

# 在处理大量序列之后，分析不同物种名称和其计数
species_counts = get_species_counts_from_fasta(sequence_data)

# 处理多物种
selected_sequence_data, selected_species_list = handle_multiple_species(sequence_data, species_counts)


# 进行序列质量清洗
unique_sequences = process_sequences(sequence_data)

# Convert the unique sequences back to fasta format
formatted_sequence_data = '\n'.join([f'>{header}\n{seq}' for header, seq in unique_sequences])


# 保存序列数据到文件
sequences_file = "sequences.fasta"
try:
    with open(sequences_file, "w") as file:
        file.write(sequence_data)
    print("Sequences saved to", sequences_file)
except IOError as e:
    print("An error occurred while writing sequences to file:", e)

# 保存序列数据到文件
selected_sequences_file = "selected_sequences.fasta"
try:
    with open(selected_sequences_file, "w") as file:
        file.write(selected_sequence_data)
    print("Sequences saved to", selected_sequences_file)
except IOError as e:
    print("An error occurred while writing sequences to file:", e)

# 保存序列数据到文件
formatted_sequences_file = "formatted_sequences.fasta"
try:
    with open(formatted_sequences_file, "w") as file:
        file.write(formatted_sequence_data)
    print("Sequences saved to", formatted_sequences_file)
except IOError as e:
    print("An error occurred while writing sequences to file:", e)


