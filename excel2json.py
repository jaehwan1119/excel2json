import re

import pandas as pd
from glob import glob
import os
import json

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# document 정보(임의로 설정)
document_id = "EXAU2302308290"
document_metadata = {
    "title": "국립국어원 웹 말뭉치 추출 EXAU2302308290",
    "creator": "국립국어원",
    "distributor": "국립국어원",
    "year": "2023",
    "category": "웹 > 리뷰 > 누리소통망",
    "annotation_level": "부적절 발언 탐지",
    "sampling": "본문 전체 / 부분 추출 - 임의 추출 / 부분 추출 - 특정 부분 추출"
}



# excel 데이터를 쌓을 document 리스트
document = []

# excel, json 파일 path
excel_path = '/Users/dataly/Desktop/E/result_excel.xlsx'

# excel 파일 읽어오기
df = pd.read_excel(excel_path, engine='openpyxl')

# 읽어온 excel 파일에서 id값 읽기
excel_id = df['id'][0]
excel_form = df['output'][0]

# excel의 id로부터 파일명을 추출
json_file_path = '/Users/dataly/Desktop/ABU/' + excel_id.split('.')[0] + '.json'

# json 파일 열기
f = open(json_file_path)
data = json.load(f)
json_df = pd.json_normalize(data, record_path=['document'])

print(json_df)
# print(excel_form)

# 불러온 json DataFrame에서 excel의 id에 해당하는 부분 추출


# print(df)