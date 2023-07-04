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
            sort_option = input(
                """ Recommended for you is default sort
            1. New In
            2. Top Rated
            3. Price: Low to High
            4. Price: High to Low
            """
            )
            if sort_option == "1":
                url = f"https://www.{website_name}.com.au/search?q={product_end_formatted}&srule=most-recent&start=0&sz=60"
            elif sort_option == "2":
                url = f"https://www.{website_name}.com.au/search?q={product_end_formatted}&srule=top%20rated-top%20sellers&start=0&sz=60"
            elif sort_option == "3":
                url = f"https://www.{website_name}.com.au/search?q={product_end_formatted}&srule=price-ascending&start=0&sz=60"
            elif sort_option == "4":
                url = f"https://www.{website_name}.com.au/search?q={product_end_formatted}&srule=price-descending&start=0&sz=60"
            elif sort_option == "":
                url = f"https://www.{website_name}.com.au/{product_end_formatted}&srule=recommended-for-you&start=0&sz=60"

            print(url)
        elif website_name == "harveynorman":
            sort_option = int(
                input(
                    """ Relevance is default sort
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
                print(
                    "Please ensure you pick the above options from 1-7. e.g. input: '1'"
                )
        elif website_name == "ebay":
            url = f"https://www.{website_name}.com.au/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={product_formatted}&_sacat=0"
        elif website_name == "thegoodguys":
            url = f"https://www.{website_name}.com.au/SearchDisplay?categoryId=&storeId=900&catalogId=30000&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&orderBy=0&pageSize=30&searchTerm={product_formatted}"
        elif website_name == "kogan":
            url = f"https://www.{website_name}.com/au/shop/?q={product_formatted}"
        elif website_name == "officeworks":
            url = f"https://www.officeworks.com.au/shop/officeworks/search?q={product_end_formatted}&view=grid&page=1&sortBy=bestmatch"
            # url = f"https://www.{website_name}.com.au/shop/{website_name}/search?q={product}&sortBy=bestmatch"
        else:
            print(
                "Please ensure you have spelt the website correctly and chosen from the options."
            )
        print(url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = self.get_with_retries(url, headers)
        if response is not None:
            soup = BeautifulSoup(response.content, "lxml")
            return soup
        # Response from url is None - meaning website content isn't working.
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
        for link in soup.find_all("a"):
            href = link.get("href")
            if href is not None and str(self.product) in href:
                urls.append(href)
        return urls


class ProductDetailsExtractor:
    def __init__(self, soup):
        self.soup = soup

    def get_product_details_harveynorman(self):
        products = []
        count = 1
        product_items = self.soup.select(".product-item")
        for item in product_items:
            name = item.select_one("a.name").text.strip()
            price = item.select_one("span.price").text.strip()
            product = {"Name": name, "Price": price, "Count": count}
            products.append(product)
            count += 1
        return products

    # Not working
    def get_product_details_officeworks(self):
        products = []
        product_items = self.soup.select(
            ".TileWrapper__TileWrapperStyled-sc-1ck0iwt-0.gFALXK"
        )
        for item in product_items:
            name = item.select_one(".default-product-title").text.strip()
            price = item.select_one(".price-clone").text.strip()
            product = {"Name": name, "Price": price}
            products.append(product)
        return products

    def get_product_details_thegoodguys(self):
        products = []
        count = 1
        product_items = self.soup.select(".product-tile")
        for item in product_items:
            name = item.select_one("h4").text.strip()
            price_element = item.select_one(".pricepoint-price--promo")
            price = price_element.get_text(strip=True) if price_element else None
            product = {"Name": name, "Price": price, "Count": count}
            products.append(product)
            count += 1
        return products

    # Not working
    def get_product_details_kogan(self):
        products = []
        product_items = self.soup.select("._1umis")
        for item in product_items:
            name = item.select_one("h2._1A_Xq.a").text.strip()
            price = item.select_one("._2AQgf").text.strip()
            product = {"Name": name, "Price": price}
            products.append(product)
        return products
    
    def get_product_details_rebelsport(self):
        products = []
        count = 1
        product_items = self.soup.select(".product-tile")
        for item in product_items:
            name = item.select_one(".name-link").text.strip()
            price = item.select_one("span.price-sales").text.strip()
            price = re.search(r"\d+\.\d+", price).group()
            product = {"Name": name, "Price": f"${price}", "Count": count}
            products.append(product)
            count += 1
        return products

    def get_product_details_ebay(self):
        products = []
        count = 1
        product_items = self.soup.select("li.s-item.s-item__pl-on-bottom")
        for item in product_items:
            name = item.select_one(".s-item__title").text.strip()
            price = item.select_one("span.s-item__price").text.strip()
            price = re.search(r"\d+\.\d+", price).group()
            product = {"Name": name, "Price": f"${price}", "Count": count}
            products.append(product)
            count += 1
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

elif "officeworks" in website_name:
    print("Scraping Officeworks...")
    details_extractor = ProductDetailsExtractor(soup)
    print(soup.find_all(""))
    product_details = details_extractor.get_product_details_officeworks()
    print(product_details)
    
elif "ebay" in website_name:
    print("Scraping Ebay...")
    details_extractor = ProductDetailsExtractor(soup)
    print(soup.find_all(""))
    product_details = details_extractor.get_product_details_ebay()
    print(product_details)

soup = read_page(product, website_name)
# links = get_product_links()
names = get_product_names(soup, product)
prices = get_product_prices(soup)
join_name_and_price(names, prices)

