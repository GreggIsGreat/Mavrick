import flet as ft
import requests
from datetime import datetime
import pytz



class EconomicCalendarApp(ft.Column):
    def __init__(self, url, local_timezone='Africa/Johannesburg'):
        super().__init__()
        self.url = url
        self.local_timezone = local_timezone
        self.events_column = ft.Column(scroll=ft.ScrollMode.AUTO, height=950, width=440)
        self.switch = ft.Switch(on_change=self.toggle_data, active_track_color="BLUE900", active_color="WHITE")
        self.data_visible = False

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(
                            value='Economic Data',
                            weight='BOLD',
                            size=18,
                        ),
                        self.switch,
                    ]
                ),
                ft.Container(
                    height=600,
                    content=self.events_column,
                    # border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=5,
                    padding=2,
                )
            ]),
        )

    def toggle_data(self, e):
        self.data_visible = self.switch.value
        if self.data_visible:
            self.update_events()
        else:
            self.events_column.controls.clear()
        self.update()

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch data from the URL")

    def filter_events(self, data):
        us_high_impact_events = []
        for event in data:
            if event['country'] == 'USD' and event['impact'] == 'High':
                us_high_impact_events.append({
                    'title': event['title'],
                    'date': event['date'],
                    'impact': event['impact'],
                    'previous': event.get('previous', 'N/A'),
                    'forecast': event.get('forecast', 'N/A'),
                    'actual': event.get('actual', 'N/A')
                })
        return us_high_impact_events

    def convert_to_local_time(self, date_str):
        utc_time = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        local_timezone = pytz.timezone(self.local_timezone)
        local_time = utc_time.astimezone(local_timezone)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')

    def create_event_container(self, event):
        return ft.Container(
            padding=15,
            width=380,
            height=120,
            alignment=ft.alignment.top_left,
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.WHITE),
            border_radius=5,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                spacing=5,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(event['title'], size=14, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                bgcolor=ft.colors.RED,
                                padding=5,
                                border_radius=3,
                                content=ft.Text(event['impact'], size=12, weight=ft.FontWeight.BOLD,
                                                color=ft.colors.WHITE)
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        spacing=-10,
                        controls=[
                            ft.Text("Actual: ", size=14),
                            ft.Text(event['actual'], size=18, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        spacing=-10,
                        controls=[
                            ft.Text("Previous: ", size=14),
                            ft.Text(event['previous'], size=18, weight=ft.FontWeight.BOLD),
                            ft.VerticalDivider(),
                            ft.Text("Forecast: ", size=14),
                            ft.Text(event['forecast'], size=18, weight=ft.FontWeight.BOLD)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )

    def update_events(self):
        if not self.data_visible:
            return

        data = self.fetch_data()
        us_high_impact_events = self.filter_events(data)

        self.events_column.controls.clear()
        for event in us_high_impact_events:
            event_container = self.create_event_container(event)
            self.events_column.controls.append(event_container)

        self.update()
