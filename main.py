from datetime import datetime, timedelta
from threading import Timer

from flet import *
import json

from prices.xrp import WebScraper
from prices.nas import PriceScraperApp
from sidebar.sidebar import ModernNavBar
from fiscal_insight.prediction import Tab_menu
from prices.calender import EconomicCalendarApp


# from barcharts.barchart import Bar_chart



# TODO: Thabang Teddy
class PricePredictorSwitcher(Column):
    def __init__(self):
        super().__init__()
        # Load saved state
        saved_state = self.load_switch_state()
        self.maverick_switch = Switch(value=saved_state.get('maverick', True),  # Default to True if missing
                                      active_track_color="BLUE900", active_color="WHITE",
                                      on_change=self.update_switches, rotate=55)
        self.index_switch = Switch(value=saved_state.get('index', False),  # Default to False if missing
                                   active_track_color="BLUE900", active_color="WHITE",
                                   on_change=self.update_switches, rotate=55)
        self.snack_bar = SnackBar(content=Text("Changes saved successfully!"), duration=3000)

    def load_switch_state(self):
        try:
            with open('switch_state.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"maverick": True, "index": False}  # Default state if file doesn't exist

    def update_switches(self, e):
        if e.control == self.maverick_switch and self.maverick_switch.value:
            self.index_switch.value = False
        elif e.control == self.index_switch and self.index_switch.value:
            self.maverick_switch.value = False
        save_switch_state(self.maverick_switch.value, self.index_switch.value)
        self.update()

    def save_changes(self, e):
        save_switch_state(self.maverick_switch.value, self.index_switch.value)
        self.snack_bar.open = True
        self.update()

    def build(self):
        return Column(
            alignment=MainAxisAlignment.CENTER,
            spacing=60,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            height=400,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.maverick_switch,
                                Text("Maverick", size=18)
                            ]
                        ),
                        Column(
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                self.index_switch,
                                Text("Index-I", size=18)
                            ]
                        ),
                    ]
                ),
                ElevatedButton(
                    "Save Changes",
                    icon="SAVE",
                    icon_color="WHITE",
                    bgcolor="BLUE900",
                    color="WHITE",
                    on_click=self.save_changes
                ),
                self.snack_bar,
            ]
        )



# Save function remains the same
def save_switch_state(maverick_state, index_state):
    with open('switch_state.json', 'w') as f:
        json.dump({"maverick": maverick_state, "index": index_state}, f)


# User Controls
class SideNavbar(Column):
    pass

    def UserData(self, name: str):
        return Container(
            content=Row(
                controls=[
                    Column(
                        spacing=3,
                        # alignment=alignment.bottom_left,
                        controls=[
                            Text(
                                value=name,
                                size=15,
                                # weight='bold',
                                opacity=1,
                                font_family='bl'
                            ),
                            # Text(
                            #     value=description,
                            #     size=9,
                            #     weight=400,
                            #     color='white54',
                            #     opacity=1,
                            #     animate_opacity=200,
                            #     font_family='mm'
                            # ),
                        ]
                    )
                ],
                alignment=MainAxisAlignment.CENTER
            ),
            padding=-20
        )

    def build(self):
        return Container(
            width=50,
            height=580,
            padding=padding.only(top=10),
            alignment=alignment.center,
        )


navbar = SideNavbar()


# AppBar Controls
class NavigationPanel(Column):
    def __init__(self, page):
        super().__init__()
        self.page = page  # this had to be moved lower just for it to work!!! Stupid Things fr!!
        self.drawer = NavigationDrawer(
            indicator_shape=None,
            controls=[
                Container(
                    height=200,
                    bgcolor='BLUE900',
                    content=Text("Maverick", size=25, font_family='bl'),
                    margin=10,
                    padding=10,
                    border_radius=10,
                    alignment=alignment.center,
                    on_click=lambda e: print("Clickable without Ink clicked!")
                ),
                ModernNavBar(),
            ]
        )
        self.page.drawer = self.drawer

    def show_drawer(self, e):
        self.drawer.open = True
        self.drawer.update()
        print('Drawer Is Working')

    def account_page(self, e):
        # print(self.page)
        self.page.go('/account')

    def settings_page(self, e):
        self.page.go('/settings')

    def intrinsic_value(self, e):
        self.page.go('/intrinsic')

    def dashboard(self, e):
        self.page.go('/')

    def topnav(self):
        # account_page = menu_item_clicked()
        return AppBar(
            leading=IconButton(icons.MENU_ROUNDED, on_click=self.show_drawer),
            title=navbar.UserData('Maverick'),  # Big Data Software Developer
            actions=[
                # CircleAvatar(
                #     bgcolor='BLUE800',
                #     color='WHITE',
                #     content=Text('TED', size=12),
                # ),
                PopupMenuButton(
                    items=[
                        PopupMenuItem(text='Coming Soon!'),
                    ],
                ),
            ],
            bgcolor=colors.with_opacity(0.04, "WHITE")
        )

    def build(self):
        return self.topnav()


