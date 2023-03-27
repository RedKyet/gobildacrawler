import requests
import re
import os
import glob
import shutil
import zipfile
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from os.path import exists
 
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
    #url = 'https://www.gobilda.com/sitemap/categories/'
    url = 'https://www.gobilda.com/2106-series-stainless-steel-rex-shaft-8mm-diameter-40mm-length/'
    domain = get_domain(url)
    if not os.path.isdir("steps"):
        os.mkdir("steps")
    queue = [url]
    visited = set()
 
    while queue:
        url = queue.pop(0)
        visited.add(url)
        print(url)
        page = BeautifulSoup(requests.get(url).content, "html.parser")
        stepf = page.find('a', href=re.compile('/content/step_files/'))
        
        if stepf:
            subcats = page.find_all('a', {"class": "breadcrumb-label"})
            category = ""
            for cat in subcats:
                cat.contents[0] = ''.join(e for e in cat.contents[0] if e.isalnum() or e in"() -,.&")
                if cat.contents[0][-1]== " ": cat.contents[0] = cat.contents[0][0:-1]
                category = category + "/" + cat.contents[0]
            print(category[1:])
            if not os.path.isdir("steps/"+category):
                os.makedirs("steps/"+category)
            part_name = page.find('h1',{"class": "productView-title"}).contents[0]
            part_name = ''.join(e for e in part_name if e.isalnum() or e in"() -,.")
            if not exists("steps/"+category+"/"+"{}.step".format(part_name)):
                if not os.path.isdir("unzipped_tmp"):
                    os.mkdir("unzipped_tmp")
                #part_name = url.split("/")[-1]
                stepf_link = "https://www.gobilda.com{}".format(stepf['href'])
                print(stepf_link)
                with open("tmp.zip",'wb') as f:
                    f.write(requests.get(stepf_link).content)
                    f.flush
                with zipfile.ZipFile('tmp.zip', 'r') as zip:
                    zip.extractall(path="unzipped_tmp/")
                    #files_in_zip = zip.namelist()
                files_in_zip = glob.iglob("unzipped_tmp/**/*.*", recursive=True)
                for file in files_in_zip:
                    #file="unzipped_tmp/"+file
                    filen = file.split("\\")[-1]
                    if filen.split('.')[-1] == "step" or filen.split('.')[-1] == "STEP":
                        term = filen.split(" ")
                        end=""
                        for i in range (1,(len(term))):
                            end = end+term[i]
                        end = end.split('.')[0]
                        name = "{}{}.step".format(part_name,end)
                        if not exists(path="steps/"+category+"/"+name):
                            os.rename(file,"steps/"+category+"/"+name)
                shutil.rmtree("unzipped_tmp")
            else: print("file already exists")
        links = get_links(url)
        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)