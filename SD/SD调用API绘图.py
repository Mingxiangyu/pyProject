# -*- codeing = utf-8 -*-
# @Time :2023/5/16 17:15
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://github.com/1803233552/StableDiffusionTelegramBot/blob/main/config.txt
# @File :  SD调用API绘图.py

import base64
import io
import os
import re
import time

import requests
from PIL import Image, PngImagePlugin


# 正常使用,保存信息，自动识别聊天对象发送，可读取自定义参数

def read_config(filename):
    config = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                config[key] = value
    return config


def load_config():
    # 声明全局变量
    global TOKEN
    global CHAT_ID
    global delayTime
    global localurl
    global temp_dir
    global max_filename_length
    global defaultSteps
    global defaultNegative_prompt
    global defaultSeed
    global defaultSampler_index
    global defaultCfg_scale
    global defaultSize
    global defaultEnable_hr
    global defaultHr_scale
    global defaultHr_resize_x
    global defaultHr_resize_y
    global defaultHr_upscaler
    global defaultHr_second_pass_steps
    global defaultDenoising_strength

    # 读取配置文件
    config = read_config('config.txt')

    print(f"读取默认参数")

    # 读取 telegram token
    TOKEN = config.get('TOKEN')
    if len(TOKEN) == 0:
        print(f"TOKEN为空，请检查config.txt文件")
    # print(TOKEN)

    # 读取白名单 id
    CHAT_ID = config.get('CHAT_ID', '').split(',')
    if CHAT_ID == ['']:
        CHAT_ID = []
    print(f"白名单:{CHAT_ID}")

    # 读取刷新消息间隔
    delayTime = int(config.get('delayTime', '5'))
    print(f"刷新消息间隔:{delayTime}s")

    # 读取本地sd地址
    localurl = config.get('localurl', 'http://127.0.0.1:7860')
    print(f"本地sd地址:{localurl}")

    # 读取保存图片位置
    temp_dir = config.get('temp_dir', './image')
    print(f"保存图片位置:{temp_dir}")

    # 读取允许的最大文件名长度
    max_filename_length = int(config.get('max_filename_length', '100'))

    # 读取绘图默认参数
    print(f"绘图默认参数")
    # 步数
    defaultSteps = int(config.get('defaultSteps', '28'))
    print(f"步数:{defaultSteps}")

    # 负面词
    defaultNegative_prompt = config.get('defaultNegative_prompt',
                                        'paintings, sketches, (worst quality:2),(low quality:2), (extra fingers:2), (extra toes:2),bad-picture-chill-75v, badhandv4, easynegative, negative_hand-neg, ng_deepnegative_v1_75t')
    print(f"负面词:{defaultNegative_prompt}")

    # 种子
    defaultSeed = int(config.get('defaultSeed', '-1'))
    print(f"种子:{defaultSeed}")

    # 采样方式
    defaultSampler_index = config.get('defaultSampler_index', 'DPM++ 2M Karras')
    print(f"采样方式:{defaultSampler_index}")

    # 相关性
    defaultCfg_scale = float(config.get('defaultCfg_scale', '7.0'))
    print(f"相关性:{defaultCfg_scale}")

    # 大小
    defaultSize = config.get('defaultSize', '512x768')
    print(f"图片大小:{defaultSize}")

    # 超分辨率开关
    defaultEnable_hr = config.get('defaultEnable_hr', 'False').lower() == 'true'
    print(f"超分辨率状态:{defaultEnable_hr}")

    # 超分辨率倍数
    defaultHr_scale = int(config.get('defaultHr_scale', '2'))
    print(f"超分辨率倍数:{defaultHr_scale}")

    # 超分辨率宽高
    defaultHr_resize_x = int(config.get('defaultHr_resize_x', '1024'))
    defaultHr_resize_y = int(config.get('defaultHr_resize_y', '1536'))
    print(f"超分辨率宽:{defaultHr_resize_x}")
    print(f"超分辨率高:{defaultHr_resize_y}")

    # 放大算法
    defaultHr_upscaler = config.get('defaultHr_upscaler', 'R-ESRGAN 4x+')
    print(f"放大算法:{defaultHr_upscaler}")

    # 放大采样次数
    defaultHr_second_pass_steps = int(config.get('defaultHr_second_pass_steps', '5'))
    print(f"放大采样次数:{defaultHr_second_pass_steps}")

    # 重绘幅度
    defaultDenoising_strength = float(config.get('defaultDenoising_strength', '0.4'))
    print(f"重绘幅度:{defaultDenoising_strength}")


