import requests
from bs4 import BeautifulSoup

product = input("Type a product: ")
website_name = input("type a website: ")
def read_page(product, website_name):
    product = product.replace(" ", "+")
    website_name = website_name.replace(" ", "").lower()
    # url = f"https://www.{website_name}.com.au/s?k={product}"
    url = f"https://www.{website_name}.com.au/"
    print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return url

def get_product_links():
    getUrl = read_page(product, website_name)#gets the url param from "read_page" function
    reqs = requests.get(getUrl)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    print("links that contain " + str(product))
    for link in soup.find_all('a'):#looks for the "a" tag in html
        href = link.get('href')
        if href is not None:#Fixes the TypeError: argument of type 'NoneType' is not iterable
              if str(product) in link.get('href'):
                print(link.get('href'))      

soup = read_page(product, website_name)
links = get_product_links()
