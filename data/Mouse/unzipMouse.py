from tqdm import tqdm
import os
import gzip
import shutil

output_directory = "./folder/"

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