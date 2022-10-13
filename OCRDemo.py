import base64
import json

import cv2
import requests


def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')

# 发送HTTP请求
data = {'images':[cv2_to_base64(cv2.imread(r"C:\Users\DELL\Desktop\20220920105120.jpg"))]}
headers = {"Content-type": "application/json"}
url = "http://localhost:8866/predict/chinese_ocr_db_crnn_server"
r = requests.post(url=url, headers=headers, data=json.dumps(data))

# 打印预测结果
print(r.json()["results"])
