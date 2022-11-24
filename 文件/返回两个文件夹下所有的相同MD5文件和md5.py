# -*- codeing = utf-8 -*-
# @Time :2022/11/24 18:45
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  返回两个文件夹下所有的相同MD5文件和md5.py

dir1 = "d:\\web3"
dir2 = "d:\\web"

#
# def file_name(file_dir):
#     path_file = {}
#     for root, dirs, files in os.walk(file_dir):
#         for i in files:
#             with open((root + '\\' + i), "rb") as f:
#                 file_hash = hashlib.md5()
#                 while chunk := f.read(8192):
#                     file_hash.update(chunk)
#                     get_name = root + '\\' + i
#                     path_file[get_name] = file_hash.hexdigest()
#     return (path_file)
#     # print(get_name,file_hash.hexdigest())
#
#
# def match(dict1, dict2):
#     for dict1_key, dict1_vlues in dict1.items():
#         for dict2_key, dict2_vlues in dict2.items():
#             if dict1_vlues == dict2_vlues:
#                 print(dict1_key, dict1_vlues, dict2_key, dict2_vlues)
#
#
# match(file_name(dir1), file_name(dir2))
