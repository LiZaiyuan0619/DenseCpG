# import os
# from collections import defaultdict
#
#
# def find_duplicates(directory):
#     # 创建一个字典来存储文件和目录名称的计数
#     name_count = defaultdict(int)
#
#     # 遍历指定目录下的所有文件和子目录
#     for root, dirs, files in os.walk(directory):
#         for name in dirs + files:
#             name_count[name] += 1
#
#     # 查找并输出重复的名称
#     duplicates = [name for name, count in name_count.items() if count > 1]
#
#     if duplicates:
#         print("重复的名称:")
#         for name in duplicates:
#             print(name)
#     else:
#         print("没有重复的名称。")
#
#
# # 使用示例，替换为你想要检查的目录路径
# directory_path = "D:/Data4G/Data4G/data/Neuron-Homo/folder"
# find_duplicates(directory_path)

# --------------------------

def find_duplicate_links(file_path):
    with open(file_path, 'r') as file:
        links = file.readlines()

    # 移除换行符并存储链接
    links = [link.strip() for link in links]

    # 创建一个集合来检查重复链接
    seen = set()
    duplicates = set()

    for link in links:
        if link in seen:
            duplicates.add(link)
        else:
            seen.add(link)

    # 输出重复链接
    if duplicates:
        print("重复的链接:")
        for link in duplicates:
            print(link)
    else:
        print("没有重复的链接。")


# 使用示例，替换为你的txt文件路径
file_path = "D:/Data4G/Data4G/data/Neuron-Homo/Downloaded.txt"
find_duplicate_links(file_path)
