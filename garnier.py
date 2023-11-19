import subprocess
import os

def run_command(command):
    """运行命令行工具并处理输出"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        exit(1)

# 输入fasta文件路径
input_fasta = "sequences.fasta"

# 二级结构预测输出文件
garnier_output = "sequences.garnier"

# 检查是否需要覆盖现有文件
if os.path.isfile(garnier_output):
    overwrite_prompt = input(f"File '{garnier_output}' already exists. Do you want to overwrite it? (yes/no): ")
    if overwrite_prompt.lower() != 'yes':
        exit("User chose not to overwrite the existing file.")

# 进行蛋白质二级结构预测
print("Performing protein secondary structure prediction using Garnier...")
garnier_cmd = f"garnier -sequence {input_fasta} -outfile {garnier_output}"
run_command(garnier_cmd)

print("Protein secondary structure prediction completed successfully.")

