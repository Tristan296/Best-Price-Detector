import re
import time
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
def extract_product_info(html, product_name):
    soup = BeautifulSoup(html, 'lxml')
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
            count+=1
        
    return product_names, product_elements, count

parent_links = []


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

def get_product_prices(html):
    parent_soup = BeautifulSoup(html, 'html.parser')
    # Finding all "span" tags in html
    span_elements = parent_soup.find_all('span')
    
    # Regular expression to match price patterns (e.g., $10.99, £20, 15.50 EUR, etc.)
    price_pattern = r'\$\d+\.\d+|\£\d+|\d+\.\d+\s(?:USD|EUR)'
    
    prices = []
    count = 1
    for element in span_elements:
        # Search for the price pattern in the text of the span element
        price_match = re.search(price_pattern, str(element.text))
        if price_match and element is not None:
            product_details = {price_match.group(), count}
            prices.append(product_details)
            count+=1
    
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
def extract_images(html):
    soup = BeautifulSoup(html, 'html.parser')
    image_sources = []
    # Find all image elements in the HTML
    images = soup.find_all('img')
    
    for img in images:
        # Extract the 'src' attribute of each image element
        src = img.get('src')
        # Ensure that the src is an online link.
        if src and re.search(r'^(http|https)://', src):
            image_sources.append(src)
            
    return image_sources

def get_product_price_fromLink(product_elements):
    prices = []
    for element in product_elements:
        print("Processing URL:", element)
        getUrl = requests.get(element)
        parent_soup = BeautifulSoup(getUrl.content, 'html.parser')
        price = parent_soup.find_all('span')
        if price is not None:
            prices.append(price)
    return prices


product_name = input("Enter product name: ")
name = input('Enter website: ')
url_ = f"https://www.{name}.com.au/search?q={product_name}&lang=en_AU"

# Use requests to fetch the HTML content of the webpage
response = requests.get(url_)

if response.status_code == 200:
    count = 0
    html = response.text
    
    # Extract product information from the HTML
    product_names, product_elements, count = extract_product_info(html, product_name)

    # Extract product price from product links
  #   product_price = get_product_price_fromLink(str(product_elements))
    # Output the product information
    for name, element in zip(product_names, product_elements):
        print(f"Product Name: {name}\n")
       #  print(f"Product Price: {price}")
        print(f"Product link: {element}\n")
        
    print(f"Total number of products found:  {count}")
   # price = get_product_prices(html)
   # print(price)
    urls = extract_images(html)
    print(urls)
    
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
