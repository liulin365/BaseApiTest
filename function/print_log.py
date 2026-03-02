import logging
from datetime import datetime
from pathlib import Path

class set_log:

    def __init__(self):
        self.today = datetime.now().strftime('%Y%m%d')
        self.log_dir = Path.cwd().parent / 'logs'
        self.log_dir.mkdir(exist_ok=True)

    def get_log(self):
        '''生成日志管理器 + 设置日志级别'''
        logger = logging.getLogger('API_Test')
        logger.setLevel(logging.DEBUG)

        '''设置日志打印出口'''
        # 控制台实时打印日志
        console = logging.StreamHandler()
        console.setLevel(logging.INFO) # 设置日志级别
        # 用文件记录日志
        log_file = logging.FileHandler(filename=self.log_dir / f"case_{self.today}.log",
                                       mode='a',
                                       encoding='utf-8')
        log_file.setLevel(logging.DEBUG) # 设置日志级别

        '''设置日志内容的格式'''
        log_format = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
        # 控制台使用该格式
        console.setFormatter(log_format)
        # 日志文件使用该格式
        log_file.setFormatter(log_format)

        '''绑定Handler'''
        logger.addHandler(console)
        logger.addHandler(log_file)

        return logger


log = set_log().get_log()

if __name__ == '__main__':
    logger = set_log()
    log = logger.get_log()
    log.info('这是info级别的日志！') # 已经有出口在控制台了，不用使用print()方法打印










