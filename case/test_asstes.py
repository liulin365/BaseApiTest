from function.request_method import Do_Requests
from function.read_file import control_file
from function.assert_respons import assert_response
import allure



con_file = control_file(sheet_name='不动产')
case_data = con_file.read_excel()


@allure.story('测试不动产业务线(story)')
@allure.feature('回归测试(feature)')
class Test_sys:

    @allure.title('测试新增资产')
    def test_add_asstes(self, get_token):
        method = case_data[0][1]
        path = case_data[0][2]
        param_type = case_data[0][3]
        request_data = con_file.str_to_dict(case_data[0][4])
        do = Do_Requests(path)
        request_func = getattr(do, method.lower()) # do.post
        kwargs = {param_type: request_data}
        response = request_func(**kwargs).json()
        assert_response(response,con_file.str_to_dict(case_data[0][5]))
