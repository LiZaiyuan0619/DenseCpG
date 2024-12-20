import os
import subprocess
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm

# # 指定要搜索的路径
# path = 'D:/Data4G/Data4G/data/Neuron-Homo/folder_copy/'  # 替换为你的路径
# output_file = 'bismark.txt'
#
# # 获取以bismark结尾的子目录名称
# bismark_dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d.endswith('bismark')]
#
# # 将结果写入文件
# with open(output_file, 'w') as f:
#     for dir_name in bismark_dirs:
#         f.write(dir_name + '\n')
#
# print(f"已将以bismark结尾的目录名称写入{output_file}")

# 定义主函数
def main(output_directory):

    with open("bismark.txt", "r") as file:
        bismark_dirs = [line.strip() for line in file.readlines()]

    # 查找已存在的最大计数值
    existing_files = [f for f in os.listdir(output_directory) if f.startswith("y_") and f.endswith(".npz")]
    existing_counts = [int(f.split('_')[1].split('.')[0]) for f in existing_files]
    max_count = max(existing_counts) if existing_counts else 0

    # 从 max_count + 1 开始处理
    for count in tqdm(range(max_count + 1, len(bismark_dirs) + 1)):
        cell = bismark_dirs[count - 1]  # 使用 count - 1 来索引正确的 cell
        print(f"正在处理：Index: {count}, Cell: {cell}")
        # 设定工作目录
        path = os.path.join(output_directory, cell)
        os.chdir(path)

        # 调用 EncodeLabelsLuo.py 的逻辑
        encoded_genome_file = "D:/Data4G/Data4G/data/Neuron-Homo/folder_copy/X_Homo.npz"
        # 加载编码基因组数据
        X_encoded = np.load(encoded_genome_file)

        # 设置染色体
        chroms = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "1", "20", "21", "22", "2", "3", "4", "5", "6", "7", "8", "9", "X", "Y"]

        # 初始化存储编码结果的字典
        y_encoded = {}
        pos_encoded = {}

        # 使用 tqdm 显示进度。
        for chrom_short_name in tqdm(chroms):
            chrom_name = "chr" + chrom_short_name
            tsv_path = os.path.join(path, f"allc_{cell[:-7]}{chrom_short_name}.tsv")

            # 读取 TSV 文件
            dat = pd.read_csv(tsv_path, sep='\t', header=0, dtype={0: 'string', 2: 'string', 3: 'string'})
            datsubset = dat[dat["strand"] == "+"]
            datsubset = datsubset[datsubset.mc_class.str.contains(r"CG.")]

            # 提取当前染色体的编码基因组数据
            X_chrom = X_encoded[chrom_name]
            indices = np.where(X_chrom == 2)[0]

            label_chrom = datsubset["methylated"].values.astype('int8')
            subset_ind_C = np.in1d(datsubset.iloc[:, 1] - 1, indices)

            y_encoded[chrom_name] = label_chrom[subset_ind_C].astype('int8')
            pos_encoded[chrom_name] = (datsubset.iloc[:, 1] - 1)[subset_ind_C].astype('int32')

            os.remove(tsv_path)

        y_out_file = os.path.join(output_directory, f"y_{count}.npz")
        pos_out_file = os.path.join(output_directory, f"pos_{count}.npz")

        try:
            np.savez_compressed(y_out_file, **y_encoded)
            np.savez_compressed(pos_out_file, **pos_encoded)
            print(f"成功保存: {y_out_file}\n {pos_out_file}")
        except Exception as e:
            print(f"保存文件时出错: {e}")

        print("处理结束：", cell)

if __name__ == "__main__":
    output_directory = "D:/Data4G/Data4G/data/Neuron-Homo/folder_copy/"
    main(output_directory)