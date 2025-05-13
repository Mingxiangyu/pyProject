import logging
import mimetypes
import os
import warnings
from logging.handlers import RotatingFileHandler

import ffmpeg
import requests
import torch
import whisper
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage

# os.environ['CUDA_VISIBLE_DEVICES'] = '1'

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Configure file logging
ROOT_DIR = os.getcwd()
file_handler = RotatingFileHandler(
    os.path.join(ROOT_DIR, 'whisper_transcription.log'),
    maxBytes=1024 * 1024,
    backupCount=5
)
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create upload directory
UPLOAD_DIR = os.path.join(ROOT_DIR, 'uploaded_videos')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的MIME类型
ALLOWED_MIME_TYPES = [
  'video/mp4', 'video/x-msvideo', 'video/quicktime', 'video/x-matroska',
  'video/x-flv', 'video/webm', 'audio/wav', 'audio/mpeg', 'audio/ogg'
]

# Initialize Flask and Flask-RESTx
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 10 * 10  # 1600 MB
CORS(app)

# Create API with Swagger documentation
api = Api(app,
          version='1.0',
          title='Whisper 音频转录API',
          description='Whisper 支持音频和视频文件转录的API服务',
          doc='/swagger'
          )

# Audio namespace
audio_ns = api.namespace('audio', description='音频转录操作')

# URL转录的解析器
url_parser = api.parser()
url_parser.add_argument('url',
                        location='form',
                        required=True,
                        help='音频或视频文件的URL')
url_parser.add_argument('model',
                        location='form',
                        default='base',
                        help='Whisper模型大小 (tiny/base/small/medium/large)')

# 文件上传的解析器
upload_parser = api.parser()
upload_parser.add_argument('file',
                           location='files',
                           type=FileStorage,
                           required=True,
                           help='要转录的音频或视频文件')
upload_parser.add_argument('model',
                           location='form',
                           default='base',
                           help='Whisper模型大小 (tiny/base/small/medium/large)')

# 响应模型
transcription_model = api.model('Transcription', {
  'code': fields.Integer(description='状态码', required=True),
  'msg': fields.String(description='状态消息', required=True),
  'data': fields.List(fields.Raw, description='转录结果', required=True),
  'filename': fields.String(description='原始文件名', required=True)
})


def extract_filename_from_url(url):
  """从URL提取文件名"""
  return url.split('/')[-1]


def is_allowed_mime_type(mime_type):
  return mime_type in ALLOWED_MIME_TYPES


def download_file(url, file_path):
  """从URL下载文件"""
  with requests.get(url, stream=True) as response:
    response.raise_for_status()
    with open(file_path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)


