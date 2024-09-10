# -*- coding: utf-8 -*-
# -------------------------------
# @项目：pyProject
# @文件：qwen官方样例.py
# @时间：2024/9/9 14:40
# @作者：xming
# -------------------------------
import json
import os

from qwen_agent.llm import get_chat_model


#硬编码返回相同天气的示例虚拟函数
#在生产中，这可能是您的后端API或外部API
def get_current_weather(location, unit='fahrenheit'):
    """Get the current weather in a given location"""
    if 'tokyo' in location.lower():
        return json.dumps({
            'location': 'Tokyo',
            'temperature': '10',
            'unit': 'celsius'
        })
    elif 'san francisco' in location.lower():
        return json.dumps({
            'location': 'San Francisco',
            'temperature': '72',
            'unit': 'fahrenheit'
        })
    elif 'paris' in location.lower():
        return json.dumps({
            'location': 'Paris',
            'temperature': '22',
            'unit': 'celsius'
        })
    else:
        return json.dumps({'location': location, 'temperature': 'unknown'})


def test():
    llm = get_chat_model({
        # 使用DashScope提供的模型服务：
        'model': 'qwen-max',
        'model_server': 'dashscope',
        'api_key': os.getenv('DASHSCOPE_API_KEY'),

        # 使用Together提供的模型服务。人工智能：
        # 'model': 'Qwen/Qwen2-7B-Instruct',
        # 'model_server': 'https://api.together.xyz',  # api_base
        # 'api_key': os.getenv('TOGETHER_API_KEY'),

        # Use your own model service compatible with OpenAI API:
        # 'model': 'Qwen/Qwen2-72B-Instruct',
        # 'model_server': 'http://localhost:8000/v1',  # api_base
        # 'api_key': 'EMPTY',
    })

    # Step 1:将对话和可用功能发送给模型
    messages = [{
        'role': 'user',
        'content': "What's the weather like in San Francisco?"
    }]
    functions = [{
        'name': 'get_current_weather',
        'description': 'Get the current weather in a given location',
        'parameters': {
            'type': 'object',
            'properties': {
                'location': {
                    'type': 'string',
                    'description':
                    'The city and state, e.g. San Francisco, CA',
                },
                'unit': {
                    'type': 'string',
                    'enum': ['celsius', 'fahrenheit']
                },
            },
            'required': ['location'],
        },
    }]

    print('# Assistant Response 1:')
    responses = []
    for responses in llm.chat(messages=messages,
                              functions=functions,
                              stream=True):
        print(responses)

    messages.extend(responses)  # 用助理的回复扩展对话

    # Step 2: 检查模型是否要调用函数
    last_response = messages[-1]
    if last_response.get('function_call', None):

        # Step 3:调用函数
        # 注意：JSON响应可能并不总是有效的；一定要处理错误
        available_functions = {
            'get_current_weather': get_current_weather,
        }  # 在这个例子中只有一个函数，但你可以有多个
        function_name = last_response['function_call']['name']
        function_to_call = available_functions[function_name]
        function_args = json.loads(last_response['function_call']['arguments'])
        function_response = function_to_call(
            location=function_args.get('location'),
            unit=function_args.get('unit'),
        )
        print('# Function Response:')
        print(function_response)

        # Step 4: 将每个函数调用和函数响应的信息发送到模型
        messages.append({
            'role': 'function',
            'name': function_name,
            'content': function_response,
        })  # 用功能响应扩展对话

        print('# Assistant Response 2:')
        for responses in llm.chat(
                messages=messages,
                functions=functions,
                stream=True,
        ):  # 从模型中获取新的响应，在那里可以看到函数响应
            print(responses)


if __name__ == '__main__':
    test()