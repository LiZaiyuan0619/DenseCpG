import os
import shutil
from tqdm import tqdm

def copy_files(source_dir, target_dir):
    # 检查目标目录是否存在，如果不存在则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 遍历源目录下的所有文件
    for file_name in tqdm(os.listdir(source_dir)):
        source_file = os.path.join(source_dir, file_name)
        target_file = os.path.join(target_dir, file_name)

        # 检查是否是文件，并且在目标目录中不存在该文件
        if os.path.isfile(source_file):
            if not os.path.exists(target_file):
                shutil.copy2(source_file, target_file)
                print(f"复制文件: {file_name}")
            else:
                print(f"文件已存在，跳过: {file_name}")

    print("文件复制完成！")


# 使用示例，将`source_directory`和`target_directory`替换为你的实际路径
source_directory = "G:/Data4G/Neuron-Homo/folder"
target_directory = "G:/Data4G/Neuron-Homo/folder_copy"
copy_files(source_directory, target_directory)
