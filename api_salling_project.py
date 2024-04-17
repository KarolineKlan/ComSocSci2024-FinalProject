import requests
import pandas as pd
from joblib import Parallel, delayed
from tqdm import tqdm
import time

df2 = pd.read_csv("data/df_Salling_Products_outer_categories.csv", sep=";")
df2 = list(df2.loc[df2["outer_category"] == "Foods"]["product_id"])

bearer_token = "6656b12a-84c5-48df-a174-4b3c1cd38614"

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

df_neighbor = pd.DataFrame(columns=["product_id", "neighbor_products_id"])

def get_neighbours(product_id):
    neighbour_id = []
    url = "https://api.sallinggroup.com"
    version = "v1-beta"
    recourses = "product-suggestions/frequently-bought-together"
    PARAMETERS = {
        "productId" : f"{product_id}"
    }

    API_LINK = f"{url}/{version}/{recourses}"

    results = requests.get(API_LINK, params = PARAMETERS, auth=BearerAuth(bearer_token)).json()
    
    for neighbours in results:
        try:
            neighbour_id.append(int(neighbours['prod_id']))
        except:
            print("Error")
            if results['statusCode'] == 429:
                print("Sleeping the code... Error 429")
                time.sleep(20)
        # # except TypeError:
        # #     print("Sleeping the code... Error 429")
        # #     print(results['error'])
        # #     time.sleep(10)
        # except KeyError:
        #     neighbour_id.append('No product available')

    return neighbour_id
    
#total_entities = response.headers["X-Total-Count"]



if __name__ == "__main__":
    
    get_neighbours(49856)
    
    time_step = 4
    
    for i in tqdm(range(len(pd.read_csv("data/df_Salling_Products_Neighbours.csv", sep=";")), len(df2), time_step)):
        neighbor_list = []
        p_id_list = []
        time.sleep(time_step * 0.2)
        
        p_id_list.append(list(df2[i:i+time_step]))
    
        results = Parallel(n_jobs=time_step)(delayed(get_neighbours)(product_id) for product_id in df2[i:i+time_step])
        
        for neighbours in results:
            neighbor_list.append(neighbours)
            
        df_neighbor["product_id"] = sum(p_id_list, [])
        df_neighbor["neighbor_products_id"] = neighbor_list
        df_neighbor.to_csv('data/df_Salling_Products_Neighbours.csv', sep=';', mode='a', index=False, header=False)