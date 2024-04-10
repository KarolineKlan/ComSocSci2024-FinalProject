from selenium import webdriver
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup

LINK = "https://www.bilkatogo.dk/kategori/"
categories = ["frugt-og-groent/", "koed-og-fisk/", "mejeri-og-koel/"]


SCRAPE_LINK = LINK + categories[1]

# URL of the webpage
url = SCRAPE_LINK

# Initialize Edge WebDriver
options = webdriver.EdgeOptions()
options.add_argument('headless')  # To run Edge in headless mode
driver = webdriver.Edge(options=options)

# Load the webpage
driver.get(url)

# Wait for a few seconds to ensure JavaScript execution
time.sleep(5)

# Get the page source after JavaScript execution
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(page_source, 'html.parser')

# Find the div element with specific attributes
div_element = soup.find_all('div', {'data-v-da5161c2': True, 'data-v-e0535ac4': True})
# Find all elements with product-card-container class
product_card_containers = soup.find_all('div', {'class' : 'product-card-container'})

# You can now process both sets of elements separately
print(div_element)
print(product_card_containers)

# Print the div element
print(div_element)