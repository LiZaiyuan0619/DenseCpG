import argparse
import pandas as pd
import numpy as np
import re
import os
from tqdm import tqdm
#
parser = argparse.ArgumentParser(description='Encode CpG labels from tsv file into compact format')


# dataFile：输入数据文件夹的名称。
# EncodedGenome：从另一个脚本生成的编码基因组的文件。
# y_outFile：输出文件，用于保存编码标签。
# pos_outFile：输出文件，用于保存标签的位置。
# chroms：染色体的顺序，作为可选参数。
# prepend_chr：可选参数，指示是否在染色体名称前加上“chr”。
parser.add_argument('dataFile', type=str, metavar='<folder name>',
                    help='data file')
parser.add_argument('EncodedGenome', type=str, metavar='<.npz file>',
                    help='Encoded genome from EncodeGenome.py.')
parser.add_argument('y_outFile', type=str, metavar='<.npz file>',
                    help='output file to save encoded labels in.')
parser.add_argument('pos_outFile', type=str, metavar='<.npz file>',
                    help='output file to save encoded positions of labels in.')
parser.add_argument('--chroms', nargs="+", type=str, required=True,
                    help='ordering of chromosomes in the fasta file')
parser.add_argument('--prepend_chr', action='store_true',
                    help='whether to prepend the str "chr" to the names of chromosomes given in --chroms.')

args = parser.parse_args()

chroms = args.chroms
if args.prepend_chr:
    # chroms = ["chr" + c for c in chroms]
    chroms = [c for c in chroms]

# path = "/home/dyz/repo/cpg-transformer-main/data/HCC"
# path = 'E:/Homo'
# 获取当前工作目录
path = "D:/Data4G/Data4G/data/Neuron-Homo/folder_copy/"
os.chdir(path)
# print(os.getcwd())

# print('Reading data ...')
#
# 读取数据：
cell_data_folder_name = args.dataFile

X_encoded = np.load(args.EncodedGenome)

# 初始化存储编码结果的字典
y_encoded = {}
pos_encoded = {}

# 使用 tqdm 显示进度。
for chrom_short_name in tqdm(chroms):
    # 为每个染色体构建完整的名称，并构建TSV文件的路径。
    chrom_name = "chr" + chrom_short_name
    # print('Encoding',chrom_name,'...')
    tsv_path = path+'/'+args.dataFile+'/'+"allc_"+args.dataFile[:-7]+chrom_short_name+".tsv"
    dat = pd.read_csv(tsv_path, sep='\t', header=0, dtype={0:'string', 2:'string',3:'string'})
    # # 使用 pandas 读取TSV文件，过滤数据集，选择正链（strand 为 "+"）的行，并只选择含有“CG”的行。
    datsubset = dat[dat["strand"]=="+"]
    # dat = dat[dat["mc_class"]=="CGG"]
    datsubset = datsubset[datsubset.mc_class.str.contains(r"CG.")]

    # 提取当前染色体的编码基因组数据。
    # 找到序列中C位置的索引。
    # 从过滤后的数据集中提取甲基化信息，并编码为 int8 格式。
    # 使用 np.in1d 选择与C位置匹配的标签，并分别存储编码标签和位置。
    X_chrom = X_encoded[chrom_name]
    indices = np.where(X_chrom==2)[0]#seq上C开头的位置
    
    label_chrom = datsubset["methylated"].values.astype('int8')
    
    subset_ind_C = np.in1d(datsubset.iloc[:,1]-1, indices)
    
    y_encoded[chrom_name] = label_chrom[subset_ind_C].astype('int8')
    pos_encoded[chrom_name] = (datsubset.iloc[:,1]-1)[subset_ind_C].astype('int32')

# 将编码标签和位置分别保存为压缩的.npz文件
np.savez_compressed(args.y_outFile, **y_encoded)
np.savez_compressed(args.pos_outFile, **pos_encoded)
print("处理结束：", args.dataFile)