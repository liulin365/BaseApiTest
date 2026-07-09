from function.read_file import control_file

con_file = control_file('不动产')

con_file.update_excel(3,5,json_key='housingType',json_value='8')

con_file.read_excel()

