import requests
from bs4 import BeautifulSoup


def fetch_and_update_price():
    url = "https://finance.yahoo.com/quote/XRP-USD/"
    headers = {"User-Agent": "Mozilla/5.0"}
    previous_price = None

    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            price_element = soup.find('fin-streamer', {'data-testid': 'qsp-price'})
            if price_element:
                current_price = price_element['data-value']
                if current_price != previous_price:
                    print(f"\rXRPUSD Price: {current_price}", end="")
                    previous_price = current_price


fetch_and_update_price()
