import flet as ft
import requests
from bs4 import BeautifulSoup
import threading
import time


class PriceScraperApp(ft.Column):
    def __init__(self):
        super().__init__()
        self.running = False
        self.previous_price = None
        self.current_price = None
        self.previous_usd_index = None
        self.current_usd_index = None

    def build(self):
        self.switch = ft.Switch(on_change=self.toggle_scraping)
        self.price_text = ft.Text("19000.00", size=30, weight="bold")
        self.usd_index_text = ft.Text("104.305", size=30, weight="bold")

        dashboard_text = ft.Text(
            value='Dashboard',
            weight='BOLD',
            size=18,
        )

        price_container = ft.Container(
            padding=15,
            width=190,
            height=100,
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.with_opacity(0.04, 'WHITE'),
            border_radius=ft.border_radius.all(5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                tight=True,
                spacing=-30,
                controls=[
                    ft.Text("Nasdaq100 Futures Today", size=10),
                    self.price_text,
                ]
            )
        )

        usd_index_container = ft.Container(
            padding=15,
            width=190,
            height=100,
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.with_opacity(0.04, 'WHITE'),
            border_radius=ft.border_radius.all(5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                tight=True,
                spacing=-30,
                controls=[
                    ft.Text("US Dollar Index Today", size=10),
                    self.usd_index_text,
                ]
            )
        )

        return ft.Column([
            ft.Row([
                dashboard_text,
                self.switch
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                price_container,
                usd_index_container
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], alignment=ft.MainAxisAlignment.CENTER)

    def toggle_scraping(self, e):
        self.running = e.control.value
        if self.running:
            self.start_scraping()
        else:
            self.stop_scraping()

    def start_scraping(self):
        self.running = True
        self.update()
        self.scraping_thread = threading.Thread(target=self.scrape_prices, daemon=True)
        self.scraping_thread.start()

    def stop_scraping(self):
        self.running = False
        self.update()

    def scrape_prices(self):
        nasdaq_url = "https://www.investing.com/indices/nq-100-futures?cid=1175151"
        usd_index_url = "https://www.investing.com/currencies/us-dollar-index"
        while self.running:
            try:
                nasdaq_price = self.scrape_price(nasdaq_url, 'div', {'data-test': 'instrument-price-last'})
                usd_index = self.scrape_price(usd_index_url, 'span', {'class': 'arial_26 inlineblock pid-8827-last'})

                if nasdaq_price is not None:
                    self.current_price = nasdaq_price
                    self.update_price_text(self.price_text, self.current_price, self.previous_price)
                    self.previous_price = self.current_price

                if usd_index is not None:
                    self.current_usd_index = usd_index
                    self.update_price_text(self.usd_index_text, self.current_usd_index, self.previous_usd_index)
                    self.previous_usd_index = self.current_usd_index

                time.sleep(1)  # Add a short delay between requests
            except requests.RequestException as e:
                print(f"Error fetching data: {e}")
                time.sleep(5)  # Wait longer before retrying after an error
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(5)

    def scrape_price(self, url, tag, attrs):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            price_element = soup.find(tag, attrs)
            if price_element:
                price = price_element.text.strip()
                return float(price.replace(',', ''))
            else:
                print(f"Price element not found in the HTML at {url}.")
                return None
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return None

    def update_price_text(self, text_control, current_value, previous_value):
        if previous_value is not None:
            if current_value > previous_value:
                color = ft.colors.GREEN
            else:
                color = ft.colors.RED
        else:
            color = ft.colors.BLACK

        text_control.value = f"{current_value:.2f}"
        text_control.color = color
        self.update()

