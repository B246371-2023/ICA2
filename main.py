 # main.py

# 导入其他Python文件作为模块
import download_sequences
import multiseq_analysis
import prosite
#import blast

# 主菜单函数
def main_menu():
    print("欢迎使用生物信息分析系统")
    print("1. 下载目标序列")
    print("2. 多序列比对和保守序列图绘制")
    print("3. Prosite基序搜索")
    print("4. BLAST同源序列搜索")
    print("0. 退出")

# 主程序逻辑
def main():
    while True:
        main_menu()
        choice = input("请选择一个功能：")

        if choice == '1':
            download_sequences.run()  # 假设download_sequences.py中有一个名为run的函数
        elif choice == '2':
                    # 设置输入和输出路径
            input_fasta = "sequences.fasta"
            output_folder = "results_folder"
            multiseq_analysis.run(input_fasta, output_folder)
        elif choice == '3':
                    # 设定输入输出路径
            input_fasta = "sequences.fasta"
            output_folder = "patmatmotifs_results"
            prosite.run(input_fasta, output_folder)
        #elif choice == '4':
           # blast.run()  # 假设blast.py中有一个名为run的函数
        elif choice == '0':
            print("谢谢使用，再见！")
            break
        else:
            print("无效的选择，请重新输入。")

if __name__ == "__main__":
    main()
