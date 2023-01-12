# -*- codeing = utf-8 -*-
# @Time :2022/7/17 18:42
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  test.py
# Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions
import base64
import os

import PySimpleGUI as sg

'''
    将图片转换为base64格式
    先选择存放图片的文件夹
    然后会生成一个outpt.py文件夹。里面存放了转换后的内容。用sublime打开。
    input:  folder with .png .ico .gif 's
    output: output.py file with variables
'''

def main():
    OUTPUT_FILENAME = 'output.py'

    folder = sg.popup_get_folder('Source folder for images\nImages will be encoded and results saved to %s'%OUTPUT_FILENAME,
                               title='Base64 Encoder')

    if not folder:
        sg.popup_cancel('Cancelled - No valid folder entered')
        return
    try:
        namesonly = [f for f in os.listdir(folder) if f.endswith('.png') or f.endswith('.ico') or f.endswith('.gif')]
    except:
        sg.popup_cancel('Cancelled - No valid folder entered')
        return

    outfile = open(os.path.join(folder, OUTPUT_FILENAME), 'w')

    for i, file in enumerate(namesonly):
        contents = open(os.path.join(folder, file), 'rb').read()
        encoded = base64.b64encode(contents)
        outfile.write('\n{} = {}'.format(file[:file.index(".")], encoded))
        sg.OneLineProgressMeter('Base64 Encoding', i+1, len(namesonly), key='-METER-')

    outfile.close()
    sg.popup('Completed!', 'Encoded %s files'%(i+1))

if __name__ == '__main__':
    main()
