import requests
from bs4 import BeautifulSoup
from urllib.request import Request
#Counting the number of links extracted
counter = 0
website_name = input("type a website: ")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

parent_links = []
sub_links = {}

def get_text_data(website_name):
    getUrl = read_link(website_name)
    reqs = requests.get(website_name)
    return reqs.text

#Reads the url
def read_link(website_name):
    website_name = website_name.replace(" ", "").lower()
    url = f"https://www.{website_name}.com.au/s?k=shoes"
    return url

#Extracts all links of the given website
def get_links():
    global counter
    #Getting the url
    getUrl = read_link(website_name)
    reqs = requests.get(getUrl, headers=headers)
    parent_soup = BeautifulSoup(reqs.content, 'html.parser')
    #finding all "a" tags in html
    get_parent_url = parent_soup.find_all('a', href=True)
    for extract in get_parent_url:
        parent_href = extract.get('href')
        print(parent_href)
        parent_links.append(parent_href)
        counter += 1
        #accessing sub links now

        sub_reqs = requests.get(parent_href)
        sub_soup = BeautifulSoup(sub_reqs.content, 'html.parser')
        get_sub_url = sub_soup.find_all('a', href=True)
        sub_links[parent_href] = []

        for sub_extract in get_sub_url:
            sub_href = sub_extract.get('href')
            if sub_href is not None:
                sub_links[parent_href].append(sub_href)
                print("\t"+sub_href)
            else:
                sub_links[parent_href].append('N/A')
            # print(sub_href)

def get_sub_links():
    global counter
    sub_link = get_links()
    if sub_link is not None:
        for child in sub_link:
            reqs = requests.get(sub_link)
            sub_soup = BeautifulSoup(reqs.content, "lxml")
            get_child_url = sub_soup.find_all('a', href=True)
            for extract in get_child_url:
                print(extract.get('href'))
                print(child)
            
read = read_link(website_name)
extract_links = get_links()
# extract_links_2 = get_links_2()
extract_sub_links = get_sub_links()
print("Number of links extracted ",counter)
# get_txt = get_text_data(website_name)
            
            
            
