import requests
from bs4 import BeautifulSoup
from urllib.request import Request
#Counting the number of links extracted
counter = 0
fixed_links = 0
website_name = input("type a website: ")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

parent_links = []
sub_links = {}
# def get_text_data(website_name):
#     getUrl = read_link()
#     reqs = requests.get(website_name)
#     return reqs.text


#Reads the url
def read_link(website_name):
    website_name = website_name.replace(" ", "").lower()
    base_url = f"https://www.{website_name}.com.au/"
    print("Extracting: " + base_url)
    return base_url
#Extracts all links of the given website
def get_links():
    global counter, fixed_links
    #Getting the url
    getUrl = read_link(website_name)
    reqs = requests.get(getUrl, headers=headers)
    parent_soup = BeautifulSoup(reqs.content, 'html.parser')
    #finding all "a" tags in html
    get_parent_url = parent_soup.find_all('a', href=True)
    add_https = 'https://'
    #getting the parent URL's
    for extract in get_parent_url:
        parent_href = extract.get('href')
        if add_https in parent_href:
            print(parent_href)
            parent_links.append(parent_href)
            counter += 1
        #if link doesn't contain https://
        else:
            print("fixed-->", getUrl + parent_href)
            fixed_links += 1
            parent_links.append(parent_href)

        #accessing sub links now

        sub_reqs = requests.get(parent_href, headers=headers)
        sub_soup = BeautifulSoup(sub_reqs.content, 'html.parser')
        get_sub_url = sub_soup.find_all('a', href=True)
        sub_links[parent_href] = {}
        print('subs',sub_links)

        # for childLinks in get_sub_url:
        #     sub_href = childLinks.get('href')
        #     sub_links[parent_href].append(sub_href)
        #     print("\t"+sub_href)
        #     # print(sub_href)

def get_links_2():
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

        get_sub_url = parent_href
        sub_reqs = requests.get(parent_href, headers=headers)
        sub_soup = BeautifulSoup(sub_reqs.content, 'html.parser')


        for sub_extract in get_sub_url:
            sub_href = sub_extract.get('href')
            sub_links[parent_href].append(sub_href)
            print("\t"+sub_href)
            # print(sub_href)
       
# def get_sub_links():
#     global counter 
#     sub_link = get_links()
#     for child in sub_link:
#         reqs = requests.get(sub_link)
#         sub_soup = BeautifulSoup(reqs.content, "lxml")
#         get_child_url = sub_soup.find_all('a', href=True)
#         for extract in get_child_url:
#             print(extract.get('href'))
#     print(child)

read = read_link(website_name)
extract_links = get_links()
# extract_sub_links = get_sub_links()
print("Number of links extracted:",counter, "Number of links fixed:" , fixed_links)
print("number of links in parent:" , len(parent_links))
# get_txt = get_text_data()


