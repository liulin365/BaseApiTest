import pytest
from function import request_method
from function.print_log import log
from function.read_file import control_file


@pytest.fixture(scope='session')
def get_token():
    default_headers = control_file().read_yaml()['headers']
    path = control_file('登录').read_excel()[0][1]
    user_info = control_file().read_yaml()['user_info']
    request = request_method.Do_Requests(path)
    headers = request_method.session.headers.update(default_headers)
    response = request.post(data = user_info,headers = headers).json()
    value = response['token_type'] + ' ' + response['access_token']
    request_method.session.headers['authorization'] = value
    log.info(f'当前headers中的token已更新:\n{request_method.session.headers['authorization']}')


if __name__ == '__main__':
    get_token()










