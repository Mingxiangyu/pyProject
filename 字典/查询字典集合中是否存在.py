# -*- codeing = utf-8 -*-
# @Time :2023/6/25 16:51
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  查询字典集合中是否存在.py

def searchDictionary(layerODin, layerWtLbFt, my_set):
    """
    查询字典集合中是否存在 LayerODin 值为 layerODin， LayerWtLbFt 值为 layerWtLbFt 的字典，
    如果存在则返回该字典，否则则返回空字典
    :param layerODin: 查询条件1
    :param layerWtLbFt: 查询条件2
    :param my_set: 字典集合
    :return: 字典
    """
    result = list(filter(lambda x: x.get("LayerODin") == layerODin and x.get("LayerWtLbFt") == layerWtLbFt, my_set))

    if len(result) > 0:
        print(result[0])
        return result[0]
    else:
        print("未找到匹配的字典")
        return {}
