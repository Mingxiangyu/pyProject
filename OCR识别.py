import os

import numpy as np
import requests
from flask import Flask, request, jsonify
from rapidocr_onnxruntime import RapidOCR

app = Flask(__name__)
engine = RapidOCR()


def extract_filename_from_url(url):
    # 使用split方法以'/'为分隔符分割URL
    parts = url.split('/')
    # 文件名是列表中的最后一个元素
    filename = parts[-1]
    return filename


def download_image(url, file_path):
    # 发送HTTP GET请求，并设置stream=True
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        # 以二进制写入模式打开文件
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                # 如果有数据则写入文件
                file.write(chunk)


@app.route('/ocr-file', methods=['POST'])
def ocr_file():
    if 'file' not in request.files and not request.form.get("file"):
        return jsonify({"error": "没有文件被上传!"}), 400

    file = request.files.get("file") or request.form.get("file")
    if file.filename == '':
        return jsonify({"error": "文件名为空!"}), 400

    # 保存上传的文件
    img_path = os.path.join('./picture', file.filename)
    file.save(img_path)

    # 处理图片并获取结果
    result, elapse = engine(img_path)
    # 检查并替换第三个元素的类型
    for inner_array in result:
        if isinstance(inner_array[2], np.float32):
            inner_array[2] = float(inner_array[2])  # 转换为原生 float
    # 删除临时文件
    if os.path.exists(img_path):
        os.remove(img_path)

    return jsonify({"message": result})


@app.route('/ocr-path', methods=['POST'])
def ocr_path():
    if request.form.get('url') is None:
        return jsonify({"error": "url参数为空!"}), 400

    url = request.form.get('url')
    file_name = extract_filename_from_url(url)

    file_path = os.path.join('./picture', file_name)
    download_image(url, file_path)

    # 处理图片并获取结果
    result, elapse = engine(file_path)
    # 检查并替换第三个元素的类型
    for inner_array in result:
        if isinstance(inner_array[2], np.float32):
            inner_array[2] = float(inner_array[2])  # 转换为原生 float
    # 删除临时文件
    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify({"message": result})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
