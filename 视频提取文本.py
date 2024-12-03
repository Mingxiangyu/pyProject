import requests
from flask import Flask, request, jsonify
import whisper
import ffmpeg
import torch
import os

app = Flask(__name__)


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

@app.route('/transcribe-path', methods=['POST'])
def transcribe_video():
    if request.form.get('url') is None:
        return jsonify({"error": "url参数为空!"}), 400

    url = request.form.get('url')
    file_name = extract_filename_from_url(url)

    video_path = f"./uploaded_videos/{file_name}"

    # 保存上传的视频
    if not os.path.exists('./uploaded_videos'):
        os.makedirs('./uploaded_videos')

    download_image(url, video_path)

    # 提取音频流并保存为 audio.wav
    (
        ffmpeg
        .input(video_path)
        .output("audio.wav", format="wav", acodec="pcm_s16le", ac=1, ar="16k")
        .run()
    )

    # 检查是否有可用的 GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"使用 {'GPU' if device == 'cuda' else 'CPU'} 进行处理")

    # 加载模型
    model = whisper.load_model("base").to(device)

    # 转录音频流，禁用字时间戳以提高速度
    result = model.transcribe("audio.wav", word_timestamps=True)

    # 保存转录文本与每句话的时间节点
    transcript_list = []

    for segment in result['segments']:
        # 创建一个包含时间段和文本的字符串
        transcript_entry={
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text']
        }
        # 将字符串添加到列表中
        transcript_list.append(transcript_entry)

    # # 保存转录文本与每句话的时间节点
    # transcript_path = "./transcript_with_timestamps.txt"
    # with open(transcript_path, "w", encoding='utf-8') as f:
    #     for segment in result['segments']:
    #         # 写入转录文本和时间段
    #         f.write(f"{segment['start']:.2f} --> {segment['end']:.2f}: {segment['text']}\n")

    # 删除生成的音频文件和上传的视频文件
    # 删除临时文件
    if os.path.exists("audio.wav"):
        os.remove("audio.wav")
    if os.path.exists(video_path):
        os.remove(video_path)

    return jsonify({'message': transcript_list})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
