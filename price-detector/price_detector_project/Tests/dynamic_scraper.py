import asyncio
import re
import time
import aiohttp
import requests
from bs4 import BeautifulSoup

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


async def fetch_price(session, product_link):
    try:
        async with session.get(product_link) as response:
            html_content = await response.text()
            return html_content
    except Exception as e:
        print(f"Error fetching {product_link}: {e}")
        return None

async def extract_product_info(soup, product_name):
    count = 0
    product_names = []
    product_elements = []
    product_prices = []
    pattern = re.compile(re.escape(product_name), re.IGNORECASE)
    matched_elements = soup.find_all(string=pattern)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for element in matched_elements:
            parent_element = element.find_parent()
            product_link = parent_element.get("href")

            if product_link is not None and re.search(r"^(http|https)://", product_link):
                tasks.append(fetch_price(session, product_link))

        html_contents = await asyncio.gather(*tasks)

    print("Number of html_contents:", len(html_contents))

    for i, element in enumerate(matched_elements):
        parent_element = element.find_parent()
        product_link = parent_element.get("href")

        if product_link is not None and re.search(r"^(http|https)://", product_link):
            if i < len(html_contents):  # Added this check to avoid the IndexError
                sub_product_soup = BeautifulSoup(html_contents[i], "html.parser")
                price_pattern = r"\$\d+\.\d+|\£\d+|\d+\.\d+\s(?:USD|EUR)"
                prices = re.findall(price_pattern, sub_product_soup.get_text())

                if prices:
                    product_price = prices[0]
                else:
                    product_price = "Price not found"

                product_names.append(element.strip())
                product_elements.append(product_link.strip())
                product_prices.append(product_price)

                count += 1

    return product_names, product_elements, product_prices, count


"""
    Extracts all the prices in the website. This method is hardcoded to work for a large majority of websites.
    This is due to a smaller number of websites utilising a different html element for prices.
    
    E.g:
        Rebel Sport, Aje World, Harveynorman, JBHIFI, ASOS, Target, BIGW: <span class="$...">
        Officeworks: <div data="$...">
        Bunnings: <p data-locator="$..."> 
        
    Parameters:
        html (str): The HTML content to be parsed and searched.

    Returns:
        Array:
            - prices (list): A list of product prices found in the html
"""

async def get_product_prices(html, soup):
    # Finding all "span" tags in html
    span_elements = soup.find_all("span")

    # Regular expression to match price patterns (e.g., $10.99, £20, 15.50 EUR, etc.)
    price_pattern = r"\$\d+\.\d+|\£\d+|\d+\.\d+\s(?:USD|EUR)"

    prices = []
    count = 1
    for element in span_elements:
        # Search for the price pattern in the text of the span element
        price_match = re.search(price_pattern, str(element.text))
        if price_match and element is not None:
            product_details = {price_match.group(), count}
            prices.append(product_details)
            count += 1

    return prices


async def get_url_formatting(product_name, website_name):
    product_end_formatted = product_name.replace(" ", "%20")
    product_formatted = product_name.replace(" ", "+")
    website_urls = {
        "rebelsport": f"https://www.rebelsport.com.au/search?q={product_end_formatted}",
        "harveynorman": f"https://www.harveynorman.com.au/search?q={product_formatted}",
        "ebay": f"https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={product_name}&_sacat=0",
        "thegoodguys": f"https://www.thegoodguys.com.au/SearchDisplay?categoryId=&storeId=900&catalogId=30000&langId=-1&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&orderBy=0&pageSize=30&searchTerm={product_formatted}",
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
           # print("Processing URL:", element)
           # getUrl = requests.get(element)
            price = soup.find_all("span")
            
            if price is not None:
                prices.append(price)
                
    return prices


async def fetch_html(url_):
    async with aiohttp.ClientSession() as session:
        async with session.get(url_) as response:
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
    soup = await get_soup(formatted_url)

    if soup:
        # Extract product information from the HTML
        product_names, product_links, product_prices, count = await extract_product_info(
            soup, product_name
        )

        # Output the product information
        for name, link, price in zip(product_names, product_links, product_prices):
            print(f"Product Name: {name}\n")
            print(f"Product Price: {price}\n")
            print(f"Product link: {link}\n")

            # Fetch additional product information using the product links
            additional_soup = await get_soup(link)
            if additional_soup:
                additional_prices = await get_product_prices(additional_soup, additional_soup)
                print("Additional Prices:", additional_prices)

        print(f"Total number of products found: {count}")

        urls = await extract_images(soup)
        print(urls)


if __name__ == "__main__":
    asyncio.run(main())
