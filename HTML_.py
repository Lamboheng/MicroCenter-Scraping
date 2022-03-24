from bs4 import BeautifulSoup
import requests

DEFAULT_URL = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294808776&myStore=false&storeid=101&rpp=96"
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