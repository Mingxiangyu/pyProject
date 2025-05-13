"""
视频转录与时间节点提取

本脚本使用 whisper 模型进行视频转录，并保存转录文本与每句话的时间节点。
"""
import ffmpeg
import torch
import whisper

# 视频文件路径
video_path = "../Video Understanding/data/所以说喝了酒就快乐了吗，熬夜就不空虚了吗，等待她就会回来吗？.mp4"

# 提取音频流并保存为 audio.wav
(
    ffmpeg
    .input(video_path)
    .output("audio.wav", format="wav", acodec="pcm_s16le", ac=1, ar="16k")
    .run()
)

# 检查是否有可用的 GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
if torch.cuda.is_available():
    device = "cuda"
    print("使用 GPU 进行处理")
else:
    device = "cpu"
    print("使用 CPU 进行处理")

# 加载模型
# 注意：如果没有 GPU，请将 device 改为 "cpu"
model = whisper.load_model("base").to(device)    # 加载 whisper 模型

# 转录音频流，禁用字时间戳以提高速度
result = model.transcribe("audio.wav", word_timestamps=True)

# 保存转录文本与每句话的时间节点
with open("../Video Understanding/transcript_with_timestamps.txt", "w", encoding='utf-8') as f:
    for segment in result['segments']:
        # 写入转录文本和时间段
        f.write(f"{segment['start']:.2f} --> {segment['end']:.2f}: {segment['text']}\n")

print("视频转录已完成")

