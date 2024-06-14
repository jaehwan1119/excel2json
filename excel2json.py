import re
import numpy as np
import pandas as pd
import os
import json

from data import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 불러온 json 파일 내에서 id에 대한 내용을 추출하기 위한 함수
def find_object_by_id(data, id):
    for item in data:
        if item['id'] == id:
            return item
    return None

# form의 id와 detail을 찾아내는 함수
def find_pattern(text:str, case:int) -> list:
    if case == 0:
        regex = r';;(.*) ::' # id
    else:
        regex = r':: (.*)' # detail

    # 검색 (type:list)
    matches = re.findall(regex, text)

    return matches

# form 내의 '<~:expression>'을 ~ 으로 교체하기 위한 함수
def replace_expression(text: str) -> str:
    regex = r'<(.*?):expression>'  # 정규식 패턴
    matches = re.findall(regex, text)
    result = text

    for match in matches:
        result = re.sub(regex, match, result, 1)  # 첫 번째 매치만 치환

    return result



# excel, json 파일 path
excel_path = '/Users/dataly/Desktop/E/result_excel.xlsx'
# excel_path = '/Users/gimjaehwan/Desktop/E/result_excel.xlsx'

# excel파일의 DataFrame
excel_df = pd.read_excel(excel_path, dtype=str)

# excel에서 데이터를 읽어올 때 빈 칸의 nan을 ''로 교체
excel_df = excel_df.replace(np.nan, '', regex=True)
new_excel_dict = excel_df.to_dict(orient='dict')

# json 형태로 출력
json_data = json.dumps(new_excel_dict, indent=4, ensure_ascii=False)
print(json_data)

dict_type = ['id', 'type', 'output', 'modify', 'diff_1', 'diff_2']
temp_form = []
temp_form_id = []
temp_dict = {
        'id': [],
        'type': [],
        'output': [],
        'modify': [],
        'diff_1': [],
        'diff_2': []
    }

immoral_expression = ImmoralExpression()
expression = Expression()
explicitness = Explicitness()

# excel dictionary 전체순회
for i in range(len(new_excel_dict['id'])):
    # excel dictionary의 요소를 임시 dictionary에 추가
    for dtype in dict_type:
        # form 추출
        if new_excel_dict[dtype][i] == 'form':
            # form에서 id와 detail 추출
            temp_form = find_pattern(new_excel_dict['output'][i], 1)
            temp_form_id = find_pattern(new_excel_dict['output'][i], 0)
        temp_dict[dtype].append(new_excel_dict[dtype][i])

    # 만약 현재 index의 new_excel_dict id가 저장중인 temp_dict의 id와 같지 않다면
    # -> 데이터를 json에 추가할 수 있도록 정제하고 class에 저장 후 temp_dict, temp_form 초기화
    if i == len(new_excel_dict['id']) - 1 or temp_dict['id'][0] != new_excel_dict['id'][i+1]:
        # 데이터 정제
        # form detail의 <~:expression> 제거
        for j in range(len(temp_form)):
            temp_form[j] = replace_expression(temp_form[j])

        # 데이터 저장
        expression_id = find_pattern(temp_dict['output'][1], 0) # <- 선택문장 id
        expression_form = replace_expression(find_pattern(temp_dict['output'][1], 1)[0]) # <- 선택문장 내용
        for explicitness_data in temp_dict['output'][2]:
            explicitness_form = temp_dict['output'][2][0] # 부정적 발언 list
            explicitness_type = 'True' if temp_dict['output'][3] == '명시' else 'False'
            explicitness_begin = expression_form.find(explicitness_form)
            explicitness_end = explicitness_begin + len(explicitness_form)

            explicitness.__init__(explicitness_type, explicitness_form, explicitness_begin, explicitness_end)
        expression_sentiment = temp_dict['output'][4]
        expression_intensity = temp_dict['output'][5]
        expression_domains = temp_dict['output'][6]






        print('[temp_dict]')
        print(temp_dict)
        print('[temp_form]')
        print(temp_form)
        print('[temp_form_id]')
        print(temp_form_id)
        print('=' * 50)

        # 초기화
        temp_form = []
        temp_form_id = []
        temp_dict = {
            'id': [],
            'type': [],
            'output': [],
            'modify': [],
            'diff_1': [],
            'diff_2': []
        }


# # 읽어온 excel 파일에서 id값 읽기 (현재는 맨 첫번째 아이디: ERRW1908000023.267)
# excel_id = excel_df['id'][0]
# excel_form = excel_df['output'][0]
#
# # excel의 id에 대한 json 파일명(ERRW1908000023.json) 생성
# json_file_path = '/Users/dataly/Desktop/ABU/' + excel_id.split('.')[0] + '.json'
# # json_file_path = '/Users/gimjaehwan/Desktop/ABU/' + excel_id.split('.')[0] + '.json'
#
# # excel의 id에 대한 json 파일 불러오기
# f = open(json_file_path)
# data = json.load(f)
# json_df = pd.json_normalize(data, record_path=['document'])




# print(json_df)
# print(excel_form)

# 불러온 json DataFrame에서 excel의 id에 해당하는 부분 추출


