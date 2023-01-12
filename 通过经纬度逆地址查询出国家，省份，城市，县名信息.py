# -*- codeing = utf-8 -*-
# @Time :2023/1/12 13:53
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  通过经纬度逆地址查询出国家，省份，城市，县名信息.py

import requests


class BaiduMap:
    """
    处理与百度地图API相关的所有操作
    """

    def __init__(self, ak: str):
        """
        初始化类
        :param ak: 从百度地图API控制台处获取到的AK
        """
        self.ak = ak
        self.reverse_geocoding_url = 'http://api.map.baidu.com/reverse_geocoding/v3/'
        self.s = requests.Session()

    def get_location(self, lat: float, lng: float) -> dict:
        """
        根据提供的经纬度坐标获取地理位置信息
        :param lat: 纬度
        :param lng: 经度
        :return:
        """
        params = {
            'ak': self.ak,
            'output': 'json',
            'coordtype': 'wgs84ll',
            'location': f'{lat},{lng}',
        }
        resp = self.s.get(url=self.reverse_geocoding_url, params=params).json()
        address = resp['result']['addressComponent']

        # 仅返回其中的省市县信息
        return {
            item: address[item] for item in ['country', 'province', 'city', 'district']
        }


baidumap = BaiduMap(r'QIyPrGZctztQKkePpgSvRvmjIraFeyfK')
print(baidumap.get_location(10.3833, 114.367))
