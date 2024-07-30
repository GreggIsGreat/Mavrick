import threading
import time
import requests
from bs4 import BeautifulSoup
import flet as ft


class WebScraper(ft.Column):
    def __init__(self):
        super().__init__()
        self.scraping_thread = None
        self.keep_scraping = False
        self.switch = ft.Switch(value=False, on_change=self.toggle_scraping)
        self.price_text = ft.Text("XRPUSD Price: ", color="WHITE")

    def toggle_scraping(self, e):
        if self.switch.value:
            self.start_scraping()
        else:
            self.stop_scraping()

    def start_scraping(self):
        self.keep_scraping = True
        self.scraping_thread = threading.Thread(target=self.fetch_and_update_price)
        self.scraping_thread.start()

    def stop_scraping(self):
        self.keep_scraping = False
        if self.scraping_thread:
            self.scraping_thread.join()

    def fetch_and_update_price(self):
        url = "https://finance.yahoo.com/quote/XRP-USD/"
        headers = {"User-Agent": "Mozilla/5.0"}
        previous_price = None

        while self.keep_scraping:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                price_element = soup.find('fin-streamer', {'data-testid': 'qsp-price'})
                if price_element:
                    current_price = float(price_element['data-value'])
                    if previous_price is not None:
                        if current_price > previous_price:
                            self.price_text.color = "GREEN"
                        elif current_price < previous_price:
                            self.price_text.color = "RED"
                        else:
                            self.price_text.color = "WHITE"
                        self.price_text.value = f"XRPUSD Price: {current_price}"
                        self.update()
                    previous_price = current_price
            time.sleep(5)  # Add a sleep interval to prevent constant requests

    def build(self):
        return ft.Column(
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("Web Scraper"),
                            self.switch
                        ]
                    )
                ),
                self.price_text
            ]
        )