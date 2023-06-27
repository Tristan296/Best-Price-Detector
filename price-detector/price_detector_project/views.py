import requests
from bs4 import BeautifulSoup
import re

product = input("Type a product: ")

def read_page(product):
    product = product.replace(" ", "+")

    url = f"https://www.amazon.com.au/s?k={product}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_product_names(soup, product):
    name_elements = soup.find_all(string=re.compile(product))
    # Extract the product names from the text nodes
    print("\n\nnames: ",name_elements ,"\n\n")
    names = [element.strip() for element in name_elements]
    
    return names
  

def get_product_prices(soup):
    """
        create an expression that returns the data inside
        quotations after the $= and before the </p> by specifying $(.*?)</p>.
    """
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
    
soup = read_page(product)
names = get_product_names(soup, product)
prices = get_product_prices(soup)
join_name_and_price(names, prices)
