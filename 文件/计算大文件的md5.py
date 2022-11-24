# -*- codeing = utf-8 -*-
# @Time :2022/11/24 18:34
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://zhuanlan.zhihu.com/p/437121103
# @File :  计算大文件的md5.py

"""
这利用了 MD5 具有 128 字节摘要块（8192 是 128×64）的事实。由于您没有将整个文件读入内存，因此这不会使用超过 8192 字节的内存。
"""
import hashlib

# def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128):
#     """
#     3.8版本
#     :param filename:
#     :param hash_factory:
#     :param chunk_num_blocks:
#     :return:
#     """
#     h = hash_factory()
#     with open(filename, 'rb') as f:
#         while chunk := f.read(chunk_num_blocks * h.block_size):
#             h.update(chunk)
#     return h.digest()

def get_file_md5_top10m(file_name):
    """
    根据前10兆计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_name, 'rb') as fobj:
            data = fobj.read(10240)
            m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象

print(get_file_md5_top10m(r"C:\Users\zhouhuilin\Downloads\gfs.t00z.pgrb2.1p00.f000"))


