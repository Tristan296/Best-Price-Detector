import requests
from bs4 import BeautifulSoup
import re
import itertools
import random
import time

class LinkExtractor:
    def __init__(self, product, website_name):
        self.product = product
        self.website_name = website_name

    def read_page(self):
        # Remove whitespace in website name to use for the URL.
        website_name = self.website_name.replace(" ", "").lower()
        product_end_formatted = self.product.replace(" ", "%20")
        product_formatted = self.product.replace(" ", "+")
        if website_name == "rebelsport":
            # Replace whitespaces in the product name to match the URL format.
            product_formatted = self.product.replace(" ", "/")
            url = f"https://www.{website_name}.com.au/{product_formatted}?search_term={product_end_formatted}"
        elif website_name == "harveynorman":
            sort_option = int(input(""" Relevance is default sort
            1. Sort by Price: Low to High
            2. Sort by Price High to Low
            3. Name: A to Z
            4. Name: Z to A
            5. Highest Rated
            """))
            if sort_option == 1:
                url = f"https://www.{website_name}.com.au/catalogsearch/result/index/?dir=asc&order=price&q={product}#toolbar-top"
            elif sort_option == 2:
                url = f"https://www.{website_name}.com.au/catalogsearch/result/index/?dir=desc&order=price&q={product}#toolbar-top"
            elif sort_option == 3:
                url = f"https://www.{website_name}.com.au/catalogsearch/result/index/?dir=asc&order=name&q={product}#toolbar-top"
            elif sort_option == 4:
                url = f"https://www.{website_name}.com.au/catalogsearch/result/index/?dir=desc&order=name&q={product}#toolbar-top"
            elif sort_option == 5:
                url = f"https://www.{website_name}.com.au/catalogsearch/result/index/?dir=desc&order=reviews&q={product}#toolbar-top"
            elif sort_option == None:
                url = f"https://www.{website_name}.com.au/catalogsearch/result/?q={product}"
            else:
                print("Please ensure you pick the above options from 1-7. e.g. input: '1'")
        elif website_name == "binglee":
            url = f"https://www.{website_name}.com.au/search?q={product}"
        elif website_name == "thegoodguys":
            url = f"https://www.{website_name}.com.au/SearchDisplay?categoryId=&searchTerm={product_formatted}"
        elif website_name == "kogan":
            url = f"https://www.{website_name}.com/au/shop/?q={product_formatted}"
        elif website_name == "officeworks":
            url = f"https://www.{website_name}.com.au/shop/{website_name}/search?q={product}&sortBy=bestmatch"
        else:
            print("Please ensure you have spelt the website correctly and chosen from the options.")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = self.get_with_retries(url, headers)
        if response is not None:
            soup = BeautifulSoup(response.content, "lxml")
            return soup
        else:
            print("The site's content could not be reached.")
            exit()

    def get_with_retries(self, url, headers, retries=3, delay=1):
        for i in range(retries):
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException:
                print(f"Failed to retrieve URL: {url}. Retrying ({i+1}/{retries})...")
                time.sleep(delay)
        print(f"Failed to retrieve URL: {url} after {retries} retries.")
        return None

    def extract_links(self):
        soup = self.read_page()
        urls = []
        print("Links that contain " + str(self.product))
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and str(self.product) in href:
                urls.append(href)
        return urls


class ProductDetailsExtractor:
    def __init__(self, soup):
        self.soup = soup

    def get_product_details_harveynorman(self):
        products = []
        count = 0       
        product_items = self.soup.select(".product-item")
        for item in product_items:
            name = item.select_one("a.name").text.strip()
            price = item.select_one("span.price").text.strip()
            product = {"Name": name, "Price": price, "Count": count}
            products.append(product)
            count+=1
        return products

    
    def get_product_details_officeworks(self):
        products = []
        product_items = self.soup.select(".sc-eNQAEJ Tile-iqbpf7-0 inMdYv")
        for item in product_items:
            name = item.select_one("h5.DefaultProductTile__ProductName-dfe2sm-1 dRgJNf").text.strip()
            price = item.select_one(".ProductPrice__Wrapper-sc-1ye3dgu-0 cXoUph").text.strip()
            product = {"Name": name, "Price": f"${price}"}
            products.append(product)
        return products
    
    def get_product_details_thegoodguys(self):
        products = []
        count=1
        product_items = self.soup.select(".product-tile")
        for item in product_items:
            name = item.select_one("h4.product-tile-name").text.strip()
            price = item.select_one(".pricepoint-price--promo").text.strip()
            product = {"Name": name, "Price": price, "Count": count}
            products.append(product)
            count+=1
        return products
    
    def get_product_details_kogan(self):
        products = []
        product_items = self.soup.select("._1umis")
        for item in product_items:
            name = item.select_one("h2._1A_Xq.a").text.strip()
            price = item.select_one("._2AQgf").text.strip()
            product = {"Name": name, "Price": price}
            products.append(product)
        return products
    
    def get_product_details_binglee(self):
        products = []
        product_items = self.soup.select(".product-list-item")
        for item in product_items:
            name = item.select_one("a.block").text.strip()
            price = item.select_one("span.pb-1").text.strip()
            product = {"Name": name, "Price": price}
            products.append(product)
        return products
  
    def get_product_details_rebelsport(self):
        products = []
        count = 0
        product_items = self.soup.select(".product-tile")
        for item in product_items:
            name = item.select_one(".name-link").text.strip()
            price = item.select_one("span.price-sales").text.strip()
            price = re.search(r'\d+\.\d+', price).group()
            product = {"Name": name, "Price": f"${price}", "Count": count}
            products.append(product)
            count+=1
        return products
    

    # Retrieve user input
product = input("Type a product: ")
website_name = input("Type a website: ")
# Create a new instance of the LinkExtractor class
link_extractor = LinkExtractor(product, website_name)
# Retrieve the links and soup
links = link_extractor.extract_links()
soup = link_extractor.read_page()
    

if "rebel" in website_name:
    print("Scraping Rebel Sports...")
    details_extractor = ProductDetailsExtractor(soup)
    product_details = details_extractor.get_product_details_rebelsport()
    print(product_details)
        
elif "harvey" in website_name and "norman" in website_name:
    print("Scraping Harvey Norman...")
    details_extractor = ProductDetailsExtractor(soup)
    product_details = details_extractor.get_product_details_harveynorman()
    print(product_details)

elif "good" in website_name and "guys" in website_name:
    print("Scraping The Good Guys...")
    details_extractor = ProductDetailsExtractor(soup)
    product_details = details_extractor.get_product_details_thegoodguys()
    print(product_details)

elif "bing" in website_name and "lee" in website_name:
    print("Scraping Bing Lee...")
    details_extractor = ProductDetailsExtractor(soup)
    product_details = details_extractor.get_product_details_binglee()
    print(product_details)
    
elif "officeworks" in website_name:
    print("Scraping Officeworks...")
    details_extractor = ProductDetailsExtractor(soup)
    print(soup.find_all(''))
    product_details = details_extractor.get_product_details_officeworks()
    print(product_details)