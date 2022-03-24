import sys
import GPU_
import HTML_

def setup_products(products: GPU_.GPU):
    html = HTML_.get_html(HTML_.DEFAULT_URL)
    titles = HTML_.get_html_titles(html)
    prices = HTML_.get_html_prices(html)
    stocks = HTML_.get_html_stocks(html)
    if (len(titles) == len(prices) and len(prices) == len(stocks)):
        for i in range(len(titles)):
            products.append(GPU_.GPU(title=titles[i], price=prices[i], stock=stocks[i]))

def main():
    products = []
    setup_products(products)
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

if __name__ == "__main__":
    main()