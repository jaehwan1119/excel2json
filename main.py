import time
from excel2json import *

start_time = time.time()

# excel 파일 path
excel_path = '/Users/dataly/Desktop/E/result_excel.xlsx'
json_path = '/Users/dataly/Desktop/ABU/'
save_path = '/Users/Dataly/Desktop/ABU/result.json'

excel2json(excel_path, json_path, save_path)

end_time = time.time()
print(end_time - start_time)