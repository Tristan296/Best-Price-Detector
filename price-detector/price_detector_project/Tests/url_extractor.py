import requests
from bs4 import BeautifulSoup

url = 'https://www.rebelsport.com.au/'
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'lxml')

urls = []
for link in soup.find_all('a'):
    print(link.get('href'))