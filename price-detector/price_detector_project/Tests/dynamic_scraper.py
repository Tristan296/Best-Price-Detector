import re
import time
import requests
from bs4 import BeautifulSoup

def extract_product_info(html, product_name):
    soup = BeautifulSoup(html, 'lxml')
    
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
        product_names.append(element.strip())
        product_elements.append(str(parent_element))
        
    return product_names, product_elements

parent_links = []

def get_product_prices(html):
    parent_soup = BeautifulSoup(html, 'html.parser')
    # Finding all "span" tags in html
    span_elements = parent_soup.find_all('span')
    
    # Regular expression to match price patterns (e.g., $10.99, £20, 15.50 EUR, etc.)
    price_pattern = r'\$\d+\.\d+|\£\d+|\d+\.\d+\s(?:USD|EUR)'
    
    prices = []
    for element in span_elements:
        # Search for the price pattern in the text of the span element
        price_match = re.search(price_pattern, str(element.text))
        if price_match and element is not None:
            prices.append(price_match.group())
    
    return prices
            
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
    
product_name = input("Enter product name: ")
url = input('Enter website url: ')

# Use requests to fetch the HTML content of the webpage
response = requests.get(url)

if response.status_code == 200:
    count = 0
    html = response.text
    
    # Extract product information from the HTML
    product_names, product_elements = extract_product_info(html, product_name)

    # Output the product information
    for name, element in zip(product_names, product_elements):
        print(f"Product Name: {name}\n")
    
    x = get_product_prices(html)
    print(x)
    
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
