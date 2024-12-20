import os


def list_subdirectories(directory, output_file):
    try:
        # 获取所有子目录名称
        subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

        # 将子目录名称写入到指定的txt文件
        with open(output_file, 'w') as file:
            for subdir in subdirs:
                file.write(subdir + '\n')

        print(f"子目录名称已写入到 {output_file}")

    except Exception as e:
        print(f"发生错误: {e}")


# 使用示例，替换为你想要列出子目录的路径和输出文件的路径
directory_path = "./folder_copy"
output_file_path = "bismark.txt"
list_subdirectories(directory_path, output_file_path)
