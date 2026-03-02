from function.request_method import Do_Requests
from function.read_file import control_file
from function.assert_respons import assert_response
import allure
import pytest


con_file = control_file(sheet_name='用例')
case_data = con_file.read_excel()


@allure.story('测试系统配置(story)')
@allure.feature('测试系统配置(feature)')
class Test_sys:

    @allure.title('测试添加敏感词配置的用例')
    def test_add_sysconf(self,get_token):
        path = case_data[1][1]
        request_data = con_file.str_to_dict(case_data[1][3])
        response = Do_Requests(path).post(json = request_data).json()
        assert_response(response,'添加敏感词配置')

    @allure.title('测试添加小屏看板的用例')
    @pytest.mark.dependency(name = 'test_add_sysconf')
    def test_xiaoping(self):
        path = case_data[0][1]
        request_data = con_file.str_to_dict(case_data[0][3])
        response = Do_Requests(path).post(json = request_data).json()
        assert_response(response,'添加小屏看板')