def draw(text_to_print, chat_id):
    # 开始绘图
    star_text = "开始绘图"
    star_res = requests.post(url=f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={star_text}")

    # 检查目标文件夹是否存在，如果不存在则创建
    os.makedirs(temp_dir, exist_ok=True)

    # 去除首尾空格
    text_to_print = text_to_print.strip()

    # 分割成三个部分
    parts = text_to_print.split(",")

    pattern = r"(.*?)(?=Steps:|Sampler:|CFG scale:|Seed:|Size:|ntags:|$)"
    match = re.search(pattern, text_to_print)
    ht_text = match.group(1).strip() if match else text_to_print.strip()

    param_text = ",".join(parts[2:]).strip() if len(parts) > 2 else ""

    # 分割字符串
    segments = text_to_print.split("ntags:")

    # 获取参数值
    steps = defaultSteps
    sampler = defaultSampler_index
    cfg_scale = defaultCfg_scale
    seed = defaultSeed
    size = defaultSize
    enable_hr = bool(defaultEnable_hr)
    hr_resize_x = defaultHr_resize_x
    hr_resize_y = defaultHr_resize_y
    hr_upscaler = defaultHr_upscaler  # 放大算法
    hr_second_pass_steps = defaultHr_second_pass_steps  # 放大采样次数
    denoising_strength = defaultDenoising_strength  # 重绘幅度

    #  解析中间参数
    if param_text:
        param_parts = param_text.split(",")
        for part in param_parts:
            key_value = part.split(":")
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                if key == "Steps":
                    steps = value
                elif key == "Sampler":
                    sampler = value
                elif key == "CFG scale":
                    cfg_scale = value
                elif key == "Seed":
                    seed = value
                elif key == "Size":
                    size = value
                elif key == "Enable_hr":
                    enable_hr = bool(value)
                elif key == "Hr_upscaler":
                    hr_upscaler = value
                elif key == "Hr_second_pass_steps":
                    hr_second_pass_steps = value
                elif key == "Denoising_strength":
                    denoising_strength = value

    # 获取分割后的结果
    ntags = segments[1] if len(segments) > 1 else ""

    if ntags:
        # print("自定义ntags")
        print("")
    else:
        # print("ntags 为空")
        ntags = defaultNegative_prompt

    size = size.split("x")
    width = int(size[0])  # 512
    height = int(size[1])  # 768

    # defaultHr_scale = 2  # 默认超分倍率
    hr_scale = int(defaultHr_scale)
    # print(enable_hr)
    # print(type(enable_hr))
    #
    # print("defaultHr_scale的类型")
    # print(type(defaultHr_scale))

    if enable_hr:
        print("开启超分")
        hr_resize_x = int(width * hr_scale)
        hr_resize_y = int(height * hr_scale)
        # print(type(hr_resize_x))
    # Enable_hr = defaultEnable_hr
    # Hr_scale = defaultHr_scale
    # Hr_resize_x = width * Hr_scale
    # Hr_resize_y = height * Hr_scale

    print("ht_text:", ht_text)
    print("Steps:", steps)
    print("Sampler:", sampler)
    print("CFG scale:", cfg_scale)
    print("Seed:", seed)
    print("Size:", size)
    print("ntags:", ntags)
    print("enable_hr:", enable_hr)
    print("hr_scale:", hr_scale)
    print("hr_resize_x:", hr_resize_x)
    print("hr_resize_y:", hr_resize_y)
    print("hr_second_pass_steps:", hr_second_pass_steps)
    print("denoising_strength:", denoising_strength)

    print("\n")

    payload = {
        "prompt": ht_text,
        "steps": steps,
        "negative_prompt": ntags,
        "seed": seed,
        "sampler_index": sampler,
        "width": width,
        "height": height,
        "cfg_scale": cfg_scale,
        "enable_hr": enable_hr,
        "hr_scale": hr_scale,
        "hr_upscaler": hr_upscaler,
        "hr_second_pass_steps": hr_second_pass_steps,
        "hr_resize_x": hr_resize_x,
        "hr_resize_y": hr_resize_y,
        "denoising_strength": denoising_strength,
    }
    print("正在绘图")
    response = requests.post(url=f'{localurl}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{localurl}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        # 获取已存在文件中的最大编号
        existing_files = os.listdir(temp_dir)
        existing_numbers = [
            int(filename.split("-")[0])
            for filename in existing_files
            if filename.endswith(".png") and "-" in filename
        ]
        max_number = max(existing_numbers) if existing_numbers else -1

        # 生成文件名
        next_number = max_number + 1

        # 裁剪文件名
        shortened_text = ht_text[:max_filename_length - len(f'{next_number:05d}-') - len('.png')]
        # 删除非法字符
        filename = re.sub(r'[<>:"/\\|?*]', '', shortened_text)
        filename = f'{next_number:05d}-{filename}.png'
        print(f"保存图片:{filename}")
        temp_file = os.path.join(temp_dir, filename.replace("\\", "/"))  # 使用正斜杠 / 替换生成的文件路径中的反斜杠 \，以确保路径的正确性
        temp_file = temp_file.replace("\\", "/")
        #print(f"temp_file:{temp_file}")

        # 保存图片
        image.save(temp_file, 'PNG', pnginfo=pnginfo)
        # print(pnginfo)

        # 构建发送图片的 API URL
        url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'


        # 发送图片给聊天 ID
        response1 = requests.post(url, data={'chat_id': chat_id},
                                  files={'photo': open(temp_file, 'rb')})
        print("发送图片完成")
        # print(response1.json())
        print("绘图完成")


def main():
    print("From https://github.com/1803233552/StableDiffusionTelegramBot")
    print("By DW_1803233552")
    # 读取配置
    load_config()
    print("开始监听")

    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    offset = None

    # 获取当前的最新消息的更新 ID
    response = requests.get(url)
    data = response.json()
    if data['ok'] and data['result']:
        offset = data['result'][-1]['update_id'] + 1

    while True:
        try:
            params = {'offset': offset}
            response = requests.get(url, params=params)
            data = response.json()

            if data['ok'] and data['result']:
                for result in data['result']:
                    update_id = result['update_id']
                    message = result.get('message')
                    if message:
                        # print(message)
                        chat_id = str(message['chat']['id'])
                        # print(chat_id)
                        # 判断白名单是否为空，不为空则过滤
                        if CHAT_ID:
                            # 判断群组或个人是否在白名单
                            if chat_id not in CHAT_ID:
                                print("不在白名单")
                                star_text = "没有权限"
                                star_res = requests.post(
                                    url=f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={star_text}")
                                # 更新 offset 为最新的 update_id + 1，以排除已处理的消息
                                offset = update_id + 1
                                continue  # 跳过该消息，继续处理下一条消息

                        text = message.get('text')
                        # 获取消息发送者的信息
                        from_user = message.get('from')
                        if not from_user:
                            continue  # 跳过该消息，继续处理下一条消息
                        is_bot = from_user.get('is_bot')
                        username = from_user.get('username')

                        # 检查消息是否来自机器人本身
                        if is_bot and username == 'YOUR_BOT_USERNAME':
                            continue  # 跳过该消息，继续处理下一条消息

                        if text:
                            # print("最新的消息文本值：", text)

                            if text.startswith('/ht'):
                                text_to_print = text[3:]  # 获取 "/绘图" 后面的文本
                                print("收到绘图指令，文本内容：", text_to_print)

                                # ... 绘图的其他代码 ...
                                draw(text_to_print, chat_id)

                        # 更新 offset 为最新的 update_id + 1，以排除已处理的消息
                        offset = update_id + 1

            # 关闭连接
            response.close()
            # 延迟指定时间后再次发送请求
            time.sleep(delayTime)
            # print("再次发送请求", delayTime)
        except Exception as e:
            print("获取消息时发生错误：", str(e))
            # 处理异常并进行适当的错误处理。


# 程序入口
if __name__ == '__main__':
    main()