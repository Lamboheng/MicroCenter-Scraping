import sys
import os.path
import json
from datetime import datetime
from datetime import timedelta

import HTML_
import GPU_
import Email_

DEFAULT_RECORD_NAME = "records.json"
GPU_GOAL_PRICE = {
    '3090 Ti': 0.0,
    '3090': 0.0,
    '3080 Ti': 0.0,
    '3080': 800.0,
    '3070 Ti': 700.0,
    '3070': 600.0,
    '3060 Ti': 0.0,
    '3060': 0.0,
    '3050 Ti': 0.0,
    '3050': 0.0
}

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
    changed = False
    changed_text = []
    if (len(titles) == len(prices) and len(prices) == len(stocks) and len(stocks) == len(SKUs) and len(SKUs) == len(links)):
        for i in range(len(titles)):
            found = False
            for product in products:
                if product.get_SKU() == SKUs[i]:
                    found = True
                    if product.get_title() != titles[i]:
                        changed = True
                        product.set_title(titles[i])
                        product.find_model()
                        product.find_memorySize()
                        product.find_brand()
                    if product.get_link() != links[i]:
                        changed = True
                        product.set_link(links[i])
                    if product.get_price() != float(prices[i]):
                        changed = True
                        changed_text.append(f"{product.get_brand()} {product.get_model()} price from {str(product.get_price())} to {str(float(prices[i]))}")
                        product.set_price(float(prices[i]))
                    if product.get_stock() != int(stocks[i]):
                        changed = True
                        changed_text.append(f"{product.get_brand()} {product.get_model()} stock from {str(product.get_stock())} to {str(int(stocks[i]))}")
                        product.set_stock(int(stocks[i]))
                    break
            if found == False:
                products.append(GPU_.GPU(title=titles[i], price=prices[i], stock=stocks[i], SKU=SKUs[i], link=links[i]))
    return changed, changed_text
            
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
    if os.path.exists(DEFAULT_RECORD_NAME):
        with open(DEFAULT_RECORD_NAME, "r") as f:
            datas = json.load(f)
        datas[product.get_SKU()]["price"] = product.get_price()
        datas[product.get_SKU()]["price_records"].append({datetime.now().strftime("%m/%d/%Y %H:%M:%S"): product.get_price()})
        with open(DEFAULT_RECORD_NAME, "w") as f:
            json.dump(datas, f, indent=2)
    
def json_update_stock(product: GPU_.GPU):
    if os.path.exists(DEFAULT_RECORD_NAME):
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

def send_email_at_goal(products: GPU_.GPU):
    lowest = sys.float_info.max
    found = False
    lowest_product = products[0]
    result_product = []
    sent = False;
    for i in range(len(GPU_.GPU_MODELS)):
        for product in products:
            if product.get_model() == GPU_.GPU_MODELS[i] and product.get_stock() > 0 and product.get_price() < lowest:
                found = True
                lowest = product.get_price()
                lowest_product = product
        if found and lowest < GPU_GOAL_PRICE[GPU_.GPU_MODELS[i]]:
            sent = True
            result_product.append(lowest_product)
            Email_.send_email(lowest_product)
            GPU_GOAL_PRICE[lowest_product.get_model()] -= 100
        lowest = sys.float_info.max
        found = False
    return sent, result_product

def find_lowest_highest(products: GPU_.GPU):
    lowest_price = {}
    highest_price = {}
    for model in GPU_.GPU_MODELS:
        lowest_price[model] = sys.float_info.max
        highest_price[model] = 0.0
    for product in products:
        if (lowest_price[product.model] > product.price):
            lowest_price[product.model] = product.price
        if (highest_price[product.model] < product.price):
            highest_price[product.model] = product.price
            
    return lowest_price, highest_price

def clear_json_file():
    if os.path.exists(DEFAULT_RECORD_NAME):
        with open(DEFAULT_RECORD_NAME, "r") as f:
            datas = json.load(f)
            
        before_date = "01/01/1990 00:00:00"
        for data in datas:
            before_date = "01/01/1990 00:00:00"
            i = 0
            while i < len(datas[data]['stock_records']):
                for date_str in datas[data]['stock_records'][i]:
                    date = datetime.strptime(date_str, "%m/%d/%Y %H:%M:%S")
                if date < datetime.strptime(before_date, "%m/%d/%Y %H:%M:%S") + timedelta(minutes=5):
                    datas[data]['stock_records'].pop(i-1)
                    before_date = date_str
                else:
                    before_date = date_str
                    i += 1

        with open(DEFAULT_RECORD_NAME, 'w') as f:
            json.dump(datas, f, indent=2)