class DateTimeDisplay(Column):
    def __init__(self):
        super().__init__()
        self.current_datetime_text = Text(size=14)
        self.next_release_datetime_text = Text(size=14)
        self.dialog = None

    def build(self):
        self.dialog = AlertDialog(
            title=Text("Economic Calendar"),
            content=Column([
                Row([
                    Text("Current:", weight="bold", size=14),
                    self.current_datetime_text,
                ]),
                Row([
                    Text("Next Release:", weight="bold", size=14),
                    self.next_release_datetime_text,
                ]),
            ]),
            actions=[
                IconButton(
                    icon=icons.REFRESH,
                    on_click=self.update_time,
                    tooltip="Refresh Time",
                ),
                TextButton("Close", on_click=self.close_dialog),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        return self.dialog

    def get_current_datetime(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def get_next_release_datetime(self):
        next_release = datetime.now() + timedelta(hours=1)
        return next_release.strftime("%Y-%m-%d %H:%M:%S")

    def update_time(self, e):
        self.current_datetime_text.value = self.get_current_datetime()
        self.next_release_datetime_text.value = self.get_next_release_datetime()
        self.update()

    def open_dialog(self, e):
        self.update_time(None)
        self.dialog.open = True
        self.update()

    def close_dialog(self, e):
        self.dialog.open = False
        self.update()

    def did_mount(self):
        self.update_time(None)


def main(page: Page) -> None:
    page.title = "Maverick"
    page.window_width = 430  # window's width is 400 px
    page.window_height = 850  # window's height is 800 px
    page.window_resizable = False
    page.theme_mode = ThemeMode.DARK

    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.scroll = ScrollMode.AUTO

    top = NavigationPanel(page)
    menu = top.drawer
    price_scraper = PriceScraperApp()
    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    calender = EconomicCalendarApp(url)

    page.fonts = {
        'bl': 'fonts/Blanka-Regular.otf',
        'os': 'fonts/Oswald-Regular.otf',
        'mm': 'fonts/MartianMono-Regular.ttf'
    }

    def route_change(e: RouteChangeEvent) -> None:
        # page.views.clear()

        page.views.append(
            View(
                route='/',
                controls=[
                    Text(value='MaveRick.', size=50, color='white', font_family='bl'),
                    IconButton(
                        icon=icons.NAVIGATE_NEXT,
                        icon_color="BLUE400",
                        icon_size=40,
                        tooltip="Open",
                        on_click=lambda _: page.go('/mainpage'))],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                spacing=26,
            ),

        )

        # MainPage View
        if page.route == "/mainpage":
            topnav = top.topnav()
            page.views.append(
                View(
                    route='/mainpage',
                    controls=[
                        topnav,
                        menu,
                        PriceScraperApp(),
                        Container(
                            padding=15,
                            width=400,
                            height=300,
                            alignment=alignment.top_left,
                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                            border_radius=border_radius.all(5),
                            content=Column(
                                alignment=MainAxisAlignment.START,
                                tight=True,
                                spacing=10,
                                controls=[
                                    Row(
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            Text("60 Day Closing Price Expectancy", size=10),
                                            Text("Reset in: 10-April-2025", size=10, weight="bold")
                                        ]
                                    ),
                                    # Chart will go here
                                    Image(
                                        src=f"Chart-1.png",
                                        fit=ImageFit.CONTAIN
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.END,
                                        controls=[
                                            IconButton(icons.DOWNLOAD, icon_color="WHITE"),
                                            IconButton(icons.AUTORENEW_OUTLINED, icon_color="WHITE")
                                        ]
                                    )

                                ]
                            )
                        ),

                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Text(
                                    value='Popular News',
                                    weight='BOLD',
                                    size=18,
                                    # fonts='os'
                                ),
                                Text(
                                    value='Coming Soon!!',
                                    weight='BOLD',
                                    size=12,
                                    # fonts='os'
                                ),
                            ]
                        ),

                        Column(
                            scroll=ScrollMode.ALWAYS,
                            height=200,
                            controls=[
                                Container(
                                    padding=15,
                                    width=400,
                                    height=150,
                                    alignment=alignment.top_left,
                                    bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                    border_radius=border_radius.all(5),
                                    content=Column(
                                        horizontal_alignment=CrossAxisAlignment.START,
                                        tight=True,
                                        scroll=ScrollMode.AUTO,
                                        spacing=-30,
                                        controls=[
                                            Text("US Index Today", size=10),
                                            Divider(color="BLUE"),
                                            Text("Today, the major US stock indices closed with mixed results."
                                                 " The Dow Jones Industrial Average slipped slightly by 0.3%, ending at 35,500"
                                                 "points. Meanwhile, the S&P 500 managed to edge up by 0.2%, closing "
                                                 "at 4,530"
                                                 " points, driven by gains in the technology and healthcare sectors. The Nasdaq "
                                                 "Composite showed the strongest performance of the day, rising by 0.5% to reach"
                                                 " 14,800 points, thanks to a surge in major tech stocks.", size=10)
                                        ]
                                    )
                                ),
                            ]
                        ),

                    ]
                )
            )

        # Account View
        if page.route == "/account":
            topnav = top.topnav()
            page.views.append(
                View(
                    route='/account',
                    controls=[
                        topnav,
                        menu,
                        FloatingActionButton(
                            icon=icons.HOME_FILLED,
                            on_click=lambda _: page.go('/mainpage')
                        ),
                        Container(
                            Column(
                                [
                                    Text(
                                        value='Profile',
                                        weight='BOLD',
                                        size=18,
                                        color=colors.WHITE,
                                    ),
                                    Container(
                                        alignment=alignment.center,
                                        padding=20,
                                        bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                        width=600,
                                        height=600,
                                        border_radius=10,
                                        content=Column(
                                            scroll=ScrollMode.AUTO,
                                            horizontal_alignment=CrossAxisAlignment.START,
                                            spacing=20,
                                            controls=[
                                                Text("About Maverick", size=18, weight="BOLD",
                                                     color=colors.WHITE),
                                                Text(
                                                    "Originally this app was called Index-I. It was aimed at "
                                                    "leveraging AI + "
                                                    "Machine Learning for Finance then later evolved to what it is "
                                                    "today which is "
                                                    "Maverick. Maverick is a Machine Learning and Data Analysis "
                                                    "Focused app"
                                                    "that empowers users to trade with confidence. By leveraging key "
                                                    "market indicators such as Open, Volume, High price & Low prices. "
                                                    "Maverick predicts closing prices with high accuracy.",
                                                    color=colors.WHITE,
                                                ),
                                                Text("Key Features:", size=18, weight="BOLD",
                                                     color=colors.WHITE),
                                                Text(
                                                    "• Advanced ML algorithms for price prediction\n"
                                                    "• Real-time data analysis\n"
                                                    "• User-friendly interface for traders of all levels\n"
                                                    "• Comprehensive market insights",
                                                    color=colors.WHITE,
                                                ),
                                                Text("Developer: Thabang Teddy", size=18, weight="BOLD",
                                                     color=colors.WHITE, ),
                                                Text(
                                                    "Thabang Teddy is a visionary developer with expertise in Machine "
                                                    "Learning and Financial Markets. His passion for combining "
                                                    "cutting-edge technology with trading strategies led to the "
                                                    "creation of Maverick.",
                                                    color=colors.WHITE,
                                                ),
                                                Row(
                                                    [
                                                        IconButton(
                                                            icon=icons.EMAIL,
                                                            bgcolor=colors.GREEN_900,
                                                            on_click="mailto:rttteddy@gmail.com",
                                                            tooltip="Contact Developer"
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                    spacing=20,
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                                spacing=20,
                            ),
                        )
                    ]
                )
            )
        # Economic View
        if page.route == "/economic":
            topnav = top.topnav()
            date_time_display = DateTimeDisplay()
            page.views.append(
                View(
                    route='/economic',
                    controls=[
                        topnav,
                        menu,
                        Container(
                            width=380,
                            height=600,  # Increased height to accommodate the switch and data
                            content=calender
                        ),
                        Container(
                            alignment=alignment.bottom_center,
                            height=180,
                            content=Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    FloatingActionButton(
                                        bgcolor="BLUE900",
                                        icon=icons.ACCESS_TIME,
                                        on_click=date_time_display.open_dialog,
                                    ),
                                    date_time_display,
                                    FloatingActionButton(
                                        icon=icons.HOME_FILLED,
                                        bgcolor="BLUE900",
                                        on_click=lambda _: page.go('/mainpage')
                                    ),
                                ]
                            ),
                        )

                    ]
                )
            )

        # Predictor  View
        if page.route == "/predictor":
            topnav = top.topnav()
            page.views.append(
                View(
                    route='/predictor',
                    controls=[
                        topnav,
                        menu,
                        FloatingActionButton(
                            icon=icons.HOME_FILLED,
                            on_click=lambda _: page.go('/mainpage')
                        ),
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN),
                        Tab_menu(),
                    ]
                )
            )

        # Settings View
        if page.route == "/settings":
            topnav = top.topnav()
            page.views.append(
                View(
                    route='/settings',
                    controls=[
                        topnav,
                        menu,
                        FloatingActionButton(
                            icon=icons.HOME_FILLED,
                            bgcolor='RED800',
                            on_click=lambda _: page.go('/mainpage')
                        ),
                        Text(
                            value='Settings',
                            weight='BOLD',
                            size=18,
                        ),
                        PricePredictorSwitcher(),

                    ]
                )
            )

        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


app(target=main, assets_dir='assets')
