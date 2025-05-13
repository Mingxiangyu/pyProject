import logging
import os
import warnings
from logging.handlers import RotatingFileHandler

import kaldifst
import requests
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from funasr import AutoModel
from gevent.pywsgi import WSGIHandler, WSGIServer
from werkzeug.datastructures import FileStorage

import tools

warnings.filterwarnings('ignore')

ROOT_DIR = os.getcwd()
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
TMP_DIR = os.path.join(STATIC_DIR, 'tmp')
RULE_DIR = os.path.join(STATIC_DIR, 'rules')

# 指定魔塔模型缓存路径
os.environ['MODELSCOPE_CACHE'] = './model'

# 配置日志
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# 文件日志处理
file_handler = RotatingFileHandler(
    os.path.join(ROOT_DIR, 'funAsr.log'),
    maxBytes=1024 * 1024,
    backupCount=5
)
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 初始化ASR模型
model = AutoModel(
    model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
    device='cuda:0'
)

# 初始化文本规范化
r = os.getenv('RULE', 'on')
rules = ''
normalizer = None

if r == 'on':
  rules = os.path.join(RULE_DIR, 'itn_zh_number.fst')

  if os.path.exists(rules):
    InverseTextNormalizer = kaldifst.TextNormalizer
    normalizer = InverseTextNormalizer(rules)


# 自定义WSGI处理器
class CustomRequestHandler(WSGIHandler):
  def log_request(self):
    pass


# Flask和Flask-RESTx设置
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 10  # 160 MB
CORS(app)

# 创建带Swagger文档的API
api = Api(app,
          version='1.0',
          title='音频转写API',
          description='支持音频文件转写的API服务',
          doc='/swagger'
          )

# 音频相关命名空间
audio_ns = api.namespace('audio', description='音频转写操作')

# 定义上传文件的解析器
upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage,
                           required=True,
                           help='要转写的音频文件')
upload_parser.add_argument('hot_word',
                           location='form',
                           default='遇袭 松山 拜登 特朗普 哈尼亚',
                           help='可选的热词，用于提高转写准确性')

# URL转写的解析器
url_parser = api.parser()
url_parser.add_argument('url',
                        # location='form',
                        # required=True,
                        help='音频文件的URL')
url_parser.add_argument('hot_word',
                        # location='form',
                        default='遇袭 松山 拜登 特朗普 哈尼亚',
                        help='可选的热词，用于提高转写准确性')

# 响应模型
transcription_model = api.model('Transcription', {
  'code': fields.Integer(description='状态码', required=True),
  'msg': fields.String(description='状态消息', required=True),
  'data': fields.String(description='转写文本', required=True),
  'filename': fields.String(description='原始文件名', required=True)
})


def extract_filename_from_url(url):
  """从URL提取文件名"""
  return url.split('/')[-1]


def download_file(url, file_path):
  """从URL下载文件"""
  with requests.get(url, stream=True) as response:
    response.raise_for_status()
    with open(file_path, 'wb') as file:
      for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)


def prepare_audio_file(source_file):
  """将音频文件转换为WAV格式"""
  noextname, ext = os.path.splitext(source_file)
  ext = ext.lower()
  wav_file = os.path.join(TMP_DIR, f'{noextname}.wav')

  params = ["-i", source_file]

  if not os.path.exists(wav_file) or os.path.getsize(wav_file) == 0:
    if ext in ['.mp4', '.mov', '.avi', '.mkv', '.mpeg', '.mp3', '.flac']:
      if ext not in ['.mp3', '.flac']:
        params.append('-vn')
      params.append(wav_file)
      rs = tools.runffmpeg(params)
      if rs != 'ok':
        raise ValueError(f"FFmpeg转换失败: {rs}")
    elif ext == '.speex':
      params.append(wav_file)
      rs = tools.runffmpeg(params)
      if rs != 'ok':
        raise ValueError(f"FFmpeg转换失败: {rs}")
    elif ext == '.wav':
      wav_file = source_file
    else:
      raise ValueError(f"不支持的文件格式: {ext}")

  return wav_file


@audio_ns.route('/transcribe')
class AudioTranscription(Resource):
  @api.expect(upload_parser)
  @api.marshal_with(transcription_model)
  def post(self):
    """
    音频文件转写
    上传音频文件并获取其转写文本
    """
    try:
      args = upload_parser.parse_args()
      audio_file = args['file']
      hot_word = args.get('hot_word', '遇袭 松山 拜登 特朗普 哈尼亚')

      noextname, ext = os.path.splitext(audio_file.filename)
      ext = ext.lower()
      source_file = os.path.join(TMP_DIR, f'{noextname}{ext}')
      audio_file.save(source_file)

      wav_file = prepare_audio_file(source_file)

      res = model.generate(
          input=wav_file,
          hotword=hot_word,
          language="auto",
          return_raw_text=False,
          use_itn=True
      )

      text = ""
      if rules != '' and normalizer is not None:
        text = normalizer(res[0]['text'])

      # 清理文件
      if os.path.exists(source_file):
        os.remove(source_file)

      # 清理文件
      if os.path.exists(wav_file):
        os.remove(wav_file)

      return {
        "code": 0,
        "msg": '成功',
        "data": text,
        'filename': f'{noextname}{ext}'
      }, 200

    except Exception as e:
      logger.error(f'[api]错误: {e}')
      return {'code': 2, 'msg': str(e)}, 500


@audio_ns.route('/transcribe-url')
class AudioTranscriptionFromURL(Resource):
  @api.expect(url_parser)
  @api.marshal_with(transcription_model)
  def post(self):
    """
    从URL转写音频文件
    提供音频文件的URL并获取其转写文本
    """
    try:
      # 解析参数
      args = url_parser.parse_args()
      url = args['url']
      hot_word = args.get('hot_word', '遇袭 松山 拜登 特朗普 哈尼亚')

      file_name = extract_filename_from_url(url)
      file_path = os.path.join(TMP_DIR, file_name)
      if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
      download_file(url, file_path)

      wav_file = prepare_audio_file(file_path)

      res = model.generate(
          input=wav_file,
          hotword=hot_word,
          language="auto",
          return_raw_text=False,
          use_itn=True
      )

      text = ""
      if rules != '' and normalizer is not None:
        text = normalizer(res[0]['text'])

      # 清理文件
      if os.path.exists(file_path):
        os.remove(file_path)

      return {
        "code": 0,
        "msg": '成功',
        "data": text,
        'filename': file_name
      }, 200

    except Exception as e:
      logger.error(f'[api]错误: {e}')
      return {'code': 2, 'msg': str(e)}, 500


if __name__ == '__main__':
  try:
    web_address = '0.0.0.0:5102'
    host, port = web_address.split(':')
    http_server = WSGIServer((host, int(port)), app,
                             handler_class=CustomRequestHandler)

    logger.info(f"服务器运行在 http://{web_address}")
    http_server.serve_forever(stop_timeout=10)
  except Exception as e:
    logger.error(f"[app]启动错误: {str(e)}")
