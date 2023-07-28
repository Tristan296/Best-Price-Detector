
import asyncio
import re
import time
import aiohttp
import requests
from bs4 import BeautifulSoup, SoupStrainer

async def fetch_price(session, product_link):
    try:
        async with session.get(product_link) as response:
            html_content = await response.text()
            return html_content
    except Exception as e:
        print(f"Error fetching {product_link}: {e}")
        return None


"""
    Extracts information about a product from an HTML document using the re.compile function (allows case-insensitive matching)
    Stores the parent html element of the product name in product_elements array.
    Stores the product names into a product_names array.

    Parameters:
        html (str): The HTML content to be parsed and searched.
        product_name (str): The name of the product to search for.

    Returns:
        tuple: A tuple containing three elements:
            - product_names (list): A list of product names that match the given product_name.
            - product_elements (list): A list of corresponding product elements (links) found in the HTML.
            - count (int): The number of products found that match the given product_name.
"""


async def extract_product_info(soup, product_name):
    count = 0
    product_data = {}
    pattern = re.compile(re.escape(product_name), re.IGNORECASE)
    matched_elements = soup.find_all(string=pattern)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for element in matched_elements:
            parent_element = element.find_parent()
            product_link = parent_element.get("href")

            if product_link is not None and product_link.startswith(('http://', 'https://')):
                tasks.append(fetch_price(session, product_link))

        html_contents = await asyncio.gather(*tasks)

    print("Number of html_contents:", len(html_contents))

    for i, element in enumerate(matched_elements):
        parent_element = element.find_parent()
        product_link = parent_element.get("href")

        if product_link is not None and product_link.startswith(('http://', 'https://')):
            if i < len(html_contents):  # Added this check to avoid the IndexError
                sub_product_soup = BeautifulSoup(html_contents[i], "lxml", parse_only=SoupStrainer("span"))
                price_pattern = r"\$\d+\.\d+|\£\d+|\d+\.\d+\s(?:USD|EUR)"
                prices = re.findall(price_pattern, sub_product_soup.get_text())

                if prices:
                    product_price = prices[0]
                else:
                    product_price = "Price not found"

                product_data[element.strip()] = {
                    "link": product_link.strip(),
                    "price": product_price,
                    "name": element.strip(),
                    "parent_element": parent_element
                }
                count += 1

    return product_data, count


async def get_url_formatting(product_name, website_name):
    product_end_formatted = product_name.replace(" ", "%20")
    product_formatted = product_name.replace(" ", "+")
    website_urls = {
        "rebelsport": f"https://www.rebelsport.com.au/search?q={product_end_formatted}",
        "harveynorman": f"https://www.harveynorman.com.au/search?q={product_formatted}",
        "ebay": f"https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={product_formatted}&_sacat=0",
        "thegoodguys": f"https://www.thegoodguys.com.au/SearchDisplay?categoryId=&storeId=900&catalogId=30000&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&orderBy=0&pageSize=30&searchTerm={product_formatted}",
        "kogan": f"https://www.kogan.com/au/shop/?q={product_formatted}",
        "officeworks": f"https://www.officeworks.com.au/shop/officeworks/search?q={product_end_formatted}&view=grid&page=1&sortBy=bestmatch",
        "jbhifi": f"https://www.jbhifi.com.au/search?page=1&query={product_end_formatted}&saleItems=false&toggle%5BonPromotion%5D=false",
        "ajeworld": f"https://ajeworld.com.au/collections/shop?q={product_formatted}", 
    }
    if website_name not in website_urls:
        print("Unsupported website name:", website_name)
        return None
        
    
    url_formatted = website_urls[website_name]
    return url_formatted

"""
    Extracts all the image urls in the website. 
    Uses Regex search() function to ensure the image url is an actual url, i.e. one hosted online
    
    E.g - Accepted url:
    url = https://www.rebelsport.com.au/on/demandware.static/-/Library-Sites-rebel-shared-library/default...
    
    E.g. - Url Ignored:
    url = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    
    Parameters:
        html (str): The HTML content to be parsed and searched.

    Returns:
        Array:
            - image_sources: A list of product image urls found in the html
"""


async def extract_images(soup):
    image_sources = []
    # Find all image elements in the HTML
    images = soup.find_all("img")

    for img in images:
        # Extract the 'src' attribute of each image element
        src = img.get("src")
        # Ensure that the src is an online link.
        if src and re.search(r"^(http|https)://", src):
            image_sources.append(src)

    return image_sources


async def get_product_price_fromLink(product_link, soup):
    prices = []
    for element in product_link:
        if element and re.search(r"^(http|https)://", element):
            price = soup.find_all("span")
            
            if price is not None:
                prices.append(price)
                
    return prices

        
async def fetch_html(url_):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    async with aiohttp.ClientSession() as session:        
        async with session.get(url_, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None


async def get_soup(url_):
    html = await fetch_html(url_)
    if html:
        return BeautifulSoup(html, "lxml")
    else:
        print(f"Failed to fetch the webpage: {url_}")
        return None
    
    
async def main():
    product_name = input("Enter product name: ")
    website_name = input("Enter website: ")

    formatted_url = await get_url_formatting(product_name, website_name)
    print(f"Now searching for {product_name} in url {formatted_url}")

    # Measure the execution time before starting the search
    start_time = time.time()

    soup = await get_soup(formatted_url)

    if soup:
        # Extract product information from the HTML
        product_data, count = await extract_product_info(soup, product_name)

        # Output the product information
        for product_info in product_data.values():
            print(f"Product Info:\n {product_info}\n")

            # Fetch additional product information using the product links
            # additional_soup = await get_soup(product_info['link'])
            # if additional_soup:
            #     additional_prices = await get_product_prices(additional_soup, additional_soup)
            #     print("Additional Prices:", additional_prices)

        print(f"Total number of products found: {count}")

        urls = await extract_images(soup)
        print(urls)

    # Measure the execution time after completing the search
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())