import re
from selenium import webdriver
from bs4 import BeautifulSoup

def extract_product_info(html, product_name):
    soup = BeautifulSoup(html, 'html.parser')

    product_names = []
    product_elements = []

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

# Initialize the Chrome Web Driver
driver = webdriver.Chrome()

driver.get(url)

# Get the page source HTML
html = driver.page_source

# Extract product information from the HTML
product_names, product_elements = extract_product_info(html, product_name)

# Close the browser
driver.quit()

# Output the product information
for name, element in zip(product_names, product_elements):
    print(f"Product Name: {name}")
    print("Containing Element:")
    print(element)
    print()