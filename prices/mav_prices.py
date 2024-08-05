import asyncio
import json

import requests
from flet import *


class USTECH100(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)

        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield)
        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit)
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=150,
            # bgcolor=colors.BLUE_900,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),

        )
        self.loading_ring = ProgressRing(visible=False)

    async def add_hello(self, e):
        self.loading_ring.visible = True
        self.update()

        # Simulate network delay
        await asyncio.sleep(1)

        data = requests.get("https://maverick-6nk0.onrender.com/getnas100").json()

        self.low_field.value = data["Daily_Low"]
        self.high_field.value = data["Daily_High"]
        self.volume_field.value = data["Volume"]
        self.open_field.value = data["Open_Price"]

        self.loading_ring.visible = False
        self.update()

    def clear_textfield(self, e):
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        format_value = lambda v: v.replace(',', '')
        volume = format_value(self.volume_field.value)
        volume = f"{float(volume) / 1000}k" if 'k' not in volume and float(volume) >= 1000 else volume

        data = {
            "open_price": format_value(self.open_field.value),
            "daily_high": format_value(self.high_field.value),
            "daily_low": format_value(self.low_field.value),
            "volume": volume
        }

        response = requests.post("https://maverick-6nk0.onrender.com/post_nas100", json=data)
        if response.status_code == 200:
            prediction = response.json()
            self.output_data(prediction)
            print(f"Data posted successfully! Prediction: {prediction}")
        else:
            print(f"Failed to post data. Response: {response.text}")

    def output_data(self, data):
        # Update the content of pred_container with the posted data
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def build(self):
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                # width=300,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        # height=70,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.button_add,
                                self.button_clear,
                                self.button_disabled,
                                self.button_refresh,
                                self.button_submit,
                            ]),
                    ),
                    self.loading_ring,
                ],
            ),
            self.pred_container,
        ])

    # TODO change to GBPJPY to US30 for now


class US30(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)

        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield)
        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit)
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=150,
            # bgcolor=colors.BLUE_900,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),

        )
        self.loading_ring = ProgressRing(visible=False)

    async def add_hello(self, e):
        self.loading_ring.visible = True
        self.update()

        # Simulate network delay
        await asyncio.sleep(1)

        data = requests.get("https://maverick-6nk0.onrender.com/getus30").json()

        self.low_field.value = data["daily_low"]
        self.high_field.value = data["daily_high"]
        self.volume_field.value = data["volume"]
        self.open_field.value = data["open_price"]

        self.loading_ring.visible = False
        self.update()

    def clear_textfield(self, e):
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        format_value = lambda v: v.replace(',', '')
        volume = format_value(self.volume_field.value)
        volume = f"{float(volume) / 1000}k" if 'k' not in volume and float(volume) >= 1000 else volume

        data = {
            "open_price": format_value(self.open_field.value),
            "daily_high": format_value(self.high_field.value),
            "daily_low": format_value(self.low_field.value),
            "volume": volume
        }

        response = requests.post("https://maverick-6nk0.onrender.com/postus30", json=data)
        if response.status_code == 200:
            prediction = response.json()
            self.output_data(prediction)
            print(f"Data posted successfully! Prediction: {prediction}")
        else:
            print(f"Failed to post data. Response: {response.text}")

    def output_data(self, data):
        # Update the content of pred_container with the posted data
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def build(self):
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                # width=300,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        # height=70,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.button_add,
                                self.button_clear,
                                self.button_disabled,
                                self.button_refresh,
                                self.button_submit,

                            ]),
                    ),
                    self.loading_ring,
                ],
            ),
            self.pred_container,
        ])


#
#     # TODO change to GOLD to GERMAN40 for now
#
class GER40(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)

        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit)
        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield)
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=150,
            # bgcolor=colors.BLUE_900,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),

        )
        self.loading_ring = ProgressRing(visible=False)

    async def add_hello(self, e):
        self.loading_ring.visible = True
        self.update()

        # Simulate network delay
        await asyncio.sleep(1)

        data = requests.get("https://index-i.onrender.com/german40").text
        open_price = data.split("Open: ")[1].split("\\n")[0]
        volume = data.split("Volume: ")[1].split("\\n")[0]
        low = data.split("Daily Low: ")[1].split("\\n")[0]
        high = data.split("Daily High: ")[1].split("\\n")[0]

        self.low_field.value = low
        self.high_field.value = high
        self.volume_field.value = volume
        self.open_field.value = open_price

        self.loading_ring.visible = False
        self.update()
    def clear_textfield(self, e):
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        data = {key: float(getattr(self, f"{key}_field").value.replace(',', '')) for key in
                ["open", "volume", "low", "high"]}
        response = requests.post("https://index-i.onrender.com/ger30", json=data)
        if response.status_code == 200:
            prediction = response.json()["prediction"]
            self.output_data(prediction)
            print(f"Data posted successfully! Prediction: {prediction}")
        else:
            print(f"Failed to post data. Response: {response.text}")

    def output_data(self, data):
        # Update the content of pred_container with the posted data
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def build(self):
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                # width=300,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        # height=70,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.button_add,
                                self.button_clear,
                                self.button_disabled,
                                self.button_refresh,
                                self.button_submit,

                            ]),
                    ),
                    self.loading_ring,
                ],
            ),
            self.pred_container,
        ])


class XAUUSD(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)

        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit)
        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield)
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=150,
            # bgcolor=colors.BLUE_900,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),

        )
        self.loading_ring = ProgressRing(visible=False)

    async def add_hello(self, e):
        self.loading_ring.visible = True
        self.update()

        # Simulate network delay
        await asyncio.sleep(1)

        data = requests.get("https://maverick-6nk0.onrender.com/getgold").json()

        self.low_field.value = data["daily_low"]
        self.high_field.value = data["daily_high"]
        self.volume_field.value = data["volume"]
        self.open_field.value = data["open_price"]

        self.loading_ring.visible = False
        self.update()
    def clear_textfield(self, e):
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        format_value = lambda v: v.replace(',', '')
        volume = format_value(self.volume_field.value)
        volume = f"{float(volume) / 1000}k" if 'k' not in volume and float(volume) >= 1000 else volume

        data = {
            "open_price": format_value(self.open_field.value),
            "daily_high": format_value(self.high_field.value),
            "daily_low": format_value(self.low_field.value),
            "volume": volume
        }

        response = requests.post("https://maverick-6nk0.onrender.com/postgold", json=data)
        if response.status_code == 200:
            prediction = response.json()
            self.output_data(prediction)
            print(f"Data posted successfully! Prediction: {prediction}")
        else:
            print(f"Failed to post data. Response: {response.text}")

    def output_data(self, data):
        # Update the content of pred_container with the posted data
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def build(self):
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                # width=300,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        # height=70,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.button_add,
                                self.button_clear,
                                self.button_disabled,
                                self.button_refresh,
                                self.button_submit,

                            ]),
                    ),
                    self.loading_ring,
                ],
            ),
            self.pred_container,
        ])


class GBPJPY(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)

        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit)
        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield)
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=150,
            # bgcolor=colors.BLUE_900,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),

        )
        self.loading_ring = ProgressRing(visible=False)

    async def add_hello(self, e):
        self.loading_ring.visible = True
        self.update()

        # Simulate network delay
        await asyncio.sleep(1)

        data = requests.get("https://maverick-6nk0.onrender.com/getgbpjpy").json()

        self.low_field.value = data["daily_low"]
        self.high_field.value = data["daily_high"]
        self.open_field.value = data["open_price"]

        self.loading_ring.visible = False
        self.update()

    def clear_textfield(self, e):
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        format_value = lambda v: v.replace(',', '')
        volume = format_value(self.volume_field.value)
        volume = f"{float(volume) / 1000}k" if 'k' not in volume and float(volume) >= 1000 else volume

        data = {
            "open_price": format_value(self.open_field.value),
            "daily_high": format_value(self.high_field.value),
            "daily_low": format_value(self.low_field.value),
            "volume": volume
        }

        response = requests.post("https://maverick-6nk0.onrender.com/postgbpjpy", json=data)
        if response.status_code == 200:
            prediction = response.json()
            self.output_data(prediction)
            print(f"Data posted successfully! Prediction: {prediction}")
        else:
            print(f"Failed to post data. Response: {response.text}")

    def output_data(self, data):
        # Update the content of pred_container with the posted data
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def build(self):
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                # width=300,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        # height=70,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.button_add,
                                self.button_clear,
                                self.button_disabled,
                                self.button_refresh,
                                self.button_submit,

                            ]),
                    ),
                    self.loading_ring,
                ],
            ),
            self.pred_container,
        ])


class XRPUSD(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.open_field = TextField(label="Open Price", border="underline", border_color=colors.WHITE)
        self.volume_field = TextField(label="Volume", border="underline", border_color=colors.WHITE)
        self.low_field = TextField(label="Low Price", border="underline", border_color=colors.WHITE)
        self.high_field = TextField(label="High Price", border="underline", border_color=colors.WHITE)

        self.button_disabled = IconButton(icons.REMOVE_OUTLINED, disabled=True)
        self.button_refresh = IconButton(icons.AUTORENEW_OUTLINED, on_click=self.add_hello)
        self.button_submit = IconButton(icons.SEND, on_click=self.button_submit)
        self.button_add = IconButton(icons.GET_APP, on_click=self.add_hello)
        self.button_clear = IconButton(icons.DELETE_FOREVER, on_click=self.clear_textfield)
        self.pred_container = Container(
            alignment=alignment.center,
            width=400,
            height=150,
            # bgcolor=colors.BLUE_900,
            border=border.all(1.50, colors.BLUE_GREY_900),
            border_radius=10,
            content=Text(value="Results", size=14, font_family="mm", weight='bold'),

        )
        self.loading_ring = ProgressRing(visible=False)

    def add_hello(self, e):
        data = requests.get("https://maverick-6nk0.onrender.com/getgbpjpy").json()

        self.low_field.value = data["daily_low"]
        self.high_field.value = data["daily_high"]
        self.open_field.value = data["open_price"]
        self.update()

    def clear_textfield(self, e):
        self.open_field.value = ""
        self.volume_field.value = ""
        self.low_field.value = ""
        self.high_field.value = ""
        self.pred_container.content = Text(value="Results", size=14, font_family="mm", weight='bold')
        self.update()

    def button_submit(self, e):
        format_value = lambda v: v.replace(',', '')
        volume = format_value(self.volume_field.value)
        volume = f"{float(volume) / 1000}k" if 'k' not in volume and float(volume) >= 1000 else volume

        data = {
            "open_price": format_value(self.open_field.value),
            "daily_high": format_value(self.high_field.value),
            "daily_low": format_value(self.low_field.value),
            "volume": volume
        }

        response = requests.post("https://maverick-6nk0.onrender.com/postripple", json=data)
        if response.status_code == 200:
            prediction = response.json()
            self.output_data(prediction)
            print(f"Data posted successfully! Prediction: {prediction}")
        else:
            print(f"Failed to post data. Response: {response.text}")

    def output_data(self, data):
        # Update the content of pred_container with the posted data
        self.pred_container.content = Text(value=str(data), size=14, font_family="mm", weight='bold')
        self.update()

    def build(self):
        return Column([
            self.open_field,
            self.volume_field,
            self.low_field,
            self.high_field,
            Row(
                alignment=MainAxisAlignment.CENTER,
                height=80,
                spacing=20,
                # width=300,
                controls=[
                    Container(
                        bgcolor=colors.BLUE_900,
                        border_radius=5,
                        padding=5,
                        # height=70,
                        content=Row(
                            expand=4,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.button_add,
                                self.button_clear,
                                self.button_disabled,
                                self.button_submit,

                            ]),
                    ),
                    self.loading_ring,
                ],
            ),
            self.pred_container,
        ])
