# -*- coding: utf-8 -*-
# -------------------------------
# @项目：pyProject
# @文件：约束llm结构化输出.py
# @时间：2024/9/9 16:50
# @作者：xming
# -------------------------------
import json
from typing import List

from flask import Flask, make_response
from flask_cors import CORS
from llm2json.output import JSONParser
from llm2json.prompts import Templates
from llm2json.prompts.schema import BaseModel, Field

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'https://spark-api-open.xf-yun.com/v1/chat/completions'
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = '375e92d4'
SPARKAI_API_SECRET = 'ZTE5Y2M0NzQzNTFlNGExMTMxM2Y3ODE3'
SPARKAI_API_KEY = '4a52ae24d264e3c36b9c1bd013e8bd06'
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'general'

app = Flask(__name__)
CORS(app, resources={r"/*": {}})


def ernieChat(content):
  from openai import OpenAI
  client = OpenAI(
      # 控制台获取key和secret拼接，假使控制台获取的APIPassword是123456
      api_key="zZHKUdiCfsNvQTnnIeKB:zhAkeSceUCAtQLyTiSTA",
      base_url='https://spark-api-open.xf-yun.com/v1'  # 指向讯飞星火的请求地址
  )
  completion = client.chat.completions.create(
      model=SPARKAI_DOMAIN,  # 指定请求的版本
      messages=[
        {
          "role": "user",
          "content": content
        }
      ]
  )
  print(completion.choices[0].message)
  return completion.choices[0].message


class ShiTi(BaseModel):
  name: str = Field(description="实体名称")
  type: str = Field(description="实体内容")


class ChouQu(BaseModel):
  title: str = Field(description="实体类型")
  data: List[ShiTi] = Field(description="实体")


correct_example = '''
{
	"organization": [
		{
			"name": "美军第3舰队",
			"type": "军事单位"
		},
		{
			"name": "智利海军",
			"type": "军事单位"
		},
		{
			"name": "日本海上自卫队",
			"type": "军事单位"
		},
		{
			"name": "澳大利亚皇家空军",
			"type": "军事单位"
		},
		{
			"name": "加拿大联合行动指挥部",
			"type": "军事单位"
		}
	],
	"person": [
		{
			"name": "约翰·韦德",
			"type": "海军中将"
		},
		{
			"name": "阿尔韦托·格雷罗",
			"type": "准将"
		},
		{
			"name": "横田和司",
			"type": "少将"
		},
		{
			"name": "莫里斯",
			"type": "队长"
		},
		{
			"name": "莫纳汉",
			"type": "总监"
		}
	],
	"facility": [
		{
			"name": "珍珠港海军基地",
			"type": "军事设施"
		}
	],
	"event": [
		{
			"name": "环太平洋军演",
			"type": "2024年6月27日-8月1日"
		}
	]
}
'''


def generateQuestionnaire(topic, nums):
  t = Templates(prompt="""
               现在你作为一位领域实体识别与抽取专家，我将提供一段新闻文本，请你从中抽取关键实体信息。
               
               用户给定的文本: 
               2024年5月4日，美国印太司令部在夏威夷珍珠港举行指挥权变更仪式：任期届满的约翰·阿奎利诺上将卸任退役，原太平洋舰队司令塞缪尔·帕帕罗上将接替了他的职务。
著名战舰“密苏里”号（BB-63）成为这次换帅仪式的背景板。该舰是美国海上力量的象征，也是“二战”盟国取得最终胜利的见证者。
美国国防部长劳埃德·奥斯丁和参联会主席查尔斯·布朗空军上将参加了换帅仪式。
美国印度洋-太平洋司令部（简称印太司令部，原名太平洋司令部）是美国历史最悠久、规模最大的作战司令部，管理这一区域的美国陆军、海军、空军、海军陆战队、海岸警卫队共计38万人，负责美国在印太区域的所有军事活动。辖区覆盖36个国家、14个时区和全球50%以上的人口。
在此之前，美国太平洋舰队也更换了新的指挥官，以弥补塞缪尔·帕帕罗上将升职后留下的空缺。下面来了解一下这三人的基本情况：
约翰·克里斯·阿奎利诺（JohnChristopher Aquilino）海军上将。1961年出生于纽约州亨廷顿，1984年毕业于美国海军学院，1986年成为海军飞行员，之后毕业于海军战斗机武器学校（TOPGUN）。
驾驶机型：A-4、F-5、F-14A/B、F-16N、F/A-18C/E/F；飞行时间：5100 小时；航母拦阻着舰：1150次。
约翰·阿奎利诺上将在美国海军服役了40年。因此他在2024年2月获得了“老山羊”奖，该奖授予服役时间最长的美国海军学院毕业生。
他曾在第11（VF-11）“红色开膛手”、第142(VF-142)“幽灵骑士”、第41(VFA-41)“黑桃A”、 第43(VFA-43)“挑战者”中队担任飞行员、中队长。搭载平台：“肯尼迪”号（CV-67）、“福莱斯特”号（CVA-59）、“罗斯福”号（CVN-71）、“华盛顿 ”号（CVN-73）、“布什”号（CVN-77）。
约翰·阿奎利诺参加过“拒绝飞行”、“蓄意部队”、“南方守望”、“高贵之鹰”、“持久自由”和“伊拉克自由”等军事行动；指挥过第2舰载机联队和“布什”号航母打击群。
陆上职务担任过大西洋打击武器和战术学校教官；海军作战部副部长助理；国防部长办公室武器系统和先进发展助理；大西洋海军航空兵战备和训练总监；舰队司令部司令执行助理。
之后担任太平洋舰队海上作战总监；海军中央司令部/第五舰队/联合海上部队司令；海军作战部副部长，负责作战、计划和战略。
2018年5月-2021年4月：第36任太平洋舰队司令。
2021年4月-2024年5月：第26任印太司令部司令。
塞缪尔·帕帕罗（Samuel John Paparo Jr）海军上将，1964年出生于宾州莫顿。他的父亲是一名陆战队士兵，祖父是一名二战水兵。1987年毕业于维拉诺瓦大学，之后通过航空兵军官候选学校（AOCS）进入海军，毕业于海军战斗机武器学校（TOPGUN）。
                """,
                field=ChouQu,
                correct_example=correct_example)

  template = t.invoke()
  ernieResult = ernieChat(template)
  parser = JSONParser()
  result = parser.to_dict(ernieResult)
  return result


@app.route('/')
def index():
  return 'welcome to my webpage!'


@app.route('/generate', methods=['GET'])
def generate():
  # topic = request.json.get('topic')
  # nums = request.json.get('nums')

  result = generateQuestionnaire(None, None)

  return make_response(json.dumps(result), 200)


if __name__ == "__main__":
  app.run(port=2024, host="0.0.0.0", debug=True)
