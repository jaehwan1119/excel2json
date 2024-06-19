import os
import re
import numpy as np
import pandas as pd
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

    # out of index 방지
    if not matches:
        return [text]

    return matches

# form 내의 '<~:expression>'을 '~' 으로 교체하기 위한 함수
def replace_expression(text: str) -> str:
    regex = r'<(.*?):expression>'  # 정규식 패턴
    matches = re.findall(regex, text)
    result = text

    # 치환
    for match in matches:
        result = re.sub(regex, match, result, 1)

    return result

def find_keys(dictionary, value):
    return [key for key, val in dictionary.items() if val == value]

# Excel파일 작성
def write_excel(df: pd.DataFrame, filename: str, save_path: str) -> None:
    # 파일명 끝에 확장자 없을 경우
    if not filename.endswith('.xlsx'):
        filename += '.xlsx'

    # 저장 경로가 존재하지 않으면 생성
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 전체 파일 경로
    file_path = os.path.join(save_path, filename)

    # 파일이 이미 존재한다면 기존 파일에 이어서 저장
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_excel(file_path, index=False, engine='openpyxl')
    else:
        # 파일이 존재하지 않으면 새 파일 생성
        df.to_excel(file_path, index=False, engine='openpyxl')

def excel2json(excel_path:str, json_path:str, save_path:str) -> None:
    # excel파일의 DataFrame
    excel_df = pd.read_excel(excel_path, dtype=str)

    # excel에서 데이터를 읽어올 때 빈 칸의 nan을 ''로 교체
    excel_df = excel_df.replace(np.nan, '', regex=True)
    new_excel_dict = excel_df.to_dict(orient='dict')

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

    # excel과 json에서 가져온 데이터를 계층적으로 쌓기 위한 class
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

            # temp_dict은 excel의 데이터를 id 단위로 저장하는 변수
            temp_dict[dtype].append(new_excel_dict[dtype][i])

        i += 1
        # id 단위로 끊어서 temp_dict을 내보냄
        # (while문으로 excel 전체를 순회하다가 temp_dict에 저장된 아이디와 현재 순회중인 excel의 id가 다른 경우 데이터를 추가함)
        if i >= len(new_excel_dict['id']) or temp_dict['id'][0] != new_excel_dict['id'][i]:
            asterisk_flag = False
            # 데이터를 json에 추가할 수 있도록 정제하고 class에 저장 후 temp_dict, temp_form 초기화
            k = 1
            length = len(temp_dict['output'])
            while k < length:
                expression_id = find_pattern(temp_dict['output'][k], 0)[0]  # 선택문장 id
                expression_form = replace_expression(find_pattern(temp_dict['output'][k], 1)[0])  # 선택문장 내용

                # 선택문장이 없는 경우
                if expression_id == '' and expression_form == '':
                    no_exp_form = {key: value[0] for key, value in temp_dict.items()}
                    no_expression_docu = pd.DataFrame([no_exp_form])
                    write_excel(no_expression_docu, "no_expression", json_path)

                k += 1

                explicitness_list = [] # 생성된 explicitness class를 저장할 list
                exp_form_list = temp_dict['output'][k].split(', ') # explicitness의 form 요소 list

                # explicitness 생성
                k += 1
                for explicitness_data in exp_form_list:
                    explicitness_form = explicitness_data  # explicitness form
                    explicitness_type = 'TRUE' if temp_dict['output'][k] == '명시' else 'FALSE' # explicitness type
                    explicitness_begin = expression_form.find(explicitness_form) # explicitness begin
                    explicitness_end = explicitness_begin + len(explicitness_form) # explicitness end

                    # 명시성이 '명시'인 경우 <~:expression> 내용 삽입, '비명시'인 경우엔 선택문장 삽입
                    if explicitness_type == 'TRUE':
                        explicitness.__init__(explicitness_type, explicitness_form, explicitness_begin, explicitness_end)  # explicitness class 생성
                        explicitness_list.append(explicitness.to_dict())
                    else:
                        explicitness.__init__(explicitness_type, expression_form, explicitness_begin, len(expression_form))  # explicitness class 생성
                        explicitness_list.append(explicitness.to_dict())


                # expression 생성
                k += 1
                expression_sentiment = temp_dict['output'][k]  # 긍/부정 (expression sentiment)
                k += 1
                expression_intensity = temp_dict['output'][k]  # 강도 (expression intensity)

                # intensity가 *인 경우 따로 excel 파일 작성
                if expression_intensity == "*":
                    if asterisk_flag == False:
                        asterisk_docu = pd.DataFrame(temp_dict)
                        write_excel(asterisk_docu, "intensity_is_asterisk", json_path)
                        asterisk_flag = True
                    expression_intensity = -1
                else:
                    if expression_intensity:
                        expression_intensity = int(expression_intensity)
                    else:
                        expression_intensity = 0
                k += 1
                expression_domains = temp_dict['output'][k]  # 영역 (expression domain)
                k += 1

                expression.__init__(explicitness_list, expression_sentiment, expression_domains, expression_intensity) # expression class 생성
                immoral_expression.__init__(expression_id, expression_form, expression.to_dict())
                docu_data.immoral_expression.append(immoral_expression.to_dict()) # 문서 전체 데이터를 저장할 class에 데이터 쌓기

            # json 데이터 불러오기
            json_id = temp_dict['id'][0]
            json_file_path = json_path + json_id.split('.')[0] + '.json'

            # excel의 id에 대한 json 파일 불러오기
            f = open(json_file_path)
            data = json.load(f)
            search_result = find_object_by_id(data['document'], json_id)

            docu_data.id = search_result['id']
            docu_data.metadata = search_result['metadata']
            docu_data.paragraph = search_result['paragraph']

            # json_data = json.dumps(docu_data.to_dict(), indent=4, ensure_ascii=False)
            # print(json_data)

            temp_document_data['document'].append(docu_data.to_dict())

            # 초기화
            docu_data.__init__()
            sentence.__init__('','','')
            immoral_expression.__init__('','', {})
            expression.__init__([],'', '', 0)
            explicitness.__init__('','', 0, 0)
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
    json_data = json.dumps(temp_document_data, indent=4, ensure_ascii=False)
    # print(json_data)

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(json_data)