def extract_audio(input_file):
  """从输入文件提取音频"""
  audio_path = os.path.join(UPLOAD_DIR, 'audio.wav')

  try:
    (
      ffmpeg
      .input(input_file)
      .output(audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16k")
      .run(overwrite_output=True)
    )
  except ffmpeg.Error as e:
    logger.error(f"FFmpeg error: {e.stderr.decode()}")
    raise ValueError(f"音频提取失败: {str(e)}")

  return audio_path


def transcribe_audio(audio_path, model_size='base'):
  """转录音频"""
  print(f"CUDA available: {torch.cuda.is_available()}")
  print(f"CUDA version: {torch.version.cuda}")
  print(f"cuDNN version: {torch.backends.cudnn.version()}")

  # 获取并打印可用的GPU数量
  num_gpus = torch.cuda.device_count()
  print(f"可用的显卡数量: {num_gpus}")

  # 打印每个GPU的信息
  for i in range(num_gpus):
    print(f"显卡 {i}: {torch.cuda.get_device_name(i)}")

  # 检查是否有至少两张 GPU 卡可用
  if num_gpus >= 2:
    device = "cuda"
  else:
    device = "cpu"

  # 检查是否有可用的 GPU
  # 直接指定设备为 cuda:1 表示使用第二张卡
  # device = "cuda:1" if torch.cuda.is_available() else "cpu"
  logger.info(f"使用 {'GPU' if 'cuda' in device else 'CPU'} 进行处理")
  print(f"使用 {'GPU' if 'cuda' in device else 'CPU'} 进行处理")
  logger.info(f"设备: {device}")
  print(f"设备: {device}")

  try:
    # 加载模型
    model = whisper.load_model(model_size).to(device)

    # 转录音频流
    result = model.transcribe(audio_path, word_timestamps=True)

    # 处理转录结果
    transcript_list = []
    for segment in result.get('segments', []):
      transcript_entry = {
        "start": segment['start'],
        "end": segment['end'],
        "text": segment['text'].strip()
      }
      transcript_list.append(transcript_entry)

    return transcript_list
  except Exception as e:
    logger.error(f"转录失败:", exc_info=True)  # 记录详细堆栈信息
    raise


def cleanup_files(*files):
  """清理临时文件"""
  for file in files:
    try:
      if file and os.path.exists(file):
        os.remove(file)
    except Exception as e:
      logger.warning(f"文件删除失败: {file}, 错误: {str(e)}")


@audio_ns.route('/transcribe-url')
class AudioTranscriptionFromURL(Resource):
  @api.expect(url_parser)
  @api.marshal_with(transcription_model)
  def post(self):
    """
        从URL转录音频/视频文件
        提供音频或视频文件的URL并获取其转录文本
        """
    try:
      # 解析参数
      args = url_parser.parse_args()
      url = args['url']
      model_size = args.get('model', 'base')

      # 提取文件名并下载
      file_name = extract_filename_from_url(url)

      # 猜测MIME类型
      guessed_mime, _ = mimetypes.guess_type(file_name)
      if not guessed_mime or not is_allowed_mime_type(guessed_mime):
        return {'code': 1, 'msg': f'不支持的文件类型: {guessed_mime}',
                "data": []}, 400

      file_path = os.path.join(UPLOAD_DIR, file_name)
      if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
      download_file(url, file_path)

      try:
        # 提取音频并转录
        audio_path = extract_audio(file_path)
        transcript_list = transcribe_audio(audio_path, model_size)

        return {
          "code": 0,
          "msg": '成功',
          "data": transcript_list,
          'filename': file_name
        }, 200
      finally:
        # 清理临时文件
        cleanup_files(file_path,
                      audio_path if 'audio_path' in locals() else None)

    except Exception as e:
      logger.error(f'[URL转录]错误: {e}')
      return {'code': 2, 'msg': str(e), "data": []}, 500


@audio_ns.route('/transcribe-file')
class AudioTranscriptionFromFile(Resource):
  @api.expect(upload_parser)
  @api.marshal_with(transcription_model)
  def post(self):
    """
        上传音频/视频文件并转录
        """
    try:
      # 解析参数
      args = upload_parser.parse_args()
      audio_file = args['file']
      model_size = args.get('model', 'base')

      # 保存上传的文件
      noextname, ext = os.path.splitext(audio_file.filename)
      file_path = os.path.join(UPLOAD_DIR, f'{noextname}{ext}')
      audio_file.save(file_path)

      try:
        # 提取音频并转录
        audio_path = extract_audio(file_path)
        transcript_list = transcribe_audio(audio_path, model_size)

        return {
          "code": 0,
          "msg": '成功',
          "data": transcript_list,
          'filename': audio_file.filename
        }, 200
      finally:
        # 清理临时文件
        cleanup_files(file_path,
                      audio_path if 'audio_path' in locals() else None)

    except Exception as e:
      logger.error(f'[文件转录]错误: {e}')
      return {'code': 2, 'msg': str(e)}, 500


if __name__ == '__main__':
  try:
    # 启动服务器
    web_address = '0.0.0.0:5004'
    host, port = web_address.split(':')
    logger.info(f"服务器运行在 http://{web_address}")
    app.run(host=host, port=int(port), debug=True)
  except Exception as e:
    logger.error(f"[app]启动错误: {str(e)}")
