#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
import copy


def list_filter(l, filters=None):
    """通过特殊字段过滤原始列表字典
    :param filters: 字典构建的过滤字段
    格式如下
    1.同一字段,匹配多个选项
    {
    "name":[ "m1.large","m1.xlarge","wangjw"]
    }
    2.混合模式多个字段,不同字段有独立的匹配项
    {
    "name":[ "m1.large","m1.xlarge","wangjw"],
    "ram": 4096
    }
    :param l: 目标字典列表
    :return: 过滤后的列表
    """
    rest_l = copy.deepcopy(l)  # 使用copy 是因为字列表字典中 每个元素都是字典, 而字典属于引用性类型, 整个列表也就变成了引用性类型, 当进行remove操作时, 原始的列表也会更改
    if not filters:
        return l

    for i in rest_l:
        for k, v in filters.items():
            if isinstance(v, (list, tuple)) and i.get(k) not in v:
                l.remove(i)
                break
            elif not isinstance(v, (list, tuple)) and i.get(k) != v:
                l.remove(i)
                break
    return l
d = [
        {
            'disk': 1,
            'id': '1',
            'is_disabled': False,
            'is_public': True,
            'name': 'm1.tiny',
            'ram': 512,
            'vcpus': 1
        },
        {
            'disk': 20,
            'id': '2',
            'is_disabled': False,
            'is_public': True,
            'name': 'm1.small',
            'ram': 2048,
            'vcpus': 1
        },
        {
            'disk': 40,
            'id': '3',
            'is_disabled': False,
            'is_public': True,
            'name': 'm1.medium',
            'ram': 4096,
            'vcpus': 2
        },
        {
            'disk': 80,
            'id': '4',
            'is_disabled': False,
            'is_public': True,
            'name': 'm1.large',
            'ram': 8192,
            'vcpus': 4
        },
        {
            'disk': 160,
            'id': '5',
            'is_disabled': False,
            'is_public': True,
            'name': 'm1.xlarge',
            'ram': 16384,
            'vcpus': 8
        },
        {
            'disk': 50,
            'id': 'abb677c9-1bf2-415d-97bd-ef62574690ed',
            'is_disabled': False,
            'is_public': True,
            'name': 'wangjw',
            'ram': 4096,
            'vcpus': 2
        }
    ]

filters = {
    "name": ["m1.large", "m1.xlarge", "wangjw"],
    "ram": 4096
}

filter1 = list_filter(d, filters)
print(filter1)
