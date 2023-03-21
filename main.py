import requests
import zipfile

with open("tmp.zip",'wb') as f:
    f.write(requests.get("https://www.gobilda.com/content/step_files/2000-0025-0002.zip").content)

with zipfile.ZipFile('tmp.zip', 'r') as zip_ref:
    zip_ref.extractall()