# -*- codeing = utf-8 -*-
# @Time :2023/7/5 16:27
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  删除文件内容.py
def remove_lines_with_stop_char(file_path, stop_char):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    output_lines = []
    for line in lines:
        if stop_char in line:
            break
        output_lines.append(line)

    # 使用列表推导式过滤掉要移除的元素
    result = [x for x in lines if x not in output_lines]
    result[0] = result[0].replace("~A ", "")
    print(result)

    result = ''.join(result)

    with open(file_path, 'w') as file:
        file.write(result)


# 使用示例
file_path = r"C:\Users\12074\Desktop\Case-11_Raw_Data.las"
stop_char = '~A Depth'

remove_lines_with_stop_char(file_path, stop_char)
