import pandas as pd
import numpy as np
import re
import tarfile
import wget
from tqdm import tqdm
import os
import time
import requests


# excel_df = pd.read_excel("Luo_homo_download_titleANDlinks.xlsx", index_col=None, header=None)
# # 正则表达式用于匹配包含“AD008”字符串的标题
# patternRandomPrimerIndex = r"(.*)AD008(.*)"
#
# # link_list是一个空列表，用于存储符合条件的链接。
# # 通过循环遍历Excel的第一行（标题），如果标题匹配正则表达式，就将对应的第二行链接添加到link_list中。
# link_list = []
# for id,title in enumerate(excel_df.iloc[0,:]):
#     if re.match(patternRandomPrimerIndex, title)!=None:
#         link_list.append(excel_df.iloc[1,id])
#
# # 保存链接到link.txt
# with open("link.txt", "w") as file:
#     for link in link_list:
#         file.write(link + "\n")

# 从link.txt中读取链接
with open("link.txt", "r") as file:
    link_list_from_file = [line.strip() for line in file.readlines()]

# 获取当前工作目录，用于存储下载的文件
output_directory = "./folder/"

# 遍历link_list中的每个链接，使用tqdm来显示进度条。
# download_link是构建下载链接的字符串，通过在链接前加上https:来形成完整的URL。
# download_flag用于控制下载的循环，如果下载成功，download_flag将被设为False，否则会在发生异常时输出“Retry...”并等待1秒后重试
# 下载链接
for link in tqdm(link_list_from_file):
    download_link = 'https:' + link[4:]

    # 构建文件名，从下载链接中提取文件名
    filename = os.path.join(output_directory, download_link.split('/')[-1])

    # 检查文件是否已存在
    if os.path.exists(filename):
        print(f"文件已存在，跳过下载: {filename}")
        continue  # 如果文件存在，跳过下载

    download_flag = True
    retry_count = 0  # 初始化重试计数
    max_retries = 5  # 最大重试次数
    success = False  # 用于标记下载是否成功

    while download_flag:
        try:
            filename = wget.download(download_link, out=output_directory)
            print(f"成功下载: {filename}")  # 打印下载成功的文件名
            success = True
            download_flag = False

        except Exception as e:
            print("失败，重试，错误:", e)
            retry_count += 1
            time.sleep(1)

            # 如果重试次数超过最大限制
            if retry_count >= max_retries:
                with open("Failed.txt", "a") as fail_file:
                    fail_file.write(download_link + "\n")  # 保存失败的链接
                print(f"Failed to download: {download_link}")  # 打印失败链接
                download_flag = False  # 结束下载循环

    # 如果下载成功，保存到Downloaded.txt
    if success:
        with open("Downloaded.txt", "a") as success_file:
            success_file.write(filename + "\n")  # 保存成功的文件名

