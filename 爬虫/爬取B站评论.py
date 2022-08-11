import re
import time

import requests
import urllib3

urllib3.disable_warnings()

hd = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
}


def get_oid(BV_CODE: str) -> str:
    bv = BV_CODE[2:] if "BV" == BV_CODE[:2] else BV_CODE
    video_url = f"https://www.bilibili.com/video/BV{bv}"
    r = requests.get(video_url, headers=hd, verify=False)
    r.raise_for_status()
    return re.search(r'window.__INITIAL_STATE__={"aid":(\d+)', r.text).group(1)


def get_data(page: int, oid: str):
    time.sleep(sleep_time)  # 减少访问频率，防止IP封禁
    api_url = f"https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&sort=2&_={int(time.time())}"
    print(f'正在处理:{api_url}')
    r = requests.get(api_url, headers=hd, verify=False)
    r.raise_for_status()
    return r.json()['data']['replies'], r.json()['data']['page']['count']


def get_folded_reply(page: int, oid: str, root: int):
    time.sleep(sleep_time)  # 减少访问频率，防止IP封禁
    url = f'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={page}&type=1&oid={oid}&ps=10&root={root}&_={int(time.time())}'
    print(f'正在处理:{url}')  # 由于需要减缓访问频率，防止IP封禁，打印访问网址以查看访问进程
    r = requests.get(url, headers=hd, verify=False)
    r.raise_for_status()
    return r.json()['data']


def re_reply2(temp, root):
    _ = []
    for item in temp:
        if item[2] == root:
            _.append((item[1], 'FIRST'))
            continue
        for item2 in temp:
            if item[2] == item2[1]:
                _.append((item[1], item2[1]))
                break
        else:  # 回复对象被删除
            _.append((item[1], None))
    return _


def loop_folded_reply(root: int, rcount: int):
    temp = []
    temp2 = {}
    end_page = (rcount - 1) // 10 + 1 if (rcount - 1) // 10 + 1 <= pages2 else pages2
    for page in range(1, end_page + 1):
        data = get_folded_reply(page, oid=oid, root=root)
        if not data['replies']:
            continue
        for item in data['replies']:
            mid = item['mid']
            rpid = item['rpid']
            parent = item['parent']
            dialog = item['dialog']
            rcount = item['rcount']
            like = item['like']
            ctime = item['ctime']
            name = item['member']['uname']
            # message = item['content']['message']
            message = re.sub(r'\t|\n|回复 @.*? :', '', item['content']['message'])
            # print(dialog, rpid, parent, name, message)
            temp.append([dialog, rpid, parent, name, message])
            temp2[rpid] = [mid, message, name, like, ctime]
        # else:
        #     break
    pointer = re_reply2(temp, root)

    def loop(pid, tab):
        # 用于递归查找单指
        for item in pointer:
            if pid == item[1]:
                mid, message, name, like, ctime = temp2[item[0]]
                f.write(
                    f'INSERT INTO `blbl_content`(`uid`, `uname`,`time`, `video_bv`,`content`) VALUES ({mid},"{name}","{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}","{bv}","{message}");\n')
                loop(item[0], tab + 1)

    for rpid in [i for i, j in pointer if j == 'FIRST']:
        mid, message, name, like, ctime = temp2[rpid]
        f.write(
            f'INSERT INTO `blbl_content`(`uid`, `uname`,`time`, `video_bv`,`content`) VALUES ({mid},"{name}","{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}","{bv}","{message}");\n')
        loop(rpid, tab=1)

    for ii, rpid in enumerate([i for i, j in pointer if not j]):
        if ii == 0:
            f.write(f'|\t|->\t评论已被删除\n')
        mid, message, name, like, ctime = temp2[rpid]
        f.write(
            f'INSERT INTO `blbl_content`(`uid`, `uname`,`time`, `video_bv`,`content`) VALUES ({mid},"{name}","{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}","{bv}","{message}");\n')
        loop(rpid, tab=3)


def get_reply(data, tab=0):
    if not data:
        return
    for item in data:
        mid = item['mid']
        rpid = item['rpid']
        count = item['count']
        rcount = item['rcount']
        like = item['like']
        ctime = item['ctime']
        name = item['member']['uname']
        message = re.sub(r'\t|\n|回复 @.*? :', '', item['content']['message'])
        f.write(
            f'INSERT INTO `blbl_content`(`uid`, `uname`,`time`, `video_bv`,`content`) VALUES ({mid},"{name}","{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ctime))}","{bv}","{message}");\n')
        print(f'爬取评论:UID-{mid}\tUSER-{name}\t点赞-{like}')
        if 0 < rcount <= 3:
            get_reply(item['replies'], tab=1)
        elif rcount > 3:
            loop_folded_reply(root=rpid, rcount=rcount)


if __name__ == '__main__':
    pages1 = int(input('请输入爬取"视频评论"的页数(每页20条),推荐10:'))
    pages2 = int(input('请输入爬取"评论回复(楼中楼)"的页数(每页10条),推荐03:'))

    # 每次调用链接后的休息时间，胆子大就改小点
    sleep_time = 2.1  # 访问网页间隔，防止IP被禁，若运行程序后出现无法访问评论区的现象，等待2小时即可

    # 记得在这里输入视频的BV号！
    bv = 'BV1A5411E7kc'

    oid = get_oid(bv)
    f = open(f'{time.strftime("%Y%m%d-%H%M")}.txt', 'w', encoding='utf-8')
    page = 1
    while True:
        try:
            data, reply_num = get_data(page, oid)
            get_reply(data)  # 遍历所有回复
            end_page = reply_num // 20 + 1 if reply_num // 20 + 1 <= pages1 else pages1
            if page == end_page:
                break
            page += 1
        except Exception as e:
            print('ERROR:', e)
            print('退出循环 结束')
            break
    f.close()
