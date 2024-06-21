import json
import time
from excel2json import excel2json
from checkJson import validationCheck

start_time = time.time()

# excel 파일 path
excel_path = '/Users/dataly/Desktop/E/result_excel.xlsx'
json_path = '/Users/dataly/Desktop/ABU/'
save_path = '/Users/Dataly/Desktop/ABU/result.json'

result_data = excel2json(excel_path, json_path)

json_data = json.dumps(result_data, indent=4, ensure_ascii=False)
# print(json_data)

with open(save_path, 'w', encoding='utf-8') as f:
    f.write(json_data)

with open(save_path, "r") as f:
    check_target = json.load(f)

validationCheck(result_data['document'], check_target['document'])

end_time = time.time()
print(end_time - start_time)