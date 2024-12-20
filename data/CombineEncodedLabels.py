import argparse
import numpy as np
from tqdm import tqdm
# python ../CombineEncodedLabelsHomo.py --y_files y_* --pos_files pos_* --y_outFile y_Luo_Homo.npz --pos_outFile pos_Luo_Homo.npz
parser = argparse.ArgumentParser(description='Combine encoded labels from pos.npz and y.npz files')

# --y_files: 要处理的y文件列表。
# --pos_files: 要处理的pos文件列表。
# --y_outFile: 保存合并后的y文件的输出路径。
# --pos_outFile: 保存合并后的pos文件的输出路径
parser.add_argument('--y_files', nargs="+", type=str,
                    help='y files')
parser.add_argument('--pos_files', nargs="+", type=str,
                    help='pos files')
parser.add_argument('--y_outFile', type=str,
                    help='output file to save encoded labels in.')
parser.add_argument('--pos_outFile', type=str,
                    help='output file to save encoded positions of labels in.')
args = parser.parse_args()

# 打印信息，表示正在读取数据。
# 将输入的y和pos文件名进行排序。
print('Reading data ...')

y_files = sorted(args.y_files)
pos_files = sorted(args.pos_files)
# print("==>> pos_files: ", pos_files)

# 对y_files和pos_files中的每一对文件进行遍历，提取出文件名中的特定部分（如细胞名），确保它们的顺序是一致的。如果不一致，抛出错误。
print('Ordering of cells:')
for a, b in zip(y_files, pos_files):
    a = a.split('/')[-1].split('_')[1].split('.')[0]
    b = b.split('/')[-1].split('_')[1].split('.')[0]
    
    assert a == b, 'Ordering is wrong.'
    print(a, end=',')
print(" \n")
# 使用NumPy的load函数加载所有的y和pos文件数据
ys = [np.load(d) for d in y_files]
poss = [np.load(d) for d in pos_files]

# 初始化两个空字典用于存储合并后的数据。
# 遍历所有染色体，首先合并每个染色体的位置信息（去重），然后初始化一个全为-1的数组用于存储合并后的y数据。
# 对于每个pos数据文件，通过in1d方法找到对应位置的索引，并将相关的y数据填充到合并数组中。
pos_combined = {}
ys_combined = {}

for chrom in tqdm(ys[0].keys()):#["chr4","chr5"]):#
    # print('Combining', chrom, '...')
    # pid=0
    # for p in poss:
    #     print("|", pid)
    #     pchrom=p[chrom]
    #     pid+=1
    pos_combined_chrom = np.unique(np.hstack([p[chrom] for p in poss])) 
    pos_combined[chrom] = pos_combined_chrom

    ys_combined_chrom = np.full((pos_combined_chrom.shape[0], len(ys)), -1, dtype='int8')
    
    for ix, p in enumerate(poss):
        
        indices = np.in1d(pos_combined_chrom, p[chrom])
        ys_combined_chrom[indices, ix] = ys[ix][chrom]
        
    ys_combined[chrom] = ys_combined_chrom

# 打印信息，表示正在写入合并后的文件。
# 使用np.savez_compressed函数将合并后的y和pos数据保存为压缩的.npz文件
print('Writing combined files ...')
np.savez_compressed(args.y_outFile, **ys_combined)
np.savez_compressed(args.pos_outFile, **pos_combined)