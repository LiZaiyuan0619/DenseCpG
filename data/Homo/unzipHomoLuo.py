# from tqdm import tqdm
# import os
# import gzip
# import shutil
# # os.getcwdb() 获取当前工作目录的字节字符串形式
# output_directory = "./folder_copy/"
#
# # Un-gzip
# print("un_gzip:")
#
# # os.listdir(output_directory) 列出当前工作目录下的所有文件和子目录，并用tqdm显示处理进度。
# cells_folder_list = []
# for folder in tqdm(os.listdir(output_directory)[:]):
#     # print(folder)
#     # 对每个子目录（folder）进行遍历，生成该目录的完整路径，然后列出该目录中的所有文件
#     folder_path = output_directory+'/'+folder
#     for file in os.listdir(folder_path):
#         file_path = folder_path+'/'+file
#         # 使用gzip.GzipFile以读取模式打开每个.gz文件 (f_in)。
#         # 创建一个新文件，文件名为去掉.gz后缀的原文件名，以写入模式打开 (f_out)。
#         # shutil.copyfileobj(f_in, f_out) 将解压缩的数据从f_in复制到f_out。
#         with gzip.GzipFile(file_path, 'rb') as f_in:
#             with open(file_path.replace(".gz",""), "wb") as f_out:
#                 shutil.copyfileobj(f_in, f_out)
#                 f_in.close()
#                 f_out.close()
#         print("成功处理: ", file_path)
#         # 使用os.remove(file_path) 删除原始的.gz文件。
#         os.remove(file_path)
from tqdm import tqdm
import os
import gzip
import shutil

output_directory = "D:/Data4G/Data4G/data/Neuron-Homo/folder_copy"

# Un-gzip
print("un_gzip:")

for folder in tqdm(os.listdir(output_directory)[:] ):
    folder_path = os.path.join(output_directory, folder)

    if not os.path.isdir(folder_path):
        print("不是目录，跳过: ", folder_path)
        continue  # 跳过非目录

    files = os.listdir(folder_path)
    gz_files = [f for f in files if f.endswith('.gz')]
    non_gz_files = [f for f in files if not f.endswith('.gz')]

    if len(gz_files) == 0 and len(non_gz_files) > 0:
        # 如果没有.gz文件并且有其他文件，跳过该目录
        print(f"已经完全解压，跳过 {folder_path}")
        continue
    elif len(gz_files) == len(files):
        # 如果该目录下所有文件都是.gz，直接解压
        print(f"处理完全未解压目录: {folder_path}")
    else:
        # 只处理.gz文件
        print(f"处理部分未解压目录: {folder_path}")

    for file in gz_files:
        file_path = os.path.join(folder_path, file)

        try:
            with gzip.GzipFile(file_path, 'rb') as f_in:
                with open(file_path[:-3], "wb") as f_out:  # 去掉.gz后缀
                    shutil.copyfileobj(f_in, f_out)
            os.remove(file_path)  # 删除原始的.gz文件
        except Exception as e:
            print(f"处理文件时出错: {file_path}，错误信息: {e}")
    print("成功处理: ", folder_path)
