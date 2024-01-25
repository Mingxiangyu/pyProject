# -*- coding: utf-8 -*-
# -------------------------------
# @项目：DetectionDemo
# @文件：testlas.py
# @时间：2024/1/23 14:45
# @作者：xming
# -------------------------------
import lasio

las = lasio.LASFile()


"""
批量生成曲线
"""
#
# las_csv = r"E:\Project\测井\相关\test.csv"
# df = pd.read_csv(las_csv)
# for column in df.columns:
#     las.append_curve(column, df[column].values, unit="m")
#
#  # ['STRT', 'STOP', 'STEP', 'NULL', 'COMP', 'WELL', 'FLD', 'LOC', 'PROV', 'CNTY', 'STAT', 'CTRY', 'SRVC', 'DATE', 'UWI', 'API']"
# las.well["STRT"] = [0]
# las.well["STOP"] = [3.3]
# las.well["WELL"] = "MyWell"
# las.well["FLD"] = "MyField"
#
# las.write("output.las")




"""
生成指定曲线
"""
# depth = [1.1, 2.2, 3.3] # 测量深度
# data = [11, 22, 33] # 曲线数据
#
# las.append_curve("DEPTH", depth, unit="M", descr="Measured Depth")
# las.append_curve("GR", data, unit="API", descr="Gamma Ray")
# las.well["STRT"] = [0]
# las.well["STOP"] = [3.3]
# # las.well["WELL_NAME"] = "MY WELL"
# las.write("my_las_file.las")