import flet as ft
import requests
from bs4 import BeautifulSoup
import threading
import time


class PriceScraperApp(ft.Column):
    # Constants
    NASDAQ_URL = "https://www.investing.com/indices/nq-100-futures?cid=1175151"
    USD_INDEX_URL = "https://www.investing.com/currencies/us-dollar-index"
    CONTAINER_WIDTH = 190
    CONTAINER_HEIGHT = 100
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.previous_price = self.current_price = None
        self.previous_usd_index = self.current_usd_index = None
        
        # Initialize UI elements
        self.switch = ft.Switch(
            on_change=self.toggle_scraping, 
            active_track_color="BLUE900", 
            active_color="WHITE"
        )
        self.price_text = ft.Text("0", size=30, weight="bold")
        self.usd_index_text = ft.Text("0", size=30, weight="bold")
        
        # Build UI
        self.controls = self.build()

    def build(self):
        dashboard_header = ft.Row([
            ft.Text('Dashboard', weight='BOLD', size=18),
            self.switch
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        price_container = self._create_metric_container(
            "Nasdaq100 Futures Today", 
            self.price_text
        )
        
        usd_index_container = self._create_metric_container(
            "US Dollar Index Today", 
            self.usd_index_text
        )
        
        metrics_row = ft.Row(
            [price_container, usd_index_container],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        return [dashboard_header, metrics_row]

    def _create_metric_container(self, title, value_control):
        """Helper method to create consistent metric containers"""
        return ft.Container(
            padding=15,
            width=self.CONTAINER_WIDTH,
            height=self.CONTAINER_HEIGHT,
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.with_opacity(0.04, 'WHITE'),
            border_radius=ft.border_radius.all(5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                tight=True,
                spacing=-30,
                controls=[
                    ft.Text(title, size=10),
                    value_control,
                ]
            )
        )

    def toggle_scraping(self, e):
        self.running = e.control.value
        if self.running:
            threading.Thread(target=self.scrape_prices, daemon=True).start()
        self.update()

    def scrape_prices(self):
        while self.running:
            try:
                # Scrape both prices in parallel
                nasdaq_price = self.scrape_price(
                    self.NASDAQ_URL, 
                    'div', 
                    {'data-test': 'instrument-price-last'}
                )
                usd_index = self.scrape_price(
                    self.USD_INDEX_URL, 
                    'span', 
                    {'class': 'arial_26 inlineblock pid-8827-last'}
                )

                # Update UI with new values if available
                if nasdaq_price:
                    self.update_price_text(self.price_text, nasdaq_price, self.previous_price)
                    self.previous_price = nasdaq_price

                if usd_index:
                    self.update_price_text(self.usd_index_text, usd_index, self.previous_usd_index)
                    self.previous_usd_index = usd_index

                time.sleep(1)
            except Exception as e:
                print(f"Error during scraping: {e}")
                time.sleep(5)

    def scrape_price(self, url, tag, attrs):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            element = soup.find(tag, attrs)
            return float(element.text.strip().replace(',', '')) if element else None
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def update_price_text(self, text_control, current_value, previous_value):
        color = ft.colors.BLUE
        if previous_value is not None:
            color = ft.colors.GREEN if current_value > previous_value else ft.colors.RED
            
        text_control.value = f"{current_value:.2f}"
        text_control.color = color
        self.update()
