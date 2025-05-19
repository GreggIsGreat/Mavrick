from datetime import datetime, timedelta
from threading import Timer

from flet import *
import json
import sys

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
        
        # Load saved state for the switches
        saved_state = self.load_switch_state()
        self.maverick_switch = Checkbox(
            value=saved_state.get('maverick', True),
            label="Maverick",
            on_change=self.update_switches
        )
        self.index_switch = Checkbox(
            value=saved_state.get('index', False),
            label="Index-I",
            on_change=self.update_switches
        )


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
        
        # Save the state
        save_switch_state(self.maverick_switch.value, self.index_switch.value)
        
        # Show a dialog asking to refresh
        self.show_refresh_dialog()
        
        self.page.update()
    
    def show_refresh_dialog(self):
        dialog = AlertDialog(
            modal=True,
            title=Text("Settings Changed"),
            content=Text("The application needs to refresh to apply changes. Would you like to refresh now?"),
            actions=[
                TextButton("Later", on_click=self.close_dialog),
                TextButton("Refresh Now", on_click=self.refresh_application),
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def close_dialog(self, e):
        self.page.dialog.open = False
        self.page.update()
    
    def refresh_application(self, e):
        # Close any open dialog
        if hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
        
        # Show loading indicator
        self.page.splash = ProgressBar()
        self.page.update()
        
        # Reload the current route to refresh the application
        current_route = self.page.route
        self.page.go("/")  # First go to home
        if current_route != "/":
            # Then go back to the original route if not already home
            self.page.go(current_route)
        
        # Remove splash after a short delay
        self.page.splash = None
        self.page.update()

    def show_drawer(self, e):
        self.drawer.open = True
        self.drawer.update()
        print('Drawer Is Working')

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
                PopupMenuButton(
                    items=[
                        PopupMenuItem(
                            content=Column([
                                Row([
                                    self.maverick_switch,
                                ]),
                                Row([
                                    self.index_switch,
                                ]),
                            ]),
                            on_click=None,  # Disable click handling on the item itself
                        ),
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
            title=Text("Date and Time", weight="bold", size=16),
            content=Column([
                Row([
                    Text("Current Time:", weight="bold", size=14),
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


# Loading indicator that shows when there's data in input fields
class DataLoadingIndicator(UserControl):
    def __init__(self, page, instrument_controls):
        super().__init__()
        self.page = page
        self.instrument_controls = instrument_controls
        self.progress_bar = ProgressBar(visible=False, color="BLUE900")
        self.check_timer = None
        
    def did_mount(self):
        # Start checking for data in fields
        self.start_checking()
        
    def will_unmount(self):
        # Stop checking when component is removed
        self.stop_checking()
        
    def start_checking(self):
        self.check_for_data()
        # Check every 2 seconds
        self.check_timer = Timer(2.0, self.start_checking)
        self.check_timer.start()
        
    def stop_checking(self):
        if self.check_timer:
            self.check_timer.cancel()
            self.check_timer = None
            
    def check_for_data(self):
        has_data = False
        
        # Check if any of the text fields have data
        for control in self.instrument_controls:
            if hasattr(control, 'value') and control.value:
                has_data = True
                break
                
        # Update progress bar visibility
        if has_data != self.progress_bar.visible:
            self.progress_bar.visible = has_data
            self.update()
            
    def build(self):
        return Container(
            content=self.progress_bar,
            padding=10,
            width=380
        )


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
                    ]
                )
            )

        # Economic View
        if page.route == "/economic":
            topnav = top.topnav()
            date_time_display = DateTimeDisplay()
            economic_loading_indicator = DataLoadingIndicator(page, [calender])
            
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
                        economic_loading_indicator,
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
                                ]
                            ),
                        )
                    ]
                )
            )

        # Predictor View
        if page.route == "/predictor":
            topnav = top.topnav()
            tab_menu = Tab_menu()
            predictor_loading_indicator = DataLoadingIndicator(page, tab_menu.controls)
            
            page.views.append(
                View(
                    route='/predictor',
                    controls=[
                        topnav,
                        menu,
                        predictor_loading_indicator,
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN),
                        tab_menu,
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
