import logging
import os
import warnings
from logging.handlers import RotatingFileHandler

import kaldifst
from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
from funasr import AutoModel
from gevent.pywsgi import WSGIServer, WSGIHandler

import tools

warnings.filterwarnings('ignore')

ROOT_DIR = os.getcwd()
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
TMP_DIR = os.path.join(STATIC_DIR, 'tmp')
RULE_DIR = os.path.join(STATIC_DIR, 'rules')

# 指定魔塔模型缓存路径
os.environ['MODELSCOPE_CACHE'] = '/models'
# os.environ['MODELSCOPE_CACHE'] = '/Users/sunshanming/localHub'

log = logging.getLogger('werkzeug')
log.handlers[:] = []
log.setLevel(logging.WARNING)

root_log = logging.getLogger()  # Flask的根日志记录器
root_log.handlers = []
root_log.setLevel(logging.WARNING)

# model_conf
# model = AutoModel(model="iic/SenseVoiceSmall",
#                   # vad_model="fsmn-vad",
#                   # punc_model="ct-punc",
#                   device='cuda:0'
#                   # spk_model="cam++"
#                   )

model = AutoModel(
    model="iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
    # spk_model="iic/speech_campplus_sv_zh-cn_16k-common",
    device='cuda:0'
)

r = os.getenv('RULE', 'on')
rules = ''
normalizer = None

if r == 'on':
  rules = os.path.join(RULE_DIR, 'itn_zh_number.fst')

  if not os.path.exists(rules):
    rules = ''
  else:
    InverseTextNormalizer = kaldifst.TextNormalizer
    normalizer = InverseTextNormalizer(rules)


class CustomRequestHandler(WSGIHandler):
  def log_request(self):
    pass


app = Flask(__name__)
CORS(app)  # 允许跨域

# 配置日志
app.logger.setLevel(logging.WARNING)  # 设置日志级别为 INFO
# 创建 RotatingFileHandler 对象，设置写入的文件路径和大小限制
file_handler = RotatingFileHandler(os.path.join(ROOT_DIR, 'funAsr.log'),
                                   maxBytes=1024 * 1024, backupCount=5)
# 创建日志的格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 设置文件处理器的级别和格式
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)
# 将文件处理器添加到日志记录器中
app.logger.addHandler(file_handler)

@app.route('/static/<path:filename>')
def static_files(filename):
  return send_from_directory(app.config['STATIC_FOLDER'], filename)


@app.route('/')
def index():
  return render_template("index.html", language='zh')


@app.route('/analysis', methods=['POST'])
def analysis():
  try:
    hot_word = '遇袭 松山 拜登 特朗普 哈尼亚'

    if request.form.get('hot_word') is not None:
      hot_word = request.form.get('hot_word')

    # 获取上传的文件
    audio_file = request.files.get("file") or request.form.get("file")
    noextname, ext = os.path.splitext(audio_file.filename)
    ext = ext.lower()
    source_file = os.path.join(TMP_DIR, f'{noextname}{ext}')
    # if not os.path.exists(source_file) or os.path.getsize(source_file) == 0: #是否覆盖原始文件
    audio_file.save(source_file)

    noextname, ext = os.path.splitext(source_file)
    wav_file = os.path.join(TMP_DIR, f'{noextname}.wav')
    print(f'{wav_file=}')
    params = [
      "-i",
      source_file,
    ]
    if not os.path.exists(wav_file) or os.path.getsize(wav_file) == 0:
      if ext in ['.mp4', '.mov', '.avi', '.mkv', '.mpeg', '.mp3', '.flac']:
        if ext not in ['.mp3', '.flac']:
          params.append('-vn')
        params.append(wav_file)
        rs = tools.runffmpeg(params)
        if rs != 'ok':
          return jsonify({"code": 1, "msg": rs})
      elif ext == '.speex':
        params.append(wav_file)
        rs = tools.runffmpeg(params)
        if rs != 'ok':
          return jsonify({"code": 1, "msg": rs})
      elif ext == '.wav':
        wav_file = source_file
      else:
        return jsonify({"code": 1, "msg": f"格式不支持 {ext}"})
    print(f'{ext=}')
    print(f'{source_file=}')


    res = model.generate(
        input=wav_file,
        hotword=hot_word,
        language="auto",
        return_raw_text=False,  # 返回按带时间戳的等长空间分割的原始文本识别结果
        use_itn=True  # 输出结果中是否包含标点与逆文本正则化
    )
    text = ""
    if rules != '' and normalizer is not None:
      text = normalizer(res[0]['text'])

    # res = model.generate(
    #     input=wav_file,
    #     hotword=hot_word,
    #     language="auto",
    #     use_itn=True #输出结果中是否包含标点与逆文本正则化
    # )
    # text = ""
    # if rules != '' and normalizer is not None:
    #   res[0]['text'] = normalizer(res[0]['text'])
    #   pattern = r"<\|(.+?)\|><\|(.+?)\|><\|(.+?)\|><\|(.+?)\|>(.+)"
    #   match = re.match(pattern, res[0]['text'])
    #   language, emotion, audio_type, itn, text = match.groups()

    return jsonify({"code": 0, "msg": 'ok', "data": text,
                    'filename': f'{noextname}{ext}'})
  except Exception as e:
    print(e)
    app.logger.error(f'[api]error: {e}')
    return jsonify({'code': 2, 'msg': str(e)})


