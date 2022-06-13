import base64
import json
import pprint

import requests

# get clientKey from 'http://www.yescaptcha.com/dashboard.html'
clientKey = ''

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)

def get_captcha_image_base64(data):
    image_result = []
    for d in data:
        img_base64 = get_as_base64(d['datapoint_uri'])
        img_base64 = img_base64.decode('utf-8')
        image_result.append({
            'url': d['datapoint_uri'],
            'task_key': d['task_key'],
            'base64': img_base64
        })
    return image_result

def create_task(question, queries):
    url = 'https://api.yescaptcha.com/createTask'

    data = {
        "clientKey": clientKey,
        "task": {
            "type": "HCaptchaClassification",
            "question": question,
            "queries": queries,
        }
    }

    r = requests.post(url, json=data, timeout=60)

    return r.json()


if __name__ == '__main__':
    with open('data.json', encoding='utf8') as f:
        data = f.read()
    data = json.loads(data)
    question = data.get('requester_question', {}).get('zh')
    tasklist = data.get('tasklist')
    images = get_captcha_image_base64(tasklist)
    queries = [d['base64'] for d in images]
    result = create_task(question=question, queries=queries)
    pprint.pprint(result)