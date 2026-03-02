# 该模块主要用于从Excel文件读取测试用例

from os import path
from openpyxl import load_workbook
import yaml
import json


file_path = path.abspath(__file__)
target_case = path.dirname(path.dirname(file_path)) + '/file/测试用例.xlsx'
target_setting = path.dirname(path.dirname(file_path)) + '/file/default_setting.yaml'


class control_file:
    def __init__(self,sheet_name = None):
        self.sheet_name = sheet_name
        self.wb = load_workbook(target_case) # 载入文件
        self.ws = None

    def check_input(self):
        list_name = []
        if self.sheet_name == 'all' or self.sheet_name is None:
            for name in self.wb.sheetnames:
                list_name.append(name)
            return list_name
        else:
            list_name.append(self.sheet_name)
            return list_name

    def read_excel(self):
        sheet_name = self.check_input()
        data = []
        for name in sheet_name:
            self.ws = self.wb[name]
            for i in self.ws.iter_rows(min_row=2, values_only=True):
                data.append(i)
        self.wb.close()
        return data

    def read_yaml(self):
        with open(target_setting,mode='r',encoding='UTF-8') as f:
            data = yaml.safe_load(f)
        return data

    def str_to_dict(self,data): # 从Excel中读取出来的json有字符串引号，属于字符串类型
        json_str = data.strip("'")
        dict_data = json.loads(json_str)
        return dict_data



con_file = control_file()

if __name__ == '__main__':
    con_file = control_file()
    con_file.str_to_dict()









