import hashlib
import json
import time

import requests


def calculate_checksum(app_secret, md5_value, time_stamp):
    content = app_secret + md5_value + str(time_stamp)
    sha1_hash = hashlib.sha1(content.encode('utf-8'))
    return sha1_hash.hexdigest()


# 配置信息
app_key = "57325510c7911d37c4ce0f80ea42b863"
app_secret = "9DB8EAACA93645229CD805DF98BD4A6D"
url = "https://qiyukf.com/openapi/smstask/create"

# 请求数据
request_data = {
	"mobileList":[
		"13601284338"
	],
	"templateId":217130,
	"params":[
		"abc",
		"xyz"
	]
}

# time_stamp = 1733736850
time_stamp = int(time.time())

dumps = json.dumps(request_data)
print(dumps)
md5_value = hashlib.md5(dumps.encode('utf-8')).hexdigest()
# 计算checksum
checksum = calculate_checksum(app_secret, md5_value, time_stamp)

print(md5_value)
print(time_stamp)
print(checksum)


params = {
    "appKey": app_key,
    "time": time_stamp,
    "checksum": checksum
}

headers = {
    "Content-Type": "application/json;charset=utf-8"
}

try:
    response = requests.post(url, params=params, data=dumps, headers=headers)
    response_data = response.json()
    code = response_data.get("code")
    if code == 200:
        print("短信发送任务创建成功，任务id:", response_data.get("message"))
    else:
        print(f"请求失败，错误码: {code}，错误信息: {response_data.get('message')}")
except requests.RequestException as e:
    print(f"请求出现异常: {e}")