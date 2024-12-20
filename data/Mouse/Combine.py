import numpy as np
import os
import glob
from tqdm import tqdm

# 新增导入
import argparse

# 设定目录
folder_path = './folder/'

# 自动获取 y 和 pos 文件
y_files = sorted(glob.glob(os.path.join(folder_path, 'y_*')))
pos_files = sorted(glob.glob(os.path.join(folder_path, 'pos_*')))

# 输出文件名称
y_outFile = os.path.join(folder_path, 'y_Luo_Homo.npz')
pos_outFile = os.path.join(folder_path, 'pos_Luo_Homo.npz')

print("提取细胞名称。。。")
# 对y_files和pos_files中的每一对文件进行遍历，提取出文件名中的特定部分（如细胞名），确保它们的顺序是一致的。如果不一致，抛出错误。
for a, b in zip(y_files, pos_files):
    # a_name = a.split('/')[-1].split('_')[1].split('.')[0]
    # b_name = b.split('/')[-1].split('_')[1].split('.')[0]
    a_name = os.path.basename(a).split('_')[1]  # 提取 y 文件名中 '_' 后的部分
    b_name = os.path.basename(b).split('_')[1]  # 提取 pos 文件名中 '_' 后的部分

    # print("a_name is", a_name)
    # print("b_name is", b_name)
    assert a_name == b_name, 'Ordering is wrong.'
    print(a_name, end=',')

print(" \n")

ys = [np.load(d) for d in y_files]
poss = [np.load(d) for d in pos_files]

pos_combined = {}
ys_combined = {}
print("对每一个染色体处理。。。")
for chrom in tqdm(ys[0].keys()):
    pos_combined_chrom = np.unique(np.hstack([p[chrom] for p in poss]))
    pos_combined[chrom] = pos_combined_chrom

    ys_combined_chrom = np.full((pos_combined_chrom.shape[0], len(ys)), -1, dtype='int8')

    for ix, p in enumerate(poss):
        indices = np.in1d(pos_combined_chrom, p[chrom])
        ys_combined_chrom[indices, ix] = ys[ix][chrom]

    ys_combined[chrom] = ys_combined_chrom

print('保存数据 ...')
np.savez_compressed(y_outFile, **ys_combined)
np.savez_compressed(pos_outFile, **pos_combined)
