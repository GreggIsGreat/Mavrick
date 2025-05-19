from flet import *
import requests
from prices.mav_prices import USTECH100, US30, GER40, XAUUSD, XRPUSD, GBPJPY
from prices.index_prices import USTECH100_v2, US30_v2
import json

def get_switch_state():
    try:
        with open('switch_state.json', 'r') as f:
            state = json.load(f)
        return state['maverick']
    except FileNotFoundError:
        return True



class Tab_menu(Column):
    def __init__(self):
        super().__init__()

        # Event handler for the "GET_APP" icon

    def tabs(self):
        return Container(
            # alignment=alignment.center,
            width=400,
            height=640,
            # bgcolor=colors.ERROR_CONTAINER,
            content=Tabs(
                selected_index=2,
                animation_duration=300,
                divider_color=colors.with_opacity(0.01, 'GREEN900'),
                tab_alignment=TabAlignment.CENTER,
                # overlay_color=colors.RED_900,
                tabs=[
                    Tab(
                        text="GERMAN40",
                        content=Container(
                            content=Container(
                                # bgcolor=colors.with_opacity(0.07, 'INDIGO'),
                                # max_extent=200,
                                alignment=alignment.center,
                                animate_offset=300,
                                padding=20,
                                content=Column(
                                    controls=[
                                        GER40(page),
                                    ]
                                )
                            ),
                            alignment=alignment.center,
                        )
                    ),
                    Tab(
                        text="US30",
                        content=Container(
                            content=Container(
                                # bgcolor=colors.with_opacity(0.07, 'INDIGO'),
                                # max_extent=200,
                                alignment=alignment.center,
                                animate_offset=300,
                                padding=20,
                                content=Column(
                                    controls=[
                                        US30(page) if get_switch_state() else US30_v2(page),
                                    ]
                                )
                            ),
                            alignment=alignment.center,
                        )
                    ),
                    Tab(
                        text="NAS100",
                        content=Container(
                            content=Container(
                                # bgcolor=colors.with_opacity(0.07, 'INDIGO'),
                                # max_extent=200,
                                alignment=alignment.center,
                                animate_offset=300,
                                padding=20,
                                content=Column(
                                    controls=[
                                        USTECH100(page) if get_switch_state() else USTECH100_v2(page),

                                    ]
                                )
                            ),
                            alignment=alignment.center,
                        )
                    ),
                    Tab(
                        text="XAUUSD",
                        content=Container(
                            content=Container(
                                # bgcolor=colors.with_opacity(0.07, 'INDIGO'),
                                # max_extent=200,
                                alignment=alignment.center,
                                animate_offset=300,
                                padding=20,
                                content=Column(
                                    controls=[
                                        XAUUSD(page),
                                    ]
                                )
                            ),
                            alignment=alignment.center,
                        )
                    ),
                    Tab(
                        text="GBPJPY",
                        content=Container(
                            content=Container(
                                # bgcolor=colors.with_opacity(0.07, 'INDIGO'),
                                # max_extent=200,
                                alignment=alignment.center,
                                animate_offset=300,
                                padding=20,
                                content=Column(
                                    controls=[
                                        GBPJPY(page),
                                    ]
                                )
                            ),
                            alignment=alignment.center,
                        )
                    ),
                    Tab(
                        text="XRPUSD",
                        content=Container(
                            content=Container(
                                # bgcolor=colors.with_opacity(0.07, 'INDIGO'),
                                # max_extent=200,
                                alignment=alignment.center,
                                animate_offset=300,
                                padding=20,
                                content=Column(
                                    controls=[
                                        XRPUSD(page),
                                    ]
                                )
                            ),
                            alignment=alignment.center,
                        )
                    ),
                ],
                expand=1,
            )
        )

    def build(self):
        return self.tabs()
