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

def find_keys(dictionary, value):
    return [key for key, val in dictionary.items() if val == value]

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
# print(json_data)

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

docu_data = Data()
sentence = Sentence()
immoral_expression = ImmoralExpression()
expression = Expression()
explicitness = Explicitness()

# sentence를 저장할 결과 list
i=0
# excel dictionary 전체순회
while i != len(new_excel_dict['id']):
    # excel dictionary의 요소를 임시 dictionary에 추가
    for dtype in dict_type:
        # form 추출
        if new_excel_dict[dtype][i] == 'form':
            # form의 내용 (sentence에 추가할 데이터)
            temp_form = find_pattern(new_excel_dict['output'][i], 1)

            # form의 내용에서 <~:expression> 제거
            for j in range(len(temp_form)):
                temp_form[j] = replace_expression(temp_form[j])

            # form의 id (sentence에 추가할 데이터)
            temp_form_id = find_pattern(new_excel_dict['output'][i], 0)

            # sentence의 id, form, form_origin 저장
            for id, form in zip(temp_form_id, temp_form):
                sentence.__init__(id, form, form)
                docu_data.sentence.append(sentence.to_dict())

        temp_dict[dtype].append(new_excel_dict[dtype][i])
    i += 1
    # id 단위로 끊어서 temp_dict을 내보냄
    if temp_dict['id'][0] != new_excel_dict['id'][i]:
        # 데이터를 json에 추가할 수 있도록 정제하고 class에 저장 후 temp_dict, temp_form 초기화
        k = 1
        length = len(temp_dict['output'])
        while k < length:

            expression_id = find_pattern(temp_dict['output'][k], 0)[0]  # 선택문장 id
            expression_form = replace_expression(find_pattern(temp_dict['output'][k], 1)[0])  # 선택문장 내용
            k += 1
            # 여기서부터
            explicitness_list = []
            exp_form_list = temp_dict['output'][k].split(', ')
            k += 1
            for explicitness_data in exp_form_list:
                explicitness_form = explicitness_data  # 부정적 발언 list
                explicitness_type = 'True' if temp_dict['output'][k] == '명시' else 'False'
                explicitness_begin = expression_form.find(explicitness_form)
                explicitness_end = explicitness_begin + len(explicitness_form)

                explicitness.__init__(explicitness_type, explicitness_form, explicitness_begin, explicitness_end)
                explicitness_list.append(explicitness.to_dict())
            # 여기까지 explicitness 생성

            # 여기서부터
            k += 1
            expression_sentiment = temp_dict['output'][k]  # 긍/부정 여부
            k += 1
            expression_intensity = temp_dict['output'][k]  # 강도
            k += 1
            expression_domains = temp_dict['output'][k]  # 영역
            k += 1

            expression.__init__(explicitness_list, expression_sentiment, expression_domains, expression_intensity)
            immoral_expression.__init__(expression_id, expression_form, expression.to_dict())
            docu_data.immoral_expression.append(immoral_expression.to_dict())
            # 여기까지 expression 생성

        # json 데이터 불러오기
        json_id = temp_dict['id'][0]
        json_file_path = '/Users/dataly/Desktop/ABU/' + json_id.split('.')[0] + '.json'

        # # excel의 id에 대한 json 파일 불러오기
        f = open(json_file_path)
        data = json.load(f)
        search_result = find_object_by_id(data['document'], json_id)

        docu_data.id = search_result['id']
        docu_data.metadata = search_result['metadata']
        docu_data.paragraph = search_result['paragraph']

        json_data = json.dumps(docu_data.to_dict(), indent=4, ensure_ascii=False)
        print(json_data)

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

# # 데이터를 json에 추가할 수 있도록 정제하고 class에 저장 후 temp_dict, temp_form 초기화
# k=1
# length = len(temp_dict['output'])
# while k < length:
#
#     expression_id = find_pattern(temp_dict['output'][k], 0)[0]  # 선택문장 id
#     expression_form = replace_expression(find_pattern(temp_dict['output'][k], 1)[0])  # 선택문장 내용
#     k+=1
#     # 여기서부터
#     explicitness_list = []
#     exp_form_list = temp_dict['output'][k].split(', ')
#     k+=1
#     for explicitness_data in exp_form_list:
#         explicitness_form = explicitness_data # 부정적 발언 list
#         explicitness_type = 'True' if temp_dict['output'][k] == '명시' else 'False'
#         explicitness_begin = expression_form.find(explicitness_form)
#         explicitness_end = explicitness_begin + len(explicitness_form)
#
#         explicitness.__init__(explicitness_type, explicitness_form, explicitness_begin, explicitness_end)
#         explicitness_list.append(explicitness.to_dict())
#     # 여기까지 explicitness 생성
#
#     # 여기서부터
#     k+=1
#     expression_sentiment = temp_dict['output'][k] # 긍/부정 여부
#     k+=1
#     expression_intensity = temp_dict['output'][k] # 강도
#     k+=1
#     expression_domains = temp_dict['output'][k] # 영역
#     k+=1
#
#     expression.__init__(explicitness_list, expression_sentiment, expression_domains, expression_intensity)
#     immoral_expression.__init__(expression_id, expression_form, expression.to_dict())
#     docu_data.immoral_expression.append(immoral_expression.to_dict())
#     #여기까지 expression 생성
#
#
# # json 데이터 불러오기
# json_id = temp_dict['id'][0]
# json_file_path = '/Users/dataly/Desktop/ABU/' + json_id.split('.')[0] + '.json'
#
# # # excel의 id에 대한 json 파일 불러오기
# f = open(json_file_path)
# data = json.load(f)
# search_result = find_object_by_id(data['document'], json_id)
#
# docu_data.id = search_result['id']
# docu_data.metadata = search_result['metadata']
# docu_data.paragraph = search_result['paragraph']
#
# json_data = json.dumps(docu_data.to_dict(), indent=4, ensure_ascii=False)
# print(json_data)
#
#
# # 초기화
# temp_form = []
# temp_form_id = []
# temp_dict = {
#     'id': [],
#     'type': [],
#     'output': [],
#     'modify': [],
#     'diff_1': [],
#     'diff_2': []
# }


