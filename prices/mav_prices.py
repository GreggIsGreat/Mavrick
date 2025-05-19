import asyncio
import json
from datetime import datetime

import requests
from flet import *


class BaseInstrument(Column):
    """Base class for all financial instrument widgets."""
    
    def __init__(self, page, endpoints=None):
        super().__init__()
        self.page = page
        self.endpoints = endpoints or {}
        
        # Common text fields
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)
        
        # Common buttons
        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello, icon_color=colors.WHITE)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield, icon_color=colors.WHITE)
        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True, icon_color=colors.WHITE)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello, icon_color=colors.WHITE)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit, icon_color=colors.WHITE)
        
        # Common container for predictions
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=130,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),
        )

        # For history tracking (only implemented in USTECH100)
        self.predictions = []

    async def add_hello(self, e):
        """Fetch data from API and populate fields."""
        try:
            data = await self.fetch_data()
            self.populate_fields(data)
        except Exception as ex:
            print(f"Error fetching data: {ex}")

    async def fetch_data(self):
        """Fetch data from API - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement fetch_data()")

    def populate_fields(self, data):
        """Populate fields with data - can be overridden by subclasses."""
        if isinstance(data, dict):
            # Handle dictionary data
            self.low_field.value = data.get("daily_low") or data.get("Daily_Low", "")
            self.high_field.value = data.get("daily_high") or data.get("Daily_High", "")
            self.volume_field.value = data.get("volume") or data.get("Volume", "")
            self.open_field.value = data.get("open_price") or data.get("Open_Price", "")
        else:
            # Handle other data formats if needed
            pass
        self.update()

    def clear_textfield(self, e):
        """Clear all text fields."""
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        """Submit data to API for prediction."""
        try:
            data = self.prepare_data_for_submission()
            response = self.submit_data(data)

            if response.status_code == 200:
                prediction = self.extract_prediction(response)
                self.output_data(prediction)
                self.record_prediction(prediction)
                print(f"Data posted successfully! Prediction: {prediction}")
            else:
                print(f"Failed to post data. Response: {response.text}")
        except Exception as ex:
            print(f"Error submitting data: {ex}")

    def prepare_data_for_submission(self):
        """Prepare data for submission - can be overridden by subclasses."""
        format_value = lambda v: v.replace(',', '')
        volume = format_value(self.volume_field.value)
        volume = f"{float(volume) / 1000}k" if 'k' not in volume and float(volume) >= 1000 else volume

        return {
            "open_price": format_value(self.open_field.value),
            "daily_high": format_value(self.high_field.value),
            "daily_low": format_value(self.low_field.value),
            "volume": volume
        }

    def submit_data(self, data):
        """Submit data to API - to be implemented by subclasses."""
        if not self.endpoints.get("post"):
            raise NotImplementedError("No post endpoint defined")
        return requests.post(self.endpoints["post"], json=data)

    def extract_prediction(self, response):
        """Extract prediction from response - can be overridden by subclasses."""
        return response.json()

    def record_prediction(self, prediction):
        """Record prediction history - only used by some subclasses."""
        timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        self.predictions.append({
            "timestamp": timestamp,
            "prediction": str(prediction)
        })

    def output_data(self, data):
        """Display prediction results."""
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def history(self, e):
        """Show prediction history - only implemented in USTECH100."""
        history_controls = []
        for pred in reversed(self.predictions):  # Display most recent first
            history_controls.extend([
                Text(f"Date: {pred['timestamp']}", size=10),
                Text(f"Maverick: {pred['prediction']}", size=10),
                Divider(color="BLUE"),
            ])

        if not history_controls:
            history_controls = [Text("No predictions yet", size=10)]

        self.dialog = AlertDialog(
            modal=True,
            title=Text("My History", size=16),
            content=Container(
                height=200,
                width=300,
                content=Column(
                    scroll=ScrollMode.ALWAYS,
                    tight=True,
                    spacing=-5,
                    controls=history_controls
                )
            ),
            actions=[
                IconButton(icons.CLOSE, on_click=self.handle_close)
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=self.on_dismiss
        )

        # Show the AlertDialog
        e.page.dialog = self.dialog
        self.dialog.open = True
        e.page.update()

    def handle_close(self, e):
        """Handle dialog close button."""
        self.dialog.open = False
        e.page.update()

    def on_dismiss(self, e):
        """Handle dialog dismiss event."""
        e.page.add(Text("Modal dialog dismissed"))

    def build(self):
        """Build the UI."""
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=self.get_button_controls(),
                        ),
                    ),
                ],
            ),
            self.pred_container,
        ])
    
    def get_button_controls(self):
        """Get button controls - can be overridden by subclasses."""
        return [
            self.button_add,
            self.button_clear,
            self.button_disabled,
            self.button_refresh,
            self.button_submit,
        ]


class USTECH100(BaseInstrument):
    def __init__(self, page):
        super().__init__(page, endpoints={
            "get": "https://maverick-6nk0.onrender.com/getnas100",
            "post": "https://maverick-6nk0.onrender.com/post_nas100"
        })
        # Add history button which is unique to this class
        self.button_history = IconButton(icons.HISTORY_SHARP, on_click=self.history, icon_color=colors.WHITE)
    
    async def fetch_data(self):
        return requests.get(self.endpoints["get"]).json()
    
    def get_button_controls(self):
        return [
            self.button_add,
            self.button_clear,
            self.button_history,
            self.button_refresh,
            self.button_submit,
        ]


class US30(BaseInstrument):
    def __init__(self, page):
        super().__init__(page, endpoints={
            "get": "https://maverick-6nk0.onrender.com/getus30",
            "post": "https://maverick-6nk0.onrender.com/postus30"
        })
    
    async def fetch_data(self):
        return requests.get(self.endpoints["get"]).json()


class GER40(BaseInstrument):
    def __init__(self, page):
        super().__init__(page, endpoints={
            "get": "https://index-i.onrender.com/german40",
            "post": "https://index-i.onrender.com/ger30"
        })
    
    async def fetch_data(self):
        data = requests.get(self.endpoints["get"]).text
        open_price = data.split("Open: ")[1].split("\\n")[0]
        volume = data.split("Volume: ")[1].split("\\n")[0]
        low = data.split("Daily Low: ")[1].split("\\n")[0]
        high = data.split("Daily High: ")[1].split("\\n")[0]
        
        return {
            "open_price": open_price,
            "volume": volume,
            "daily_low": low,
            "daily_high": high
        }
    
    def prepare_data_for_submission(self):
        return {key: float(getattr(self, f"{key}_field").value.replace(',', '')) for key in
                ["open", "volume", "low", "high"]}
    
    def extract_prediction(self, response):
        return response.json()["prediction"]


class XAUUSD(BaseInstrument):
    def __init__(self, page):
        super().__init__(page, endpoints={
            "get": "https://maverick-6nk0.onrender.com/getgold",
            "post": "https://maverick-6nk0.onrender.com/postgold"
        })
    
    async def fetch_data(self):
        return requests.get(self.endpoints["get"]).json()


class GBPJPY(BaseInstrument):
    def __init__(self, page):
        super().__init__(page, endpoints={
            "get": "https://maverick-6nk0.onrender.com/getgbpjpy",
            "post": "https://maverick-6nk0.onrender.com/postgbpjpy"
        })
    
    async def fetch_data(self):
        data = requests.get(self.endpoints["get"]).json()
        # Note: GBPJPY doesn't seem to have volume in the original implementation
        return data


class XRPUSD(BaseInstrument):
    def __init__(self, page):
        super().__init__(page, endpoints={
            "get": "https://maverick-6nk0.onrender.com/getgbpjpy",  # This seems to be the same as GBPJPY in original code
            "post": "https://maverick-6nk0.onrender.com/postripple"
        })
    
    # Override to make non-async as in the original
    def add_hello(self, e):
        data = requests.get(self.endpoints["get"]).json()
        self.low_field.value = data["daily_low"]
        self.high_field.value = data["daily_high"]
        self.open_field.value = data["open_price"]
        self.update()
