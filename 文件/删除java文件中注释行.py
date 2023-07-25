# -*- codeing = utf-8 -*-
# @Time :2023/7/25 9:32
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  删除java文件中注释行.py
import os
import re

# 改这个目录！！！
top_dir = "E:\\java_comments_trim\\"
# 状态
S_INIT = 0
S_SLASH = 1 # 斜杠
S_BLOCK_COMMENT = 2
S_BLOCK_COMMENT_DOT = 3
S_LINE_COMMENT = 4
S_STR = 5
S_STR_ESCAPE = 6


def trim_dir(path):
    print("目录：" + path)
    for root, dirs, files in os.walk(path):
        for name in files:
            trim_file(os.path.join(root, name))
        for name in dirs:
            trim_dir(os.path.join(root, name))


def trim_file(path):
    print("文件：" + path)
    # 使用 re.match() 函数检查路径是否匹配正则表达式模式
    if re.match(r".*java", path):
        print(" 处理")
    else:
        print(" 忽略")
        return
    bak_file = path + ".bak"
    os.rename(path, bak_file)
    fp_src = open(bak_file)
    fp_dst = open(path, 'w')
    # 初始状态定义为代码
    state = S_INIT
    for line in fp_src.readlines():
        for c in line:
            if state == S_INIT:
                if c == '/':
                    state = S_SLASH
                elif c == '"''"':
                    state = S_STR
                    fp_dst.write(c)
                else:
                    fp_dst.write(c)
            elif state == S_SLASH:
                if c == '*':
                    state = S_BLOCK_COMMENT
                elif c == '/':
                    state = S_LINE_COMMENT
                else:
                    fp_dst.write('/')
                    fp_dst.write(c)
            elif state == S_BLOCK_COMMENT:
                if c == '*':
                    state = S_BLOCK_COMMENT_DOT
            elif state == S_BLOCK_COMMENT_DOT:
                if c == '/':
                    state = S_INIT
                else:
                    state = S_BLOCK_COMMENT
            elif state == S_LINE_COMMENT:
                if c == '\n':
                    state = S_INIT
            elif state == S_STR:
                if c == '\\':
                    state = S_STR_ESCAPE
                elif c == '"':
                    state = S_INIT
                fp_dst.write(c)
            elif state == S_STR_ESCAPE:
                # 这里未完全实现全部序列，如\oNNN \xHH \u1234 \U12345678，但没影响
                state = S_STR
                fp_dst.write(c)
    fp_src.close()
    fp_dst.close()


trim_dir(top_dir)
