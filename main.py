import requests
import re
import os
import zipfile
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from os.path import exists

"""with open("tmp.zip",'wb') as f:
    f.write(requests.get("https://www.gobilda.com/content/step_files/2000-0025-0002.zip").content)

with zipfile.ZipFile('tmp.zip', 'r') as zip_ref:
    zip_ref.extractall()

with open("content.txt",'wb') as f:
    f.write(requests.get("https://www.gobilda.com/sitemap/categories/").content)"""

#search for pages containing st links, save url name and download stl

 
def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain
 
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = set()
    for link in soup.find_all('a'):
        link_url = link.get('href')
        if link_url and not str(link_url).endswith('.zip') and str(link_url).count("/")>3:
            absolute_link = urljoin(url, link_url)
            if absolute_link.startswith(domain):
                links.add(absolute_link)
    return links
 
if __name__ == '__main__':
    url = 'https://www.gobilda.com/sitemap/categories/'
    domain = get_domain(url)
    if not os.path.isdir("unzipped_tmp"):
        os.mkdir("unzipped_tmp")
    queue = [url]
    visited = set()
 
    while queue:
        url = queue.pop(0)
        visited.add(url)
        print(url)
        page = BeautifulSoup(requests.get(url).content, "html.parser")
        stepf = page.find('a', href=re.compile('/content/step_files/'))
        
        if stepf:
            
            part_name = page.find('h1',{"class": "productView-title"}).contents[0]
            part_name = ''.join(e for e in part_name if e.isalnum() or e in"() -,.")
            if not exists("{}.step".format(part_name)):
                #part_name = url.split("/")[-1]
                stepf_link = "https://www.gobilda.com{}".format(stepf['href'])
                print(stepf_link)
                with open("tmp.zip",'wb') as f:
                    f.write(requests.get(stepf_link).content)
                with zipfile.ZipFile('tmp.zip', 'r') as zip:
                    zip.extractall()
                    files_in_zip = zip.namelist()
                for file in files_in_zip:
                    if file.split('.')[-1] == "step" or file.split('.')[-1] == "STEP":
                        term = file.split(" ")
                        end=""
                        for i in range (1,(len(term))):
                            end = end+term[i]
                        end = end.split('.')[0]
                        name = "{}{}.step".format(part_name,end)
                        if exists(name):
                            os.remove(file)
                        else:
                            os.rename(file,name)
                    elif file.split('.')[-1] in ("zip","py","git","gitignore"):
                        pass
                    else:
                        os.remove(file)
            else: print("file already exists")
        links = get_links(url)
        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)