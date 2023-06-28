import requests
from bs4 import BeautifulSoup
import re

product = input("Type a product: ")
website_name = input("type a website: ")



def read_page(product, website_name):
    product = product.replace(" ", "+")
    website_name = website_name.replace(" ", "").lower()
    url = f"https://www.{website_name}.com.au/s?k={product}"
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
    for link in soup.find_all('a'):#looks for the "a" tag in html
        print(link.get('href'))

def get_product_names(soup, product):
    name_elements = soup.find_all(string=re.compile(product))
    # Extract the product names from the text nodes
    print("\n\nnames: ",name_elements ,"\n\n")
    names = [element.strip() for element in name_elements]
    
    return names
  

def get_product_prices(soup):
    price_symbols = soup.find_all("span", string=re.compile(r"\$\d+\.?\d*"))

    # Extract the prices using regular expressions
    prices = [re.search(r"\$\d+\.?\d*", symbol.get_text()).group() for symbol in price_symbols]
    return prices

def join_name_and_price(product_names, product_prices):
    products = []
    
    for name, price in zip(product_names, product_prices):
        product = {"Name": name.strip(), "Price": price.strip()}
        products.append(product)

    print(products)
    
soup = read_page(product, website_name)
# links = get_product_links()
names = get_product_names(soup, product)
prices = get_product_prices(soup)
join_name_and_price(names, prices)