# -*- codeing = utf-8 -*-
# @Time :2022/12/5 16:40
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  多进程复制文件，多线程复制文件加显示进度条.py

# coding=utf-8

import os
import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Pool, Manager
from threading import Thread


class copyf_show:
    """
    # 多进程复制文件
    # 多进程复制文件加显示进度
    # despath 目标目录
    # soupath 源目录
    """

    def __init__(self, despath, soupath):
        self.d = despath
        self.s = soupath
        self.st = os.path.dirname(soupath)
        self.q = Manager().Queue()
        self.show_d = {}  # show
        self.count = 0  # show
        self.total = 0  # show
        if not os.path.isdir(self.d): os.mkdir(self.d)

    def pro_pool(self):
        """
        # 实时复制文件
        # 先启动扫描目录，向管道发送数据
        # 开启进程池，等待管道接受数据
        # 一个进程复制一个目录层文件
        """
        print('正在从 {} 复制所有文件到 {}'.format(self.s, self.d))
        time_node = time.time()
        count = 0
        ps = Process(target=self.scanfile)
        ps.start()
        p = Pool()  # 进程数量
        while True:
            if self.q.empty(): continue
            t = self.q.get()
            if not t: break
            count += len(list(t.values())[0])
            p.apply_async(self.pro_cp, (t,))
        ps.join()
        p.close()
        p.join()
        print('总计文件数量：{}\n耗时：{} 秒'.format(count, round(time.time() - time_node, 2)))

    def scanfile(self):
        """
        # 扫描一层目录，生成字典
        # 绝对路径为key，文件列表为值
        # 向管道发送字典
        """
        for root, dirs, files in os.walk(self.s):
            self.q.put({root: files})
        self.q.put(False)

    def pro_cp(self, dif):
        """
        # 判断目标目录是否存在
        # 切换路径，复制文件
        """
        dpa = list(dif.keys())[0].replace(self.st, self.d)
        if not os.path.isdir(dpa): os.mkdir(dpa)
        os.chdir(dpa)
        for i, j in dif.items():
            for nn in [os.path.join(i, k) for k in j]:
                shutil.copy(nn, dpa)

    def show_fun(self):
        """
        # 开启线程城池复制文件并打印进度条
        """
        print('正在从 {} 复制所有文件到 {}'.format(self.s, self.d))
        self.show_scanfile()
        self.count = 0
        print('总计文件数量：{}'.format(self.total))
        pp = Thread(target=self.show_pgr)
        pp.setDaemon(True)  # 主程序退出结束
        pp.start()
        for d, f in self.show_d.items():
            self.show_pool(d, f)
        pp.join()

    def show_pgr(self):
        """
        # 进度条
        # 已复制数除以总数乘以100
        # 计时
        """
        time_node = time.time()
        while True:
            cls = round(self.count / self.total * 100)
            print('\r{:<100} {}%'.format('*' * cls, cls), end='')
            if cls == 100:
                print('\n耗时：{} 秒'.format(round((time.time() - time_node), 2)))
                break
            time.sleep(0.1)

    def show_scanfile(self):
        """
        # 扫描一层目录，生成字典
        # 绝对路径为key，文件列表为值
        # 
        """
        for root, dirs, files in os.walk(self.s):
            self.total += len(files)
            self.show_d.update({root: files})

    def show_pool(self, root, fl):
        """
        # root = 目录, fl = 文件列表
        # 多线程
        """
        dpa = root.replace(self.st, self.d)
        if not os.path.isdir(dpa): os.mkdir(dpa)
        os.chdir(dpa)
        with ThreadPoolExecutor(None, self.show_cp) as p:
            p.map(self.show_cp, [(root + os.sep + f, dpa) for f in fl])
        p.shutdown()
        self.count += len(fl)

    def show_cp(self, file):
        """
        # 绝对路径
        # 复制文件file = (src, dst)
        """
        shutil.copy(file[0], file[1])


if __name__ == '__main__':
    path = r'D:\GIN\py\pool_copy_file\t'
    soup = r'D:\GIN\py\photo\photo'
    t = copyf_show(path, soup)
    t.pro_pool()
    t.show_fun()
    print('Done!')
