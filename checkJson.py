import json
import os
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def checkIntegrity(new_txt_dict: dict, new_excel_dict: dict) -> None:
    global idx
    for i in range(len(new_txt_dict['id'])):
        for type in dict_type:
            # 만약 txt와 excel의 내용이 맞지 안는 경우 위치와 내용 표시
            if new_txt_dict[type][i] != new_excel_dict[type][idx]:
                print('='*50)
                print(f"[Error Loaction: {new_txt_dict['id'][0]}")
                print('[Error Detail: txtFile]')
                print(new_txt_dict[type][i])
                print('[Error Detail: excelFile]')
                print(new_excel_dict[type][idx])
                print('=' * 50)
                print()
        idx += 1
    return None

dict_type = ['id', 'type', 'output', 'modify', 'diff_1', 'diff_2']

# excel과 json 파일의 무결성 검사
# json path
json_path = '/Users/Dataly/Desktop/ABU/result.json'
# excel path
excel_path = '/Users/Dataly/Desktop/E/result_excel.xlsx'

# new_excel 순회를 위한 전역변수
idx=0

# excel파일의 DataFrame
excel_df = pd.read_excel(excel_path, dtype=str)

# print(excel_df)

# excel에서 데이터를 읽어올 때 빈 칸의 nan을 ''로 교체
# excel_df = excel_df.replace('*', -1, regex=True)
# new_excel_dict = excel_df.to_dict(orient='dict')
#
# print(new_excel_dict)

f = open(json_path)
data = json.load(f)
json_df = pd.DataFrame(data)
print(json_df)
