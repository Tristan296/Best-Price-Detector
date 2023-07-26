import asyncio
import re
import time
import aiohttp
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


async def extract_product_info(soup, product_name):
    count = 0
    product_names = []
    product_elements = []
    product_prices = []
    # Use re.compile to create a case-insensitive regex pattern for the product name
    pattern = re.compile(re.escape(product_name), re.IGNORECASE)
    matched_elements = soup.find_all(string=pattern)

    for element in matched_elements:
        # Get the parent element that contains the product name
        parent_element = element.find_parent()
        product_link = parent_element.get("href")
        
        # Check each product link and get the price
        if product_link is not None and re.search(r"^(http|https)://", product_link):
            print(f"Searching {product_link}...\n")
            sub_product_soup = await get_soup(product_link)
            
            # Regular expression to match price patterns (e.g., $10.99, £20, 15.50 EUR, etc.)
            price_pattern = r"\$\d+\.\d+|\£\d+|\d+\.\d+\s(?:USD|EUR)"
            
            # Search for the price pattern in the entire HTML
            prices = re.findall(price_pattern, sub_product_soup.get_text())
            
            if prices:
                # Take the first price found
                product_price = prices[0]
            else:
                product_price = "Price not found"
            
            product_names.append(element.strip())
            product_elements.append(product_link.strip())
            product_prices.append(product_price)
            
            count += 1
    
    return product_names, product_elements, product_prices, count


async def get_soup(url_):
    html = await fetch_html(url_)

    if html:
        return BeautifulSoup(html, "lxml")
    else:
        print(f"Failed to fetch the webpage: {url_}")
        return None

async def fetch_html(url_):
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None



async def get_soup_with_selenium(url_):
    # Initialize the Chrome Web Driver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode to avoid opening a visible browser window
    driver = webdriver.Chrome(options=options)

    driver.get(url_)
    
    # Get the page source HTML
    html = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Create a BeautifulSoup object from the page source
    soup = BeautifulSoup(html, "html.parser")

    return soup


async def get_url_formatting(product_name, website_name):
    website_urls = {
        "rebelsport": f"https://www.rebelsport.com.au/search?q={product_name}",
        "harveynorman": f"https://www.harveynorman.com.au/search?q={product_name}",
        "ebay": f"https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={product_name}&_sacat=0",
        "thegoodguys": f"https://www.thegoodguys.com.au/SearchDisplay?categoryId=&storeId=900&catalogId=30000&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&orderBy=0&pageSize=30&searchTerm={product_name}",
        "kogan": f"https://www.kogan.com/au/shop/?q={product_name}",
        "officeworks": f"https://www.officeworks.com.au/shop/officeworks/search?q={product_name}&view=grid&page=1&sortBy=bestmatch",
        "amazon": f"https://www.amazon.com.au/s?k={product_name}",
        "jbhifi": f"https://www.jbhifi.com.au/search?page=1&query={product_name}&saleItems=false&toggle%5BonPromotion%5D=false",
        "ajeworld": f"https://ajeworld.com.au/collections/shop?q={product_name}", 
        "bestbuy" : f"https://www.bestbuy.com/site/searchpage.jsp?st={product_name}"
    }
    if website_name not in website_urls:
        print("Unsupported website name:", website_name)
        return None
        
    
    url_formatted = website_urls[website_name]
    return url_formatted


async def main():
    product_name = input("Enter product name: ")
    website_name = input("Enter website: ")
    formatted_url = await get_url_formatting(product_name, website_name)
    print(f"Now searching for {product_name} in url {formatted_url}")

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(requests.get(formatted_url).content, "html.parser")
    product_names, product_elements, product_prices, count = await extract_product_info(soup, product_name)

    # Output the product information from regular HTML content
    print("Product names from regular HTML content:")
    for name, element in zip(product_names, product_elements):
        print(f"Product Name: {name}")
        print(f"Product link: {element}")
        print()

    # Use Selenium to parse the JavaScript-rendered content
    soup_with_js = await get_soup_with_selenium(formatted_url)
    product_names, product_elements, product_prices, count = await extract_product_info(soup_with_js, product_name)

    # Output the product information from JavaScript-rendered content
    print("Product names from JavaScript-rendered content:")
    for name, element, price in zip(product_names, product_elements, product_prices):
        print(f"Product Name: {name}")
        print(f"Product link: {element}")
        print(f"Product Price: {price}")
        print()

    # ... (other code remains the same)

if __name__ == "__main__":
    asyncio.run(main())