import requests
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

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
        if link_url:
            absolute_link = urljoin(url, link_url)
            if absolute_link.startswith(domain):
                links.add(absolute_link)
    return links
 
if __name__ == '__main__':
    url = 'https://gobilda.com'
    domain = get_domain(url)
    queue = [url]
    visited = set()
 
    while queue:
        url = queue.pop(0)
        visited.add(url)
        print(url)
        page = BeautifulSoup(requests.get(url).content, "html.parser")
        stepf = page.find('a', href=re.compile('/content/step_files/'))
        if stepf:
            print("https://www.gobilda.com{}".format(stepf['href']))
        
        
        links = get_links(url)
        for link in links:
            if link not in visited and link not in queue:
                queue.append(link)