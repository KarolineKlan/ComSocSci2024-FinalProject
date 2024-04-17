import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
from joblib import Parallel, delayed
from tqdm import tqdm

BASE_LINK = "https://www.bilkatogo.dk"
df1 = pd.DataFrame(columns=["p_id", "descriptions"])



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
    time.sleep(2)

    # Get the page source after JavaScript execution
    page_source = driver.page_source

    # Close the WebDriver
    driver.quit()

    # Parse the HTML content
    soup = BeautifulSoup(page_source, 'html.parser')
    try:
        description = soup.find('section', {'id' : 'content-description', 'class': 'content'})
        a = description.find("h2")
        if a != None:
            description = ''.join([str(tag) for tag in reversed(list(description.h2.previous_siblings)) if tag.name != 'h2'])
            description = description.replace("<br/><br/>","")
        else:
            description = description.text
    except AttributeError:
        description = "No description available"

    product_descriptions.append(description)

    return product_descriptions




if __name__ == "__main__":
    products = pd.read_csv('data/df_clean_data.csv', sep=";")
    product_links = products["link"]
    product_id = products["product_id"]


    for i in tqdm(range(len(pd.read_csv('data\df_Salling_Products_Descriptions_CLEANED.csv', sep=";")), len(product_links), 14)):

        results = Parallel(n_jobs=14)(delayed(get_product_description)(link) for link in product_links[i:i+14])

        df1['p_id'] = list(product_id[i:i+14])
        df1["descriptions"] = sum(results, [])
        df1.to_csv('data/df_Salling_Products_Descriptions_CLEANED.csv', sep=';', mode='a', index=False, header=False)

    print(1)