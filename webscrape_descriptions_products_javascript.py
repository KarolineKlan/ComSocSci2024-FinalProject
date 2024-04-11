import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from joblib import Parallel, delayed
from tqdm import tqdm

BASE_LINK = "https://www.bilkatogo.dk"
df1 = pd.DataFrame(columns=["descriptions"])



def get_product_description(link):
    product_descriptions = []
    #for link in product_links:
    url = BASE_LINK + link  
    
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    options.add_argument('headless')  # To run Edge in headless mode

    driver = webdriver.Edge(options=options)

    # Load the webpage
    driver.get(url)
    
    # Wait for a few seconds to ensure JavaScript execution
    time.sleep(0.3)

    # Get the page source after JavaScript execution
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')

    description = soup.find('section', {'id' : 'content-description', 'class': 'content'}).text

    product_descriptions.append(description)
        
    return product_descriptions




if __name__ == "__main__":

    product_links = pd.read_csv('data\df_Salling_Products.csv', sep=";")["link"]

    results = Parallel(n_jobs=8)(delayed(get_product_description)(link) for link in tqdm(product_links[:10]))
    df1["descriptions"] = sum(results, [])

    df1.to_csv('df_Salling_Products_Descriptions.csv', sep=';')

    print(1)