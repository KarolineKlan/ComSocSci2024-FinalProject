from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

LINK = "https://www.bilkatogo.dk/kategori/"
categories = ["frugt-og-groent/", "koed-og-fisk/", "mejeri-og-koel/"]

def extract_products(url, category):
    products_df = pd.DataFrame(columns=['product_id', 'name', 'price', 'link'])
    page_counter = 0
    
    SCRAPE_LINK = f"{url}/{category}"   # Construct the URL for the first case with no page number
    product_card_containers = ["dummy"]
    
    while len(product_card_containers) != 0:
        print("The length of product_card_containers is: ", len(product_card_containers))
        print("The page counter is: ", page_counter)
        
        # Initialize Edge WebDriver
        options = webdriver.EdgeOptions()
        options.add_argument('headless')  # To run Edge in headless mode
        driver = webdriver.Edge(options=options)

        # Load the webpage
        driver.get(SCRAPE_LINK)

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
        
        
        #JACK INDSÆTTER KODE HER TIL AT EXTRACTE PRODUCT_ID 
        #TODO:

        
        
        page_counter += 1
        SCRAPE_LINK = f"{url}/{category}/?page={page_counter}"
        
    return products_df
    





extract_products(LINK, categories[1])