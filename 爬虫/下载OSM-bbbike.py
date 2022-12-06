# -*- codeing = utf-8 -*-
# @Time :2022/12/6 15:48
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载OSM-bbbike.py
import hashlib
import logging
import os
from urllib.error import URLError

import requests
from fake_useragent import UserAgent
from tqdm import tqdm

SaveDir = "D:\RS_data\OSM"
base_url = "https://download.bbbike.org/osm/bbbike/"


def get_file_md5_top10m(file_name):
    """
    根据前10兆计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_name, 'rb') as fobj:
        data = fobj.read(1024 * 1024 * 10)
        m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


class OSMDownload(object):
    def __init__(self):
        # 下载请求链接
        # https://download.bbbike.org/osm/bbbike/Aachen/Aachen.osm.shp.zip
        self.url = "https://download.bbbike.org/osm/bbbike/{}/{}.osm.shp.zip"
        # 产生随机的User - Agent请求头进行访问
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 30):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }

    # 请求网站获取url
    def download(self, url, out):
        # toDo 添加代理，更新反扒
        total = None
        try:
            # fh = urlopen(Request(url, headers=headers), context=CTX)
            # shutil.copyfileobj(fh, out)
            response = requests.get(url, headers=self.headers, timeout=30, stream=True)

            # 在出现 http 错误时引发异常
            response.raise_for_status()

            # 添加下载进度条
            total = int(response.headers.get('content-length', 0))
            with open(out, 'wb') as file, tqdm(
                    desc=out,
                    total=total,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)
                response.close()
        except URLError as e:
            logging.error('Failed to make request: %s' % e.reason)
        except requests.exceptions.HTTPError as e:
            # handle any errors here
            logging.error('Failed to make request: %s' % e)
        return total

    def main(self, region):

        url = self.url.format(region, region)
        print("start download html:{}".format(url))

        # 数据下载
        if not os.path.exists(SaveDir):
            os.makedirs(SaveDir)
        file_name = url.split('/')[-1]
        path = os.path.join(SaveDir, file_name)

        # 这一步判断本地是否存在该文件，如果不存在就下载，存在的话就跳过
        file_size = None
        if not os.path.exists(path):
            print('downloading: ', path)
            file_size = self.download(url, path)
        else:
            # 如果存在，但是字节数为空，则重新下载 todo 如果字节数对应不上网站对数据的描述，是不是也可以重新下载
            if not os.path.getsize(path):
                print('downloading: ', path)
                file_size = self.download(url, path)
            else:
                stats = os.stat(path)
                print(stats.st_size)
                file_size = stats.st_size
                print('skipping: ', path)

        file_md5 = get_file_md5_top10m(path)
        print("数据md5为：" + file_md5)
        data = {"id": file_md5}

        # data_json = json.dumps(data)
        # with open(SaveDir + "/" + "md5" + ".modisjson", "wb") as f:
        #     写文件用bytes而不是str，所以要转码
        #      f.write(bytes(data_json, "utf-8"))


if __name__ == '__main__':
    spider = OSMDownload()
    region = "Beijing"
    spider.main(region)
