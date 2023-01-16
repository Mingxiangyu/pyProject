# -*- codeing = utf-8 -*-
# @Time :2023/1/12 13:31
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  csv文件往MySQL数据库插入数据.py

import csv
import os

cursor = db.cursor()


# 插入数据库函数，传递参数为csv文件路径
def insert_data_from_csv(csv_file):
    f = csv.reader(open(csv_file, 'r'))
    for i in f:
        # csv第一行是字段名，排除掉
        if i[0] == "STATION":
            continue
        sql = 'insert into data values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        # print(i)
        # 插入到数据库
        try:
            cursor.execute(sql, list(i[n] for n in range(28)))
            db.commit()
        except:
            print('插入数据错误')


# 遍历接压缩后的文件夹，获取csv文件，如果符合条件则把文件名作为参数传递给函数insert_data_from_csv插入数据
def insert_data(file_dir):
    # 遍历文件夹
    for tar_gz_dir in os.listdir(file_dir):
        # 如果是文件夹则继续遍历即只遍历下面的文件夹，排除压缩文件
        if os.path.isdir(f'{file_dir}/{tar_gz_dir}'):
            # 排除压缩文件继续遍历文件夹,下面的遍历文件列表为csv文件
            for tar_gz_file in os.listdir(f'{file_dir}/{tar_gz_dir}'):
                # 切割文件，如果csv文件是以5开头则代表是中国的气象站，则调用插入函数插入，否则不处理
                if f'{file_dir}/{tar_gz_dir}/{tar_gz_file}'.split('/')[2][0] == '5':
                    print('是中国的气象站网数据库插入数据%s' % (f'{file_dir}/{tar_gz_dir}/{tar_gz_file}'))
                    insert_data_from_csv(f'{file_dir}/{tar_gz_dir}/{tar_gz_file}')
                else:
                    print('外国气象站数据不处理')


tar_file_dir = r"E:\WorkSpace\pyWorkSpace\pyProject\爬虫\tar_gz"
insert_data(tar_file_dir)
