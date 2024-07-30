import flet
from flet import *
from functools import partial


class ModernNavBar(Column):
    def __init__(self):
        super().__init__()

    def HighlightContainer(self, e):
        if e.data == "true":
            e.control.content.controls[0].icon_color = "WHITE90"
            e.control.content.controls[1].color = "WHITE90"
            e.control.content.update()
        else:
            e.control.content.controls[0].icon_color = "WHITE"
            e.control.content.controls[1].color = "WHITE"
            e.control.content.update()

    def ContainedIcon(self, icon_name, text, data, route):
        return Container(
            data=data,
            width=300,
            height=45,
            # border_radius=5,
            on_hover=lambda e: self.HighlightContainer(e),
            on_click=lambda _: self.page.go(route),
            ink=True,
            content=Row(
                controls=[
                    IconButton(
                        icon=icon_name,
                        icon_size=18,
                        icon_color="WHITE",
                        selected=True,
                        style=ButtonStyle(
                            shape={
                                "": RoundedRectangleBorder(radius=7),
                            },
                            overlay_color={"": "transparent"},
                        ),
                    ),
                    Text(
                        value=text,
                        color="WHITE",
                        # size=15,
                        # weight='bold',
                        opacity=1,
                        animate_opacity=200,
                    ),
                ],
            ),
        )

    def build(self):
        return Container(
            alignment=alignment.center,
            padding=20,
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Column(
                expand=True,
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.START,
                spacing=5,
                controls=[
                    self.ContainedIcon(icons.DASHBOARD_ROUNDED, "Dashboard", 1, '/mainpage'),
                    self.ContainedIcon(icons.PERSON_ROUNDED, "Profile", None, '/account'),
                    # self.ContainedIcon(icons.DASHBOARD_ROUNDED, "Dashboard", 2),
                    self.ContainedIcon(icons.CANDLESTICK_CHART, "Fiscal Insight", 3,'/predictor'),
                    self.ContainedIcon(icons.BAR_CHART, "Economic Data", None,'/economic'),
                    # self.ContainedIcon(icons.PIE_CHART_ROUNDED, "Analytics", None),
                    # self.ContainedIcon(icons.FAVORITE_ROUNDED, "Price Information", None),
                    # self.ContainedIcon(icons.WALLET_ROUNDED, "Wallet", None),
                    Divider(color="WHITE", height=12),
                    self.ContainedIcon(icons.SETTINGS, "Settings", None, '/settings'),
                ],
            ),
        )