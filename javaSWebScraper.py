from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Path to your Chrome WebDriver executable
webdriver_path = '/Users/jacob/OneDrive/Uni/6. Semester/Social Informatik/ComSocSci2024-FinalProject/WebDriver/msedgedriver.exe'

# URL of the webpage
url = 'https://www.bilkatogo.dk/kategori/koed-og-fisk/'

# Initialize Chrome WebDriver
options = webdriver.Edge()
options.add_argument('headless')  # To run Chrome in headless mode
driver = webdriver.Edge(executable_path=webdriver_path, options=options)

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
div_element = soup.find('div', {'data-v-da5161c2': True, 'data-v-e0535ac4': True})

# Print the div element
print(div_element)