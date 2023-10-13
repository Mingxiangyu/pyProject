# -*- codeing = utf-8 -*-
# @Time :2023/10/11 11:28
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  test.py

import csv

path = r"G:\软件备份\Project\测井\项目所需\Test-1_input&output\Input Package\Test-1_Pipe Inofrmation.csv"
result_dict = {}
with open(path) as f:
    reader = csv.reader(f)
    next(reader)  # 跳过标题行
    next(reader)  # 跳过标题行
    pipe_dicts = []
    for row in reader:
        d = {'od': float(row[2]), 'weight': float(row[3])}
        pipe_dicts.append(d)

    tuple_list = set([(d['od'], d['weight']) for d in pipe_dicts])
    tuple_list = sorted(tuple_list)

    result_dict = [{'od': t[0], 'weight': t[1]} for t in tuple_list]

    # pipe_dicts = list(set(frozenset(d.items()) for d in pipe_dicts))
    # # pipe_dicts = list(set(pipe_dicts))
    # pipe_dicts = sorted(pipe_dicts, key=lambda x: x['od'])
    #
    # result_dict = {d['od']: d['weight'] for d in pipe_dicts}

print(result_dict)