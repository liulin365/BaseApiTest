import pytest
from function import request_method
from function.connect_mysql import do_connect
from function.print_log import log
from function.read_file import control_file


@pytest.fixture(scope='session')
def get_universal_verify_code():
    verify_code = do_connect.do_select(control_file().read_yaml()['verify_code'])
    tag_code = verify_code[0]['code']
    code = control_file().update_yaml('user_info',tag_code,'code')
    return code



@pytest.fixture(scope='session')
def get_token(get_universal_verify_code):
    default_headers = control_file().read_yaml()['headers']
    path = control_file('登录').read_excel()[0][1]
    user_info = control_file().read_yaml()['user_info']
    request = request_method.Do_Requests(path)
    headers = request_method.session.headers.update(default_headers)
    response = request.post(data = user_info,headers = headers).json()
    value = response['token_type'] + ' ' + response['access_token']
    request_method.session.headers['authorization'] = value
    log.info(f'当前 Headers 中的 token 已更新:\n{request_method.session.headers['authorization']}')


if __name__ == '__main__':
    get_token()










