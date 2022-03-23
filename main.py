from bs4 import BeautifulSoup
import requests
import re
import GPU_detail
url = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294808776&myStore=false&storeid=101&rpp=96"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def get_html(url: str):
    page = requests.get(url, headers=headers).text
    return BeautifulSoup(page, "html.parser")

def get_html_titles(doc: BeautifulSoup):
    titles = []
    details = doc.find_all(class_ = "detail_wrapper")
    for detail in details:
        titles.append(detail.find("a").string)
    return titles

def get_html_prices(doc: BeautifulSoup):
    prices = []
    tags = doc.find_all(text="$")
    for tag in tags:
        prices.append(float(tag.parent.parent.text.replace(",","").strip("$")))
    return prices

def get_html_stocks(doc: BeautifulSoup):
    stocks = []
    tags = doc.find_all(class_ = "stock")
    for tag in tags:
        text = tag.text.replace("IN STOCK", "").replace("SOLD OUT", "").replace("at Tustin Store", "").replace("+", "").strip()
        if len(text) > 0:
            stocks.append(int(text))
        else:
            stocks.append(int(0))
    return stocks
        
def setup_products():
    new_products = []
    html = get_html(url)
    titles = get_html_titles(html)
    prices = get_html_prices(html)
    stocks = get_html_stocks(html)
    if (len(titles) == len(prices) and len(prices) == len(stocks)):
        for i in range(len(titles)):
            new_products.append(GPU_detail.GPU(title=titles[i], price=prices[i], stock=stocks[i]))
    return new_products


def main():
    products = setup_products()
    for product in products:
        print(product.string())

if __name__ == "__main__":
    main()