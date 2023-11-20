#blast.py
import subprocess
import requests
import time
import re
import os
def create_blast_db(fasta_file, db_type, db_name):
    # 构造 makeblastdb 命令
    command = f'makeblastdb -in {fasta_file} -dbtype {db_type} -out {db_name}'

    # 执行命令
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"makeblastdb output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running makeblastdb: {e.stderr}")

# 本地 BLAST 搜索函数
def run_local_blast(query_sequence, db_path, output_file):

    blast_cmd = f"echo '{query_sequence}' | blastp -db {db_path} -out {output_file}"
    subprocess.run(blast_cmd, shell=True)

# 在线 BLAST 搜索函数
def run_online_blast(query_sequence, output_file, api_key, email):
    rid = blast_sequence(query_sequence, api_key, email=email)
    get_blast_results(rid, api_key, output_file)

# 发送序列到 NCBI BLAST 的函数
def blast_sequence(sequence, api_key, db='nr', program='blastp', email='your_email@example.com'):
    params = {
        'CMD': 'Put',
        'DATABASE': db,
        'PROGRAM': program,
        'QUERY': sequence,
        'FORMAT_TYPE': 'Text',
        'EMAIL': email,
        'API_KEY': api_key
    }

    response = requests.post('https://blast.ncbi.nlm.nih.gov/Blast.cgi', data=params)
    if response.status_code != 200:
        raise Exception(f"Error submitting BLAST job: {response.text}")

    # 提取 RID
    rid_search = re.search(r'RID = (.*?)\n', response.text)
    if rid_search:
        rid = rid_search.group(1)
        return rid
    else:
        raise Exception("RID not found in BLAST response.")

# 检索并保存 BLAST 结果的函数
def get_blast_results(rid, api_key, output_file, sleep_time=15, max_attempts=20):
    params = {
        'CMD': 'Get',
        'RID': rid,
        'FORMAT_TYPE': 'Text',
        'API_KEY': api_key
    }

    for attempt in range(max_attempts):
        response = requests.post('https://blast.ncbi.nlm.nih.gov/Blast.cgi', data=params)
        if 'Status=WAITING' in response.text:
            print(f"Attempt {attempt + 1}: Result is not ready, waiting for {sleep_time} seconds.")
            time.sleep(sleep_time)
        elif 'Status=READY' in response.text:
            with open(output_file, 'w') as file:
                file.write(response.text)
            print(f"Results written to {output_file}")
            break
        else:
            raise Exception(f"Error retrieving BLAST results: {response.text}")


# 封装成可供 main.py 调用的 run 函数
def run():
    fasta_file = 'sequences.fasta'  # 输入文件名
    db_type = 'prot'
    db_name = 'my_database'  # 输出数据库名
    local_output_file = "local_blast_results.txt"
    online_output_file = "online_blast_results.txt"
    user_choice = input("Do you want to use local BLAST or online BLAST? (local/online): ")
    my_sequence = input("Please enter the protein sequence you want to blast:")
    api_key = "9570bdf95400b6e4c57a2ef852119f49e008"
    email = "1439151477@qq.com"

    if user_choice.lower() == 'local':
        create_db = input("Do you want to create a local BLAST database? (yes/no): ").strip().lower()
        if create_db in ['yes', 'y']:
            create_blast_db(fasta_file, db_type, db_name)
        else:
            print("BLAST database creation skipped.")
        # 使用当前目录路径构建数据库路径
        current_directory = os.getcwd()
        db_path = os.path.join(current_directory, db_name)
        run_local_blast(my_sequence, db_path, local_output_file)
        print(f"BLAST search completed. Results are in {local_output_file}")
    elif user_choice.lower() == 'online':
        run_online_blast(my_sequence, online_output_file, api_key, email)
        
        print(f"BLAST search completed. Results are in {online_output_file}")
    else:
        print("Invalid choice. Please enter 'local' or 'online'.")


