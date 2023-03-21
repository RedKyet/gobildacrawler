import requests
with open("tmp.zip",'wb') as f:
    f.write(requests.get("https://www.gobilda.com/content/step_files/2000-0025-0002.zip").content)