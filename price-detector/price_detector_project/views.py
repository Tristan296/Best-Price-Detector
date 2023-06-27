import requests
from bs4 import BeautifulSoup
import re


def read_page():
    product = input("Type a product: ")
    product = product.replace(" ", "+")

    url = f"https://www.amazon.com.au/s?k={product}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_product_names(soup):
    # Get product names
    product_names = soup.find_all("span", class_="a-size-base-plus")
    return product_names


def get_product_prices(soup):
    # Get prices
    product_prices = soup.find_all("span", class_="a-offscreen")
    return product_prices


def join_name_and_price(product_names, product_prices):
    products = []

    for name, price in zip(product_names, product_prices):
        product = {"Name": name.text.strip(), "Price": price.text.strip()}
        products.append(product)

    print(products)


soup = read_page()
names = get_product_names(soup)
prices = get_product_prices(soup)
join_name_and_price(names, prices)
