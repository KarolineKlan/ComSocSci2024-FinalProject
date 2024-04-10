import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def catagory(string : str, options=False) -> str:
    """
    input : 'food-waste' or 'prod-sug' or 'stores' or 'holidays' or 'jobs'

    output : RESOURCE URL to be added to the base-url : 'https://api.sallinggroup.com/'

    If using product sugestions the options can either be: 'relevant-products, similar-products or frequently-bought-together'
    """
    if str(string) == 'food-waste':
        RESOURCE = 'v1/food-waste'
    elif str(string) == 'prod-sug':
        RESOURCE = 'v1-beta/product-suggestions'
        if options:
            RESOURCE = f'v1-beta/product-suggestions/{options}'
    elif str(string) == 'stores':
        RESOURCE = 'v2/stores'
    elif str(string) == 'holidays':
        RESOURCE = 'v1/holidays'
    elif str(string) == 'jobs':
        RESOURCE = 'v1/jobs'
    return RESOURCE

url = "https://api.sallinggroup.com"
version = "v1-beta"
recourses = "product-suggestions/frequently-bought-together"
PARAMETERS = {
    "productId" : "93019"
}


API_LINK = f"{url}/{version}/{recourses}"

response = requests.get(API_LINK, params = PARAMETERS, auth=BearerAuth("0f24d6b5-a7e3-4319-bfce-e1cfe057ad1c"))
results = requests.get(API_LINK, params = PARAMETERS, auth=BearerAuth("0f24d6b5-a7e3-4319-bfce-e1cfe057ad1c")).json()
#total_entities = response.headers["X-Total-Count"]

print(1)