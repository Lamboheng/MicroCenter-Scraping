import sys
import os.path
import json
from datetime import datetime

import HTML_
import GPU_

DEFAULT_RECORD_NAME = "records.json"

## if records.json is exists, load json to products
## if not, reload from the website
def setup_products(products: GPU_.GPU):
    html = HTML_.get_html(HTML_.DEFAULT_URL)
    titles = HTML_.get_html_titles(html)
    prices = HTML_.get_html_prices(html)
    stocks = HTML_.get_html_stocks(html)
    SKUs = HTML_.get_html_SKU(html)
    links = HTML_.get_html_link(html)
    if (len(titles) == len(prices) and len(prices) == len(stocks) and len(stocks) == len(SKUs) and len(SKUs) == len(links)):
        for i in range(len(titles)):
            products.append(GPU_.GPU(title=titles[i], price=prices[i], stock=stocks[i], SKU=SKUs[i], link=links[i]))

def update_products(products: GPU_.GPU):
    html = HTML_.get_html(HTML_.DEFAULT_URL)
    titles = HTML_.get_html_titles(html)
    prices = HTML_.get_html_prices(html)
    stocks = HTML_.get_html_stocks(html)
    SKUs = HTML_.get_html_SKU(html)
    links = HTML_.get_html_link(html)
    if (len(titles) == len(prices) and len(prices) == len(stocks) and len(stocks) == len(SKUs) and len(SKUs) == len(links)):
        for product in products:
            found = False
            for i in range(len(titles)):
                if product.get_SKU() == SKUs[i]:
                    found = True
                    if product.get_title() != titles[i]:
                        product.set_title(titles[i])
                        product.find_model()
                        product.find_memorySize()
                        product.find_brand()
                    product.set_link(links[i])
                    product.set_price(float(prices[i]))
                    product.set_stock(int(stocks[i]))
                    break
            if found == False:
                products.append(GPU_.GPU(title=titles[i], price=prices[i], stock=stocks[i], SKU=SKUs[i], link=links[i]))
            
def update_json(products: GPU_.GPU):
    if os.path.exists(DEFAULT_RECORD_NAME):
        with open(DEFAULT_RECORD_NAME, "r") as f:
            datas = json.load(f)
        json_match_products(datas, products)
        with open(DEFAULT_RECORD_NAME, "w") as f:
            json.dump(datas, f, indent=2)
    else:
        with open(DEFAULT_RECORD_NAME, "w") as f:
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
        
## match data from products to json
def json_match_products(datas, products: GPU_.GPU):
    for product in products:
        if product.get_SKU() in datas.keys():
            datas[product.get_SKU()]["title"] = product.get_title()
            datas[product.get_SKU()]["model"] = product.get_model()
            datas[product.get_SKU()]["brand"] = product.get_brand()
            datas[product.get_SKU()]["memorySize"] = product.get_memorySize()
            datas[product.get_SKU()]["SKU"] = product.get_SKU()
            datas[product.get_SKU()]["link"] = product.get_link()
            
            if datas[product.get_SKU()]["price"] != product.get_price():
                datas[product.get_SKU()]["price_records"].append({datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_price()})
                datas[product.get_SKU()]["price"] = product.get_price()
            if datas[product.get_SKU()]["stock"] != product.get_stock():
                datas[product.get_SKU()]["stock_records"].append({datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_stock()})
                datas[product.get_SKU()]["stock"] = product.get_stock()
        else:
            datas[product.get_SKU()] = {
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
        
def json_update_price(product: GPU_.GPU):
    with open(DEFAULT_RECORD_NAME, "r") as f:
        datas = json.load(f)
    datas[product.get_SKU()]["price"] = product.get_price()
    datas[product.get_SKU()]["price_records"].append({datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_price()})
    with open(DEFAULT_RECORD_NAME, "w") as f:
        json.dump(datas, f, indent=2)
    
def json_update_stock(product: GPU_.GPU):
    with open(DEFAULT_RECORD_NAME, "r") as f:
        datas = json.load(f)
    datas[product.get_SKU()]["stock"] = product.get_stock()
    datas[product.get_SKU()]["stock_records"].append({datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_stock()})
    with open(DEFAULT_RECORD_NAME, "w") as f:
        json.dump(datas, f, indent=2)

def products_str(products: GPU_.GPU):
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
    string = ""
    for i in range(len(GPU_.GPU_MODELS)):
        if GPU_.GPU_MODELS[i] not in products_lowest_price.keys():
            continue
        string += "\x1b[91m" + (str(products_highest_price[GPU_.GPU_MODELS[i]])).rjust(8) + " \x1b[34m<- " "\x1b[93m" + (GPU_.GPU_MODELS[i]).ljust(8) + "\x1b[34m-> \x1b[92m" + str(products_lowest_price[GPU_.GPU_MODELS[i]]) + "\n"
    return string
