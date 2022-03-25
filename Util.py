import sys
import os.path
import json
from datetime import datetime

import HTML_
import GPU_

## if records.json is exists, load json to products
## if not, reload from the website
def setup_products(products: GPU_.GPU):
    if os.path.exists('records.json'):
        with open('records.json', "r") as f:
            print("hi")
    else:
        html = HTML_.get_html(HTML_.DEFAULT_URL)
        titles = HTML_.get_html_titles(html)
        prices = HTML_.get_html_prices(html)
        stocks = HTML_.get_html_stocks(html)
        SKUs = HTML_.get_html_SKU(html)
        links = HTML_.get_html_link(html)
        if (len(titles) == len(prices) and len(prices) == len(stocks) and len(stocks) == len(SKUs) and len(SKUs) == len(links)):
            for i in range(len(titles)):
                products.append(GPU_.GPU(title=titles[i], price=prices[i], stock=stocks[i], SKU=SKUs[i], link=links[i]))
        with open("test.json", "w") as f:
            json.dump(products_to_json(products), f, indent=2)

def products_to_json(products: GPU_.GPU):
    data = {}
    for product in products:
        data[product.get_SKU()] = {
            "title" : product.get_title(),
            "model" : product.get_model(),
            "brand" : product.get_brand(),
            "price" : product.get_price(),
            "stock" : product.get_stock(),
            "memorySize": product.get_memorySize(),
            "SKU" : product.get_SKU(),
            "link" : product.get_link(),
            "price_records" : [
                {datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_price()}
            ],
            "stock_records" : [
                {datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_stock()}
            ]
        }
    return data
        

# def json_to_products(json_: json):
#     for i in json_:
        

def print_products(products: GPU_.GPU):
    products_lowest_price = {
        "3090": sys.float_info.max, 
        "3080 Ti": sys.float_info.max, 
        "3080": sys.float_info.max, 
        "3070 Ti": sys.float_info.max, 
        "3070": sys.float_info.max, 
        "3060 Ti": sys.float_info.max, 
        "3060": sys.float_info.max, 
        "3050": sys.float_info.max
    }
    products_highest_price = {
        "3090": 0.0, 
        "3080 Ti": 0.0, 
        "3080": 0.0, 
        "3070 Ti": 0.0, 
        "3070": 0.0, 
        "3060 Ti": 0.0, 
        "3060": 0.0, 
        "3050": 0.0
    }
    
    for product in products:
        if (products_lowest_price[product.model] > product.price):
            products_lowest_price[product.model] = product.price
        if (products_highest_price[product.model] < product.price):
            products_highest_price[product.model] = product.price
            
    for i in range(len(GPU_.GPU_MODELS)):
        if GPU_.GPU_MODELS[i] not in products_lowest_price.keys():
            continue
        print("\x1b[93m" + (GPU_.GPU_MODELS[i] + ":").ljust(8) + "\x1b[91m" + (str(products_highest_price[GPU_.GPU_MODELS[i]])).rjust(8) + " \x1b[34m<--> \x1b[92m" + str(products_lowest_price[GPU_.GPU_MODELS[i]]))
