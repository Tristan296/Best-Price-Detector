#WORKING FILE - USE THIS FOR UPDATES!!!!!!
"""
    DO NOT DELETE THIS FILE. THIS FILE IS USED TO TEST DIFFERENT FUNCTIONALITIES OF
    LINK EXTRACTTION!

    CODE THAT PASSES THROUGH WILL BE IMPLEMENTED TO THE FILE LINK_EXTRACTOR
"""
import requests
from bs4 import BeautifulSoup
counter = 0
duplicate_counter = 0;
getUrl = requests.get("https://www.jbhifi.com.au")
parent_soup = BeautifulSoup(getUrl.content, 'html.parser')
#Set() removes duplicates
parent_a_tag = set(parent_soup.find_all("a", href=True))
parent_links = []
sub_links = {}
for link in parent_a_tag: 
    parent_href = link.get('href')
    # parent_links.append(parent_href)
    # Checking for duplicates again as set() doesn't remove all duplicates so we would need to search our "parent_links"
    # array and compare it if the next link is doesn't exist in our current array                                                                                                    
    if parent_href not in parent_links:
        parent_links.append(parent_href)
        print(parent_href)
        # counter += 1
    #This is used to get the stats of how many duplicate links we have detected
    if(parent_href in parent_links):
        duplicate_counter += 1;
    #print(parent_href)
    
    #accessing parents child --> sub links
    sub_request = requests.get(parent_href)
    sub_soup = BeautifulSoup(sub_request.content, 'html.parser')
    sub_atags = set(sub_soup.find_all("a", href=True))
    sub_links[parent_href] = []
    counter += 1
    for sub_atag in sub_atags:
        sub_href = sub_atag.get('href')
        if '/p/' in sub_href:

            sub_links[parent_href].append(sub_href)
            # if(parent_a_tag)
            counter+=1;
            print("\t"+sub_href)
    print("Links extracted: ",counter)
    print("Duplicated links: ", duplicate_counter)
    # while True:
    #     try:
    #         sub_request = requests.get(parent_href)
    #         sub_soup = BeautifulSoup(sub_request.content, 'html.parser')
    #         sub_atags = set(sub_soup.find_all("a", href=True))
    #         sub_links[parent_href] = []
    #         counter += 1
    #         for sub_atag in sub_atags:
    #             sub_href = sub_atag.get('href')
    #             if '/p/' in sub_href:

    #                 sub_links[parent_href].append(sub_href)
    #                 # if(parent_a_tag)
    #                 counter+=1;
    #                 print("\t"+sub_href)
    #         print("Links extracted: ",counter)
    #         print("Duplicated links: ", duplicate_counter)

    #     except ValueError:
    #         print("sd")
    #     #print(sub_href)
    #     print(parent_href)
    
print("Duplicate links found in parent:", duplicate_counter)
print("counter: ", counter)
    