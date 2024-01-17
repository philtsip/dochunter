# Usage: python localhunter.py name_of_output.json
import sys
import os
import json
from datetime import datetime

root_dir = '.'

output_file = "output.json"

if len(sys.argv) > 1:
    output_file = sys.argv[1] #output file name

files_data = []
text_file_extensions = ['.txt', '.md']

for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        timestamp = os.path.getmtime(file_path)
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        
        extension = os.path.splitext(filename)[1]
        if extension in text_file_extensions:
            try:
                with open(file_path, 'r') as f:
                    contents = f.read()

                file_data = {
                    'url': file_path,
                    'date': date,
                    'contents': contents
                }
                files_data.append(file_data)

            except:
                continue

with open(output_file, 'w') as f:
    json.dump(files_data, f, ensure_ascii=False)
