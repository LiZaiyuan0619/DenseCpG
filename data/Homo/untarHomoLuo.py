# from tqdm import tqdm
# import os
# import tarfile
#
# output_directory = "./folder"
# # Un-tar
# print("开始解压...")
# for file in tqdm(os.listdir(output_directory)):
#     # print(output_directory+'/'+file)
#     tar_filename = output_directory+'/'+file
#     tar = tarfile.open(tar_filename)
#     tar.extractall(output_directory)
#     tar.close()
#     os.remove(tar_filename)
from tqdm import tqdm
import os
import tarfile

output_directory = "D:/Data4G/Data4G/data/Neuron-Homo/folder_copy"
# Un-tar
print("开始解压...")
for file in tqdm(os.listdir(output_directory)):
    tar_filename = os.path.join(output_directory, file)
    # 检查是否是 tar 文件
    if tar_filename.endswith(".gz"):
        try:
            # 解压文件
            with tarfile.open(tar_filename) as tar:
                tar.extractall(output_directory)
                print(f"解压成功: {tar_filename} ")
            os.remove(tar_filename)
        except Exception as e:
            print(f"解压 {tar_filename} 失败: {e}")
    else:
        print(f"跳过目录: {tar_filename}")