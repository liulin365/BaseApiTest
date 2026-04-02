from function.request_method import Do_Requests
from function.read_file import control_file
from function.assert_respons import assert_response
import allure
import pytest
import requests


con_file = control_file(sheet_name='用例')
case_data = con_file.read_excel()


@allure.story('测试系统配置(story)')
@allure.feature('测试系统配置(feature)')
class Test_sys:

    @allure.title('测试添加敏感词配置的用例')
    @pytest.mark.flaky(reruns=5, reruns_delay=1, only_rerun=[requests.Timeout, requests.ConnectionError])
    # - reruns: 失败后的重试次数
    # - reruns_delay: 每次重试之间的延迟（秒）
    # - only_rerun参数：仅在指定异常发生时重试,其他异常直接失败不重试
    @pytest.mark.order(1)
    def test_add_sysconf(self,get_token):
        path = case_data[1][1]
        request_data = con_file.str_to_dict(case_data[1][3])
        response = Do_Requests(path).post(json = request_data).json()
        assert_response(response,'添加敏感词配置')

    @allure.title('测试添加小屏看板的用例')
    @pytest.mark.dependency(name = 'test_add_sysconf')
    @pytest.mark.order(2)
    def test_xiaoping(self):
        path = case_data[0][1]
        request_data = con_file.str_to_dict(case_data[0][3])
        response = Do_Requests(path).post(json = request_data).json()
        assert_response(response,'添加小屏看板')

