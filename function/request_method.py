import requests
import allure
from function.read_file import con_file
from function.print_log import log

base_url = con_file.read_yaml()['base_url']
header = con_file.read_yaml()['headers']
session = requests.Session()

class Do_Requests:
    def __init__(self,path):
        self.url = base_url + path
        self.path = path

    def which_method(self,method,**kwargs):
        try:
            if method == 'GET':
                response = session.get(self.url,**kwargs)
            if method == 'POST':
                response = session.post(self.url,**kwargs)
            if method == 'DELETE':
                response = session.delete(self.url,**kwargs)
            if method == 'PUT':
                response = session.put(self.url,**kwargs)
            return response
        except Exception as e:
            log.error(f'接口请求异常：\n{e}\n请求地址：\n{self.url}')
            raise
        finally:
            self.session_close()


    def get(self,**kwargs):
        with allure.step(f'发送 get 请求: {self.path}'):
            return self.which_method('GET',**kwargs)

    def post(self,**kwargs):
        with allure.step(f'发送 post 请求: {self.path}'):
            return self.which_method('POST',**kwargs)

    def delete(self,**kwargs):
        with allure.step(f'发送 delete 请求: {self.path}'):
            return self.which_method('DELETE',**kwargs)

    def put(self,**kwargs):
        with allure.step(f'发送 put 请求: {self.path}'):
            return self.which_method('PUT',**kwargs)

    def session_close(self):
        session.close()











