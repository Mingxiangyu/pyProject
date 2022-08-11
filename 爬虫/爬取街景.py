import json
import os

import pandas as pd
import requests


#  initialize
def get_json(index, bbox):
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:4780'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:4780'
    app_access_token = 'MLY|7495017997236794|965d4238d3ccee5136a39f79c66e9a6d'  # create your access token at https://mapillary.com/developer
    access_token = 'MLY|7495017997236794|965d4238d3ccee5136a39f79c66e9a6d'
    fields = 'id,thumb_2048_url,geometry,captured_at,camera_type'
    Authorization = 'OAuth AQCWI1Td7K5dHNGxLvQFUrm1oK9t1zwTrevTQCqD-MmvMNoDevmX6ce6FVG2MNVbAzXDWXsND5NSqpUQAzkhKIGj9cYVI_u-6gLeEZ8txw6YCp27RapNbZNDS03HkXfSrk7IO_sFLTr9ol4BJM1fNtk7LmTs3HMOS9o4TX2eIq-5dp0Wk6KgG-2LUSD_TGf3I4Xmo59x20ZPd_I0qFuvvp10KstiqwLUYyLDEcs5kO_46KlSLuIhWqKl4qk7AnfD1bIpsUVDA5vuzs8fSPUvIJgJ'
    url = 'https://graph.mapillary.com//images?access_token={}&Authorization={}&fields={}&bbox={}'.format(access_token,
                                                                                                          Authorization,
                                                                                                          fields, bbox)
    # or instead of adding it to the url, add the token in headers (strongly recommended for user tokens)
    headers = {"Authorization": "OAuth {}".format(app_access_token)}
    response = requests.get(url, headers, stream=True, timeout=10)
    data = response.json()
    json_name = './all_json/' + str(index) + '.json'
    with open(json_name, "w") as outfile:
        json.dump(data, outfile)


def get_json1(index, bbox):
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:4780'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:4780'
    app_access_token = 'MLY|7495017997236794|965d4238d3ccee5136a39f79c66e9a6d'  # create your access token at https://mapillary.com/developer
    access_token = 'MLY|7495017997236794|965d4238d3ccee5136a39f79c66e9a6d'
    fields = 'id,thumb_2048_url,geometry,captured_at,camera_type'
    Authorization = 'OAuth AQCWI1Td7K5dHNGxLvQFUrm1oK9t1zwTrevTQCqD-MmvMNoDevmX6ce6FVG2MNVbAzXDWXsND5NSqpUQAzkhKIGj9cYVI_u-6gLeEZ8txw6YCp27RapNbZNDS03HkXfSrk7IO_sFLTr9ol4BJM1fNtk7LmTs3HMOS9o4TX2eIq-5dp0Wk6KgG-2LUSD_TGf3I4Xmo59x20ZPd_I0qFuvvp10KstiqwLUYyLDEcs5kO_46KlSLuIhWqKl4qk7AnfD1bIpsUVDA5vuzs8fSPUvIJgJ'
    url = 'https://graph.mapillary.com//images?access_token={}&Authorization={}&fields={}&bbox={}'.format(access_token,
                                                                                                          Authorization,
                                                                                                          fields, bbox)
    # or instead of adding it to the url, add the token in headers (strongly recommended for user tokens)
    headers = {"Authorization": "OAuth {}".format(app_access_token)}
    try:
        response = requests.get(url, headers, stream=True, timeout=10)
    except:
        return
    flag = 0
    while (response.status_code != 200):
        flag += 1
        try:
            response = requests.get(url, headers, stream=True, timeout=10)
        except:
            continue
    data = response.json()
    json_name = './json_copy/' + str(index) + '.json'
    with open(json_name, "w") as outfile:
        json.dump(data, outfile)


def download_img(img_url, image_name):
    try:
        r = requests.get(img_url, stream=True, timeout=10)
    except:
        return
    flag = 0
    while (r.status_code != 200):
        flag += 1
        try:
            r = requests.get(img_url, stream=True, timeout=10)
        except:
            continue
        if flag == 10:
            break

    # print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(image_name, 'wb').write(r.content)  # 将内容写入图片
        print("done")


def write_excel(json_name):
    data = open(json_name)
    test = json.load(data)
    temp = test['data']
    result_id = []
    result_url = []
    result_lat = []
    result_lon = []
    result_perspective = []
    result_capture_at = []
    index = 0
    for data in temp:
        id = data['id']
        url = data['thumb_2048_url']
        geometry = data['geometry']
        lat = geometry['coordinates'][0]
        lon = geometry['coordinates'][1]
        capture_at = data['captured_at']
        try:
            perspective = data['camera_type']
        except KeyError:
            perspective = 'None'
        capture_at = data['captured_at']  # result_id.append(id)
        result_id.append(id)
        result_url.append(url)
        result_lat.append(lat)
        result_lon.append(lon)
        result_perspective.append(perspective)
        result_capture_at.append(capture_at)

    result_dict = {
        'id': result_id,
        'url': result_url,
        'lat': result_lat,
        'lon': result_lon,
        'perspective': result_perspective,
        'capture_at': result_capture_at
    }

    result = pd.DataFrame(result_dict)
    result['capture_at'] = result['capture_at'].apply(lambda x: '{:.0f}'.format(x))
    result.to_excel('Ago.xls')


def charge_exists(download_path):
    if os.path.exists(download_path):
        pass
    else:
        os.mkdir(download_path)


def combine_json(all_json_path):
    path = all_json_path
    jsons = os.listdir(path)
    ids = set()
    dictd = {}
    for js in jsons:
        f = open(path + js, 'r')
        setting = json.load(f)
        print(len(setting['data']))
        for s in setting['data']:
            if s['id'] not in dictd.keys():
                dictd[s['id']] = s
    re = {'data': []}
    for key in dictd.keys():
        re['data'].append(dictd[key])
    print(len(re['data']))
    with open("merge.json", "w") as f:
        json.dump(re, f, indent=4)
        print("加载入文件完成...")


if __name__ == '__main__':
    # data = pd.read_excel('all_fish_net.xls')
    # 将记录放入 json 之中
    # for i in range(387,all_length):
    #     index = data['index'][i]
    #     bbox = data['Bound'][i]
    #     get_json1(index,bbox)
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:4780'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:4780'

    # json_dir = './all_json/'
    # json_files = os.listdir(json_dir)
    # for i in range(len(json_files)):

    # tile = json_files[i].split('.')[0]
    for i in os.listdir('./all_json'):
        # print(os.getcwd())
        tile = i.split('.json')[0]
        down_load_tile_dir = './download/tile_' + tile
        print(tile)
        if int(tile) >= 2432 and int(tile) <= 2500:  # //根据需要自行设置tile范围
            print(tile)
        # bbox = data['Bound'][int(tile)]
        # get_json1(tile,bbox)
        charge_exists(down_load_tile_dir)
        json_file = './all_json/' + i
        f = open(json_file, encoding='utf-8')
        setting = json.load(f)
        for data in setting['data']:
            url = data['thumb_2048_url']
            id = data['id']
            image_name = down_load_tile_dir + '/' + id + '.jpg'
            download_img(url, image_name)