@app.route('/upload', methods=['POST'])
def upload():
  try:
    # 获取上传的文件
    audio_file = request.files['audio']
    # 如果是mp4
    noextname, ext = os.path.splitext(audio_file.filename)
    ext = ext.lower()
    # 如果是视频，先分离
    wav_file = os.path.join(TMP_DIR, f'{noextname}{ext}')
    if os.path.exists(wav_file) and os.path.getsize(wav_file) > 0:
      return jsonify(
          {'code': 0, 'msg': 'zh', "data": os.path.basename(wav_file)})
    msg = ""

    audio_file.save(wav_file)

    # 返回成功的响应
    return jsonify({'code': 0, 'msg': '上传成功' + msg,
                    "data": os.path.basename(wav_file)})
  except Exception as e:
    app.logger.error(f'[upload]error: {e}')
    return jsonify({'code': 2, 'msg': '上传失败'})


@app.route('/api', methods=['GET', 'POST'])
def api():
  source_file = ''
  wav_file = ''
  is_delete = None
  try:
    # 获取上传的文件

    hot_word = '遇袭 松山 拜登 特朗普 哈尼亚'

    is_delete = request.form.get('is_delete', None)

    if request.form.get('hot_word') is not None:
      hot_word = request.form.get('hot_word')

    if request.form.get('wav_name') is not None:
      source_file = os.path.join(TMP_DIR, request.form.get('wav_name'))
    else:
      audio_file = request.files.get("file") or request.form.get("file")
      noextname, ext = os.path.splitext(audio_file.filename)
      ext = ext.lower()
      source_file = os.path.join(TMP_DIR, f'{noextname}{ext}')
      if not os.path.exists(source_file) or os.path.getsize(source_file) == 0:
        audio_file.save(source_file)

    noextname, ext = os.path.splitext(source_file)
    wav_file = os.path.join(TMP_DIR, f'{noextname}.wav')
    print(f'{wav_file=}')
    params = [
      "-i",
      source_file,
    ]
    if not os.path.exists(wav_file) or os.path.getsize(wav_file) == 0:
      if ext in ['.mp4', '.mov', '.avi', '.mkv', '.mpeg', '.mp3', '.flac']:

        if ext not in ['.mp3', '.flac']:
          params.append('-vn')
        params.append(wav_file)
        rs = tools.runffmpeg(params)
        if rs != 'ok':
          return jsonify({"code": 1, "msg": rs})
      elif ext == '.speex':
        params.append(wav_file)
        rs = tools.runffmpeg(params)
        if rs != 'ok':
          return jsonify({"code": 1, "msg": rs})
      elif ext == '.wav':
        wav_file = source_file
      else:
        return jsonify({"code": 1, "msg": f"格式不支持 {ext}"})
    print(f'{ext=}')
    print(f'{source_file=}')

    res = model.generate(
        input=wav_file,
        hotword=hot_word,
        language="auto",
        return_raw_text=False,  # 返回按带时间戳的等长空间分割的原始文本识别结果
        use_itn=True  # 输出结果中是否包含标点与逆文本正则化
    )
    text = ""
    if rules != '' and normalizer is not None:
      text = normalizer(res[0]['text'])

    # res = model.generate(
    #     input=wav_file,
    #     hotword=hot_word,
    #     language="auto",
    #     use_itn=True #输出结果中是否包含标点与逆文本正则化
    # )
    # text = ""
    # if rules != '' and normalizer is not None:
    #   res[0]['text'] = normalizer(res[0]['text'])
    #   pattern = r"<\|(.+?)\|><\|(.+?)\|><\|(.+?)\|><\|(.+?)\|>(.+)"
    #   match = re.match(pattern, res[0]['text'])
    #   language, emotion, audio_type, itn, text = match.groups()

    # res = model.generate(
    #     input=wav_file,
    #     hotword=hot_word,
    # )
    #
    # if rules != '' and normalizer is not None:
    #   res[0]['text'] = normalizer(res[0]['text'])

    return jsonify(
        {"code": 0, "msg": 'ok', "data": text, 'filename': f'{noextname}{ext}'})
  except Exception as e:
    print(e)
    app.logger.error(f'[api]error: {e}')
    return jsonify({'code': 2, 'msg': str(e)})
  finally:
    if is_delete is None:
      if os.path.exists(wav_file):
        os.remove(source_file)
      if os.path.exists(source_file):
        os.remove(source_file)


if __name__ == '__main__':
  http_server = None
  try:
    try:
      web_address = '0.0.0.0:5002'
      host = web_address.split(':')
      http_server = WSGIServer((host[0], int(host[1])), app,
                               handler_class=CustomRequestHandler)

      app.logger.info(f" http://{web_address}")

      http_server.serve_forever(stop_timeout=10)
    finally:
      if http_server:
        http_server.stop()
  except Exception as e:
    if http_server:
      http_server.stop()
    print("error:" + str(e))
    app.logger.error(f"[app]start error:{str(e)}")
