from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

'''
    Future Updates:
    - Improve Amazon Scraper (fixe status code 503 issue)
    - Add Target, B&H, PC Richard & Son
    - Add more detailed pricing information (monthly payments, sale active, etc.)
'''

app = Flask(__name__)
CORS(app)

custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'accept-language': 'en-US,en;q=0.9'
}
@app.route("/scrape")
def scrape():
    search = request.args.get("search")
    return jsonify({'data': [scrape_best_buy(search), scrape_microcenter(search), scrape_newegg(search), scrape_walmart(search), scrape_ebay(search)]})

def scrape_amazon(search):
    req = requests.get('https://www.amazon.com/s?k=' + search + '&crid=N4J2WV0PZU5F&sprefix=' + search + '%2Caps%2C229&ref=nb_sb_noss_1', headers=custom_headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find_all(attrs={"data-component-type": "s-search-result"})
        product_information = []
        for index in range(0,10):
            try:
                title = results[index].find(class_="a-size-medium").text
                price = results[index].find(class_="a-offscreen").text
                link = "amazon.com" + results[index].find(class_="a-link-normal")["href"]
                product_information.append({"title" : title, "price": price, "link": link})
            except IndexError:
                break
            except AttributeError:
                continue
        return {'store': 'Amazon', 'products': product_information}
    else:
        return {"status code": req.status_code}
    
def scrape_best_buy(search):
    req = requests.get('https://www.bestbuy.com/site/searchpage.jsp?st='+ search + '+&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys', headers=custom_headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find_all(class_="sku-item")
        product_information = []
        for index in range(0,10):
            try:
                title = results[index].find(class_="sku-title").text
                price = results[index].find(attrs={"data-testid": "customer-price"}).text[:results[index].find(attrs={"data-testid": "customer-price"}).text.find("Y")]
                link = "https://bestbuy.com/" + results[index].find(class_="sku-title").find("a")['href'][1:]
                product_information.append({"title" : title, "price": price, "link": link})
            except IndexError:
                break
            except AttributeError:
                continue
        return {'store': 'Best Buy', 'products': product_information}
    else:
        return {"status code": req.status_code}
    
def scrape_walmart(search):
    req = requests.get('https://www.walmart.com/search?q=' + search, headers=custom_headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find_all(attrs={"role": "group"})
        product_information = []
        for index in range(0,10):
            try:
                title = results[index].find("a").text
                price = "$" + results[index].find(class_="f2").text + ".00"
                link = results[index].find("a")['href']  if 'walmart' in results[index].find("a")['href'] else 'https://walmart.com' + results[index].find("a")['href']
                product_information.append({"title" : title, "price": price, "link": link})
            except IndexError:
                break
            except AttributeError:
                continue
        return {'store': 'Walmart', 'products': product_information}
    else:
        return {"status code": req.status_code}
    
def scrape_newegg(search):
    req = requests.get('https://www.newegg.com/p/pl?d=' + search, headers=custom_headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find_all(class_="item-container")
        product_information = []
        for index in range(0,10):
            try:
                title = results[index].find(class_='item-title').text
                price = results[index].find(class_="price-current").text[:results[index].find(class_="price-current").text.find("\u00a0")]
                link = results[index].find(class_='item-title')['href']
                product_information.append({"title" : title, "price": price, "link": link})
            except IndexError:
                break
            except AttributeError:
                continue
        return {'store': 'Newegg', 'products': product_information}
    else:
        return {"status code": req.status_code}
    
def scrape_microcenter(search):
    req = requests.get('https://www.microcenter.com/search/search_results.aspx?N=&cat=&Ntt='+ search + '&searchButton=search', headers=custom_headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find_all('li', class_="product_wrapper")
        product_information = []
        for index in range(0,10):
            try:
                title = results[index].find(class_='productClickItemV2')['data-name']
                price = results[index].find(attrs={"itemprop":"price"}).text[results[index].find(attrs={"itemprop":"price"}).text.find("$"):]
                link = 'https://microcenter.com' + results[index].find(class_='productClickItemV2')['href']
                product_information.append({"title" : title, "price": price, "link": link})
            except IndexError:
                break
            except AttributeError:
                continue
        return {'store': 'Microcenter', 'products': product_information}
    else:
        return {"status code": req.status_code}
    
def scrape_ebay(search):
    req = requests.get('https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + search +'&_sacat=0')
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, "html.parser")
        results = soup.find_all('div', class_="s-item__info")
        product_information = []
        for index in range(2,12):
            try:
                title = results[index].find(class_='s-item__title').text
                price = results[index].find(class_='s-item__price').text
                link = results[index].find(class_='s-item__link')['href']
                product_information.append({"title" : title, "price": price, "link": link})
            except IndexError:
                break
            except AttributeError:
                continue
        return {'store': 'Ebay', 'products': product_information}
    else:
        return {"status code": req.status_code}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)