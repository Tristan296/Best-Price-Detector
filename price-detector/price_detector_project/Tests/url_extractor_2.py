import requests
from bs4 import BeautifulSoup
counter = 0
getUrl = requests.get("https://www.thewhiskeyexchange.com/")
parent_soup = BeautifulSoup(getUrl.content, 'html.parser')
parent_a_tag = parent_soup.find_all("a", href=True)
parent_links = []
sub_links = {}
for link in parent_a_tag:
    parent_href = link.get('href')
    print(parent_href)
    parent_links.append(parent_href)
    
    #accessing parents child --> sub links

    sub_request = requests.get(parent_href)
    sub_soup = BeautifulSoup(sub_request.content, 'html.parser')
    sub_atags = sub_soup.find_all("a", href=True)
    sub_links[parent_href] = []
    counter += 1
    for sub_atag in sub_atags:
        sub_href = sub_atag.get('href')
        sub_links[parent_href].append(sub_href)
        print("\t"+sub_href)

print("Links extracted: " + counter)