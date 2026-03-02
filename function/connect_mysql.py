import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
from function.read_file import control_file
from function.print_log import log

mysql_config = control_file().read_yaml()['mysql']

class connect_mysql:

    def __init__(self):
        self.conn = None
        self.cursor = None

    @contextmanager
    def do_connect(self):
        try:
            self.conn = pymysql.connect(host=mysql_config['host'],
                                        port=mysql_config['port'],
                                        user=mysql_config['user'],
                                        password=mysql_config['password'],
                                        database=mysql_config['database'],
                                        charset='utf8mb4',
                                        cursorclass=DictCursor,  # 用于返回字典形式
                                        autocommit=True)
            self.cursor = self.conn.cursor()
            log.info('数据库已连接！')
            yield self.cursor
        except Exception as e:
            log.info(f'数据库连接失败！{e}')
            raise
        finally:
            if self.cursor:
                self.cursor.close()
            if self.cursor:
                self.cursor.close()
            log.info('数据库已关闭！')

    def do_select(self,sql:str, params:tuple = None):
        with self.do_connect() as do_con:
            do_con.execute(sql,params)
        log.info(f'查询结果如下：\n{do_con.fetchall()}')
        return do_con.fetchall()

    def do_update(self,sql:str, params:tuple = None):
        pass


do_connect = connect_mysql()


if __name__ == '__main__':
    do_connect = connect_mysql()
    do_connect.do_select('select * from test.test_case where id = %s',(1,))
