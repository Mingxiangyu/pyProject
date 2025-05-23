import logging
import sys
import time

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H: %M:%S')
    # 监听路径
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    print('当前文件路径为：' + path)
    # 生成事件处理器对象
    event_handler = LoggingEventHandler()
    # 生成监控器对象
    observer = Observer()
    # 注册事件处理器,配置监控目录
    observer.schedule(event_handler, path, recursive=True)
    # 监控器启动一创建线程
    observer.start()

    # 以下代码是为了保持主线程运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    # 等待其他的子线程执行结束之后,主线程再终止
    observer.join()
