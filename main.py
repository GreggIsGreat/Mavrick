from flet import *

from prices.xrp import WebScraper
from prices.nas import PriceScraperApp
from sidebar.sidebar import ModernNavBar
from fiscal_insight.prediction import Tab_menu


# from barcharts.barchart import Bar_chart


# TODO: Thabang Teddy
class PricePredictorSwitcher(Column):
    def __init__(self):
        super().__init__()
        self.maverick_switch = Switch(value=True, active_color="BLUE600", on_change=self.update_switches, rotate=55)
        self.index_switch = Switch(value=False, active_color="BLUE600", on_change=self.update_switches, rotate=55)

    def update_switches(self, e):
        if e.control == self.maverick_switch and self.maverick_switch.value:
            self.index_switch.value = False
        elif e.control == self.index_switch and self.index_switch.value:
            self.maverick_switch.value = False
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
                    bgcolor="BLUE",
                    color="WHITE"
                ),
            ]
        )


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
                alignment=MainAxisAlignment.START
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
                        PopupMenuItem(text='Account', on_click=self.account_page),
                        PopupMenuItem(text='Settings', on_click=self.settings_page),
                    ],
                ),
            ],
            bgcolor=colors.with_opacity(0.04, "WHITE")
        )


    def build(self):
        return self.topnav()


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
                                            Text("Reset in: 10-June-204", size=10, weight="bold")
                                        ]
                                    ),
                                    #Chart will go here
                                    Image(
                                        src=f"Chart-1.png",
                                        fit=ImageFit.CONTAIN
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.END,
                                        controls=[
                                            IconButton(icons.SAVE, icon_color="WHITE"),
                                            IconButton(icons.AUTORENEW_OUTLINED, icon_color="WHITE")
                                        ]
                                    )

                                ]
                            )
                        ),

                        Row(
                            controls=[
                                Text(
                                    value='Popular News',
                                    weight='BOLD',
                                    size=18,
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
                            Row(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Container(
                                        width=200,
                                        padding=10,
                                        alignment=alignment.center_left,
                                        content=Text(
                                            value='PROFILE PAGE',
                                            weight='BOLD',
                                            size=25,
                                        ),
                                    ),
                                    # Container(
                                    #     width=100,
                                    #     padding=10,
                                    #     alignment=alignment.center_right,
                                    #     content=Icon(
                                    #         icons.PERSON,
                                    #         color='BLUE',
                                    #         size=30,
                                    #     ),
                                    # ),
                                ]),
                            # bgcolor=colors.with_opacity(0.03, 'WHITE54'),
                            # padding=8,
                            # margin=2,
                            # width=400,
                            # height=100,
                            # border_radius=10,
                        ),
                        Container(
                            alignment=alignment.center,
                            padding=10,
                            bgcolor=colors.with_opacity(0.4, color="INDIGO"),
                            width=300,
                            height=400,
                            content=Column(
                                horizontal_alignment=CrossAxisAlignment.START,
                                controls=[
                                    TextField(label="Open Price", border="underline", border_color=colors.WHITE),
                                    TextField(label="Volume Price", border="underline", border_color=colors.WHITE)
                                ]
                            )
                        )
                        # GridView(
                        #     expand=1,
                        #     max_extent=200,
                        #     animate_offset=300,
                        #     controls=[
                        #         # Open Price
                        #         Container(
                        #             padding=10,
                        #             alignment=alignment.center,
                        #             bgcolor=colors.with_opacity(0.10, 'BLACK'),
                        #             border_radius=border_radius.all(5),
                        #
                        #         ),
                        #         # Volume Price
                        #         Container(
                        #             padding=10,
                        #             alignment=alignment.center,
                        #             bgcolor=colors.with_opacity(0.10, 'RED'),
                        #             border_radius=border_radius.all(5),
                        #         ),
                        #     ]
                        # )

                    ]
                )
            )
        # Economic View
        if page.route == "/economic":
            topnav = top.topnav()
            page.views.append(
                View(
                    route='/economic',
                    controls=[
                        topnav,
                        menu,
                        FloatingActionButton(
                            icon=icons.HOME_FILLED,
                            on_click=lambda _: page.go('/mainpage')
                        ),
                        Row(
                            controls=[
                                Text(
                                    value='Economic Data',
                                    weight='BOLD',
                                    size=18,
                                ),

                                IconButton(
                                    icons.ERROR,
                                    # on_click=lambda _: page.go('/mainpage'),
                                    tooltip="Feature Coming Soon!"
                                )
                            ]
                        ),
                        Column(
                            scroll=ScrollMode.ALWAYS,
                            height=550,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.START,
                                    vertical_alignment=CrossAxisAlignment.START,
                                    controls=[
                                        Container(
                                            padding=15,
                                            width=250,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=5,
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                spacing=5,
                                                controls=[
                                                    # First row: Title and Impact
                                                    Row(
                                                        controls=[
                                                            Text("FOMC Statement", size=14, weight="bold"),
                                                            Text("High", size=14, weight="bold", color="red")
                                                        ],
                                                        alignment=MainAxisAlignment.SPACE_BETWEEN
                                                    ),
                                                    # Second row: Previous and Forecast
                                                    Row(
                                                        controls=[
                                                            Text("Previous: ", size=12),
                                                            Text("235K", size=18,  weight="bold"),  # No previous value
                                                            Text("Forecast: ", size=12),
                                                            Text("236K", size=18,  weight="bold")  # No forecast value
                                                        ],
                                                        alignment=MainAxisAlignment.SPACE_BETWEEN
                                                    )
                                                ]
                                            )
                                        ),


                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    vertical_alignment=CrossAxisAlignment.START,
                                    controls=[
                                        Container(
                                            padding=15,
                                            width=180,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                tight=True,
                                                spacing=-30,
                                                controls=[
                                                    Text("Initial Jobless Claims", size=10),
                                                    Text("123.4M", size=30, weight="bold")

                                                ]
                                            )

                                        ),
                                        Container(
                                            padding=15,
                                            width=180,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                tight=True,
                                                spacing=-30,
                                                controls=[
                                                    Text("Nonfarm Payrolls", size=10),
                                                    Text("123.4M", size=30, weight="bold")

                                                ]
                                            )

                                        ),

                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    vertical_alignment=CrossAxisAlignment.START,
                                    controls=[
                                        Container(
                                            padding=15,
                                            width=180,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                tight=True,
                                                spacing=-30,
                                                controls=[
                                                    Text("Initial Jobless Claims", size=10),
                                                    Text("123.4M", size=30, weight="bold")

                                                ]
                                            )

                                        ),
                                        Container(
                                            padding=15,
                                            width=180,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                tight=True,
                                                spacing=-30,
                                                controls=[
                                                    Text("Nonfarm Payrolls", size=10),
                                                    Text("123.4M", size=30, weight="bold")

                                                ]
                                            )

                                        ),

                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.CENTER,
                                    vertical_alignment=CrossAxisAlignment.START,
                                    controls=[
                                        Container(
                                            padding=15,
                                            width=180,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                tight=True,
                                                spacing=-30,
                                                controls=[
                                                    Text("Initial Jobless Claims", size=10),
                                                    Text("123.4M", size=30, weight="bold")

                                                ]
                                            )

                                        ),
                                        Container(
                                            padding=15,
                                            width=180,
                                            height=100,
                                            alignment=alignment.top_left,
                                            bgcolor=colors.with_opacity(0.04, 'WHITE'),
                                            border_radius=border_radius.all(5),
                                            content=Column(
                                                alignment=MainAxisAlignment.START,
                                                tight=True,
                                                spacing=-30,
                                                controls=[
                                                    Text("Nonfarm Payrolls", size=10),
                                                    Text("123.4M", size=30, weight="bold")

                                                ]
                                            )

                                        ),

                                    ]
                                ),

                            ]
                        ),
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
                            # font_family='MM'
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
