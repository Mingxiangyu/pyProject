# -*- codeing = utf-8 -*-
# @Time :2023/3/6 18:08
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :https://mp.weixin.qq.com/s/wa0sdimbB5QEZKquDQsotw
# @File :  突破CloudFlare五秒盾付费版.py

import json

import requests

"""
提前部署docker
docker run -d \
  --name=flaresolverr \
  -p 8191:8191 \
  -e LOG_LEVEL=info \
  --restart unless-stopped \
  ghcr.io/flaresolverr/flaresolverr:latest
"""

url = "http://localhost:8191/v1"

payload = json.dumps({
  "cmd": "request.get",
  "url": "https://www.coinbase.com/ventures/content",
  "maxTimeout": 60000
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)

# 这个Docker镜像启动的接口，返回的数据是JOSN，网页源代码在其中的.solution.response中
print(response.json()['solution']['response'])