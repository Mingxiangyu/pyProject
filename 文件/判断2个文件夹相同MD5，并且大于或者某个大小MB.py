# -*- codeing = utf-8 -*-
# @Time :2022/11/24 18:43
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://zhuanlan.zhihu.com/p/437121103
# @File :  判断2个文件夹相同MD5，并且大于或者某个大小MB.py

#
# def match(dir1, dir2, size):
#     path_file = {}
#
#     def get(dir_list):
#         for root, dirs, files in os.walk(dir_list):
#             for i in files:
#                 filePath = root + '\\' + i
#                 fsize = os.path.getsize(filePath)
#                 fsize = fsize / float(1024 * 1024)
#                 if round(fsize, 2) >= size:
#                     with open(filePath, "rb") as f:
#                         file_hash = hashlib.md5()
#                         while chunk := f.read(8192):  # py3.8语法
#                             file_hash.update(chunk)
#                             path_file[filePath] = file_hash.hexdigest() + '  size is' + str(round(fsize, 2)) + 'MB'
#
#     get(dir1)
#     get(dir2)
#     new_dict = {}
#     for dict1_key, dict1_vlues in path_file.items():
#         for dict2_key, dict2_vlues in path_file.items():
#             if dict1_vlues == dict2_vlues and dict1_key > dict2_key:
#                 # print(dict1_key,dict1_vlues,'\n',dict2_key,dict2_vlues)
#                 new_dict[dict1_key], new_dict[dict2_key] = dict1_vlues, dict2_vlues
#     return new_dict
#
#
# if __name__ == "__main__":
#     dir1 = "d:\\web2"
#     dir2 = "d:\\迅雷云盘"
#     size = 200  # size单位是MB 查找大于200MB的文件
#     # 如果改为if round(fsize, 2)<=size:则查找小于200MB的文件
#     match(dir1, dir2, size)
