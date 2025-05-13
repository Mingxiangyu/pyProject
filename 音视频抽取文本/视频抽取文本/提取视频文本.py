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

# 加载较小的模型
model = whisper.load_model("small").to(device)

# 转录音频流，移除 device 参数
result = model.transcribe("audio.wav", word_timestamps=False)

# 保存转录文本
with open("transcript.txt", "w", encoding='utf-8') as f:
    f.write(result["text"])

print("视频转录已完成")
