from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from tqdm import tqdm
from joblib import Parallel, delayed

BASE_LINK = "https://www.bilkatogo.dk"

def extract_products(url, category_list):

    products_df = pd.DataFrame(columns=['product_id', 'name', 'price', 'link', 'category'])
    
    for category in tqdm(category_list):
        page_counter = 0
        
        SCRAPE_LINK = f"{url}/{category}"   # Construct the URL for the first case with no page number
        product_card_containers = ["dummy"]
        
        while len(product_card_containers) != 0:
            print("The length of product_card_containers is: ", len(product_card_containers))
            print("The page counter is: ", page_counter)
            
            # Initialize Edge WebDriver
            options = webdriver.EdgeOptions()
            options.use_chromium = True
            options.add_argument('headless')  # To run Edge in headless mode
            driver = webdriver.Edge(options=options)

            # Load the webpage
            driver.get(SCRAPE_LINK)

            # Wait for a few seconds to ensure JavaScript execution
            time.sleep(0.5)

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
            for product in product_card_containers:
                if product == 'dummy':
                    continue
                product_info = product.find('div')
                product_id = product_info.attrs['data-productid']
                product_name = product_info.contents[0]['aria-label']
                product_link = product_info.contents[0]['href']


                prod_price = product_info.find('div', {'class' : 'row product-description flex-column'})
                produc_price = prod_price.find('p', {'class' : 'description'})

                ### Added a logic for 'drikkevarer' as the category doesn't have the same price format as the others and follows a slight random pattern when displaying the price ###
                if category == "drikkevarer/":
                    for span in produc_price.find_all('span'):
                        if "/L." in span.text:
                            product_kg_price = span.string
                else:
                    product_kg_price = produc_price.find_all('span')[-1].string     # Extract the kg./stk. price from the product. Sufficient for all categories except 'drikkevarer'
            
                #price = [int(s) for s in test.split() if s.isdigit()]
                new_row = {'product_id' : product_id, 'name' : product_name, 'link' : product_link, 'price' : product_kg_price, 'category' : category}
                products_df.loc[len(products_df)] = new_row
            
            page_counter += 1
            SCRAPE_LINK = f"{url}/{category}/?page={page_counter}"
        
    return products_df
    





if __name__ == "__main__":
    LINK = "https://www.bilkatogo.dk/kategori/"
    categories = ["frugt-og-groent/", "koed-og-fisk/", "mejeri-og-koel/", "drikkevarer/", "broed-og-kager/", "kolonial/", "slik-og-snacks/", "frost/", "kiosk/", "dyremad/", "husholdning/",
                   "personlig-pleje/", "baby-og-boern/", "bolig-og-koekken/", "fritid-og-sport/", "toej-og-sko/", "elektronik/", "have/", "leg/", "biludstyr/", "byggemarked/"]


    prods = extract_products(LINK, ["drikkevarer/"])
    print(1)

