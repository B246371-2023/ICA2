# multiseq_analysis.py

import subprocess
import webbrowser
import os

def run(input_fasta, output_folder):
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    except OSError as e:
        print(f"Error: Could not create output directory {output_folder}. {e}")
        return

    # 输出路径
    msa_output = os.path.join(output_folder, "multiple_alignment.fasta")
    plotcon_output = os.path.join(output_folder, "conservation_graph.svg")

    # 检查是否已存在多序列比对文件
    if os.path.isfile(msa_output):
        overwrite_prompt = input(f"File '{msa_output}' already exists. Do you want to overwrite it? (yes/no): ")
        if overwrite_prompt.lower() != 'yes':
            print("User chose not to overwrite the existing file.")
            return

    # 进行多序列比对
    print("Performing multiple sequence alignment...")
    clustalo_cmd = f"clustalo -i '{input_fasta}' -o '{msa_output}' --force"
    subprocess.run(clustalo_cmd, shell=True, check=True)

    # 绘制保守性图表
    print("Plotting conservation graph...")
    plotcon_cmd = f"plotcon -sequence '{msa_output}' -graph x11 -winsize 10 -goutfile '{plotcon_output}'"
    subprocess.run(plotcon_cmd, shell=True, check=True)

    print("Multiple sequence alignment and conservation graph plotting completed.")

    # 打开生成的 .svg 文件
    try:
        svg_file_path = os.path.abspath(plotcon_output)
        webbrowser.get('firefox').open_new_tab(svg_file_path)
        print(f"Opened {svg_file_path} in Firefox.")
    except Exception as e:
        print(f"Could not open the file in Firefox: {e}")

