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
        # Append the product name and its parent element to the lists
        product_link = parent_element.get("href")
        if product_link is not None:
            product_names.append(element.strip())
            product_elements.append(product_link)
            count += 1

    return product_names, product_elements, count


"""
    Extracts all the prices in the website. This method is hardcoded to work for a large majority of websites.
    This is due to a smaller number of websites utilising a different html element for prices.
    
    E.g:
        Rebel Sport, Aje World, Harveynorman, JBHIFI, Amazon, ASOS, Target, BIGW: <span class="$...">
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


async def get_product_price_fromLink(product_elements, soup):
    prices = []
    for element in product_elements:
        print("Processing URL:", element)
        getUrl = requests.get(element)
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
    name = input("Enter website: ")
    url_ = f"https://www.{name}.com.au/search?q={product_name}&lang=en_AU"

    soup = await get_soup(url_)

    if soup:
        # Extract product information from the HTML
        product_names, product_elements, count = await extract_product_info(
            soup, product_name
        )

        # Extract product price from product links
        # product_price = get_product_price_fromLink(str(product_elements))
        # Output the product information
        for name, element in zip(product_names, product_elements):
            print(f"Product Name: {name}\n")
            print(f"Product link: {element}\n")

        print(f"Total number of products found: {count}")

        urls = await extract_images(soup)
        print(urls)


if __name__ == "__main__":
    asyncio.run(main())
