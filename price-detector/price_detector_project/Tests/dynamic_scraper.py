import re
import time
import requests
from bs4 import BeautifulSoup

def extract_product_info(html, product_name):
    soup = BeautifulSoup(html, 'html.parser')

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


product_name = input("Enter product name:  ")
url = input('Enter website url:  ')

# Use requests to fetch the HTML content of the webpage
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    # Extract product information from the HTML
    product_names, product_elements, execution_time = extract_product_info(html, product_name)

    # Output the product information
    for name, element in zip(product_names, product_elements):
        print(f"Product Name: {name}")
        print("Containing Element:")
        print(element)
        print()
else:
    print(f"Failed to fetch the webpage. Status code: {response.status_code}")
