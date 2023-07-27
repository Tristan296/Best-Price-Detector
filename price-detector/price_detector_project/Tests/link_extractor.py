#WORKING FILE - USE THIS FOR UPDATES!!!!!!
"""
    DO NOT DELETE THIS FILE. THIS FILE IS USED TO TEST DIFFERENT FUNCTIONALITIES OF
    LINK EXTRACTTION!

    CODE THAT PASSES THROUGH WILL BE IMPLEMENTED TO THE HERE FROM URL_EXTRACTOR_2

    THIS WILL BE THE FINAL PRODUCT OF THIS PROJECT.
    USE THIS FILE AS THE CORE PROGRAM OF THIS PROJECT!!
"""

import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from urllib.request import Request
#Counting the number of links extracted
counter = 0
fixed_links = 0
website_name = input("type a website: ")
product = input("Enter in product: ")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

parent_links = []
sub_links = {}
# def get_text_data(website_name):
#     getUrl = read_link()
#     reqs = requests.get(website_name)
#     return reqs.text


"""
    YOU CAN DELETE THE WEBSITE NAME AND PRODUCT NAME AS YOUR CODE ALREADY HAS IT. CONNECT YOUR USER INPUT 
    FOR THE WEBSITE AND PRODUCT NAME INTO MY "READ_LINK(PRODUCT, WEBSITE_NAME) FUNCTION!!
"""

#Reads the url
def read_link(product, website_name):
    website_name = website_name.replace(" ", "").lower()
    base_url = f"https://www.{website_name}.com.au/"
    product = product.replace(" ", "-")
    print("Extracting: " + base_url)
    return base_url

"""
    GET LINKS AND SUB LINKS WORK WELL. I WILL CREATE ANOTHER FUNCTION LIKE "ADD_HTTPS_REBEL" TO WORK WITH 
    OTHER WEBSITES OR YOU CAN USE YOUR CODE TO LET THE SOFTWARE PASS THORUGH EXCEPTIONS WERE THE CODE HAS
    MISSING SCHEME APPLIED DID YOU MEAN "//HTTPS: ..... ERROR
"""
def get_links():
    global counter, fixed_links
    # Getting the url
    getUrl = read_link(product, website_name)
    reqs = requests.get(getUrl, headers=headers)
    parent_soup = BeautifulSoup(reqs.content, 'lxml')
    # finding all "a" tags in html
    get_parent_url = set(parent_soup.find_all('a', href=True))
    add_https_rebel = 'https://www.rebelsport.com.au/'
    add_https_aje = 'https://'
    # getting the parent URL's
    for link in get_parent_url:
        parent_href = link.get('href')
        # Checking for duplicates again as set() doesn't remove all duplicates so we would need to search our "parent_links"
        # array and compare it if the next link is doesn't exist in our current array     
        if parent_href not in parent_links and add_https_rebel in parent_href and re.search(r"^(http|https)://www.", parent_href):
            parent_links.append(parent_href)
            print(parent_href)
            counter += 1
        # else:
        #     print("fixed-->", urljoin(getUrl, parent_href))
        #     fixed_links += 1
        #     parent_links.append(parent_href)

        # accessing sub links now
        # passing through exceptions
        sub_request = requests.get(parent_href)
        sub_soup = BeautifulSoup(sub_request.content, 'html.parser')
        sub_atags = set(sub_soup.find_all("a", href=True))
        sub_links[parent_href] = []
        counter += 1
        # Avoiding exceptions like "missing schema"
        try:
            for sub_atag in sub_atags:
                sub_href = sub_atag.get('href')
                if '/p/' in sub_href and product in sub_href and re.search(r"^(http|https)://www.", sub_href):
                    sub_links[parent_href].append(sub_href)
                    # if(parent_a_tag)
                    counter += 1
                    print("\t" + sub_href)
                if add_https_rebel not in sub_href and product in sub_href:
                    print("fixed-->", urljoin(getUrl, sub_href))
                    fixed_links += 1
                    sub_links[parent_href].append(sub_href)
        except Exception:
            pass

        print("Links extracted: ", counter)
read = read_link(product, website_name)
extract_links = get_links()
# extract_sub_links = get_sub_links()
# extract_links_2 = get_sub_links()
print("Number of links extracted:",counter, "Number of links fixed:" , fixed_links)
print("number of links in parent:" , len(parent_links))
# get_txt = get_text_data()
