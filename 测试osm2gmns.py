# -*- codeing = utf-8 -*-
# @Time :2023/2/16 17:44
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  测试osm2gmns.py

import osm2gmns as og
from flask import Flask

def download_and_out():
    # 下载osm文件并进行拓扑简化
    net = og.getNetFromFile('Aachen.osm.pbf')
    og.outputNetToCSV(net)


def local_and_out(file_path):
    # 读取本地osm文件并进行简化
    # filename = r"G:\xunleiDownload\Beijing.osm.gz"
    net = og.getNetFromFile(filename=file_path,
                            POI=False)
    og.connectPOIWithNet(net)
    # og.show(net)
    intersections = og.consolidateComplexIntersections(net, auto_identify=True)
    og.outputNetToCSV(net, output_folder="output_osm")
    og.show(net)

app = Flask(__name__)  # 创建flask实例


@app.route("/clean/<path:file_path>")
def spider(file_path):
    print(file_path)
    local_and_out(file_path)
    return "hello,world"


if __name__ == '__main__':
    # 启动flask，提供http接口
    app.run()
