import requests
from bs4 import BeautifulSoup

# List of major retailers and their search URLs
RETAILERS = {
    "Amazon": "https://www.amazon.com/s?k=",
    "Walmart": "https://www.walmart.com/search/?query=",
    "Target": "https://www.target.com/s?searchTerm=",
    "Lego": "https://www.lego.com/en-us/search?q=",
    "Kohls": "https://www.kohls.com/search.jsp?search=",
    "BestBuy": "https://www.bestbuy.com/site/searchpage.jsp?st="
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def get_price_amazon(lego_id):
    search_url = RETAILERS["Amazon"] + lego_id
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find("span", {"class": "a-offscreen"})
    return price.text if price else "Price not found"

def get_price_walmart(lego_id):
    search_url = RETAILERS["Walmart"] + lego_id
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find("span", {"class": "price-characteristic"})
    return price.text if price else "Price not found"

def get_price_target(lego_id):
    search_url = RETAILERS["Target"] + lego_id
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find("span", {"data-test": "product-price"})
    return price.text if price else "Price not found"

def get_price_lego(lego_id):
    search_url = RETAILERS["Lego"] + lego_id
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find("span", {"class": "ProductPrice-module__srOnly___2UGDM"})
    return price.text if price else "Price not found"

def get_price_kohls(lego_id):
    search_url = RETAILERS["Kohls"] + lego_id
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find("span", {"class": "prod_price_amount"})
    return price.text if price else "Price not found"

def get_price_bestbuy(lego_id):
    search_url = RETAILERS["BestBuy"] + lego_id
    response = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    price = soup.find("div", {"class": "priceView-hero-price priceView-customer-price"})
    return price.text if price else "Price not found"

def get_lego_price(lego_id):
    prices = {}
    prices["Amazon"] = get_price_amazon(lego_id)
    prices["Walmart"] = get_price_walmart(lego_id)
    prices["Target"] = get_price_target(lego_id)
    prices["Lego"] = get_price_lego(lego_id)
    prices["Kohls"] = get_price_kohls(lego_id)
    prices["BestBuy"] = get_price_bestbuy(lego_id)
    return prices

if __name__ == "__main__":
    lego_id = input("Enter Lego Product ID: ")
    prices = get_lego_price(lego_id)
    for retailer, price in prices.items():
        print(f"{retailer}: {price}")
