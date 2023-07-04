import requests
from bs4 import BeautifulSoup
import re

product = input("Type a product: ")
website_name = input("type a website: ")
    
def read_page(product, website_name):
    website_name = website_name.replace(" ", "").lower()
    if "rebel" in website_name:
        product_formatted = product.replace(" ", "/")
        product_end_formatted = product.replace(" ", "%20")
        url = f"https://www.{website_name}.com.au/{product_formatted}?search_term={product_end_formatted}"
    
    elif website_name == "amazon":
        product = product.replace(" ", "+")
        url = f"https://www.{website_name}.com.au/s?k={product}"
    
    elif website_name == "jbhifi":
        product = product.replace(" ", "+")
        url = f"https://www.{website_name}.com.au/search?page=1&query={product}&saleItems=false&toggle%5BonPromotion%5D=false"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")
    return soup, url

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

def get_amazon_product_details(soup):
    products = []
    product_items = soup.select(".a-section")
    for item in product_items:
        name = item.select_one("span.a-size-base-plus").text.strip()
        price = item.select_one("span.a-offscreen").text.strip()
        price = re.search(r'\d+\.\d+', price).group()
        product = {"Name": name, "Price": f"${price}"}
        products.append(product)
        
    print(products)
    return products

def get_product_details_rebelsport(soup):
    products = []
    product_items = soup.select(".product-tile")
    for item in product_items:
        name = item.select_one(".name-link").text.strip()
        price = item.select_one("span.price-sales").text.strip()
        price = re.search(r'\d+\.\d+', price).group()
        product = {"Name": name, "Price": f"${price}"}
        products.append(product)
        
    print(products)
    return products

def get_product_details_jbhifi(soup):
    products = []
    product_items = soup.select("._10ipotxu")
    for item in product_items:
        name = item.select_one("._10ipotx5").text.strip()
        price = item.select_one("span.PriceFont_fontStyle__w0cm2q1").text.strip()
        product = {"Name": name, "Price": f"${price}"}
        products.append(product)
        
    print(products)
    return products

soup, url = read_page(product, website_name)
if "rebel" in website_name:
    print("Scraping Rebel Sports...")
    names = get_product_details_rebelsport(soup)
elif "amazon" in website_name:
    print("Scraping Amazon...")
    names = get_amazon_product_details(soup)
elif "jb" in website_name:
    print("Scraping JBHIFI...")
    names = get_product_details_jbhifi(soup)
    

soup = read_page(product, website_name)
# links = get_product_links()
names = get_product_names(soup, product)
prices = get_product_prices(soup)
join_name_and_price(names, prices)

