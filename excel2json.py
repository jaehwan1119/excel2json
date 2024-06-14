import re
import numpy as np
import pandas as pd
from glob import glob
import os
import json

from data import *

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# excel, json 파일 path
# excel_path = '/Users/dataly/Desktop/E/result_excel.xlsx'
excel_path = '/Users/gimjaehwan/Desktop/E/result_excel.xlsx'

# excel파일의 DataFrame
excel_df = pd.read_excel(excel_path, dtype=str)

# excel에서 데이터를 읽어올 때 빈 칸의 nan을 ''로 교체
excel_df = excel_df.replace(np.nan, '', regex=True)
new_excel_dict = excel_df.to_dict(orient='dict')

# json 형태로 출력
json_data = json.dumps(new_excel_dict, indent=4, ensure_ascii=False)
print(json_data)

# excel 파일 읽어오기
df = pd.read_excel(excel_path, engine='openpyxl')

# 읽어온 excel 파일에서 id값 읽기
excel_id = df['id'][0]
excel_form = df['output'][0]

# excel의 id로부터 파일명을 추출
# json_file_path = '/Users/dataly/Desktop/ABU/' + excel_id.split('.')[0] + '.json'
json_file_path = '/Users/gimjaehwan/Desktop/ABU/' + excel_id.split('.')[0] + '.json'

# json 파일 열기
f = open(json_file_path)
data = json.load(f)
json_df = pd.json_normalize(data, record_path=['document'])

data1 = Data()

# print(json_df)
# print(excel_form)

# 불러온 json DataFrame에서 excel의 id에 해당하는 부분 추출



# for file in txt_file: