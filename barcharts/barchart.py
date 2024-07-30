from flet import *


class Bar_chart(UserControl):
    def __init__(self):
        super().__init__()

    def barChart(self):
        return BarChart(
            bar_groups=[
                BarChartGroup(
                    x=0,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=40,
                            width=40,
                            color=colors.BLUE,
                            tooltip="17000",
                            border_radius=0,
                        ),
                    ],
                ),
                BarChartGroup(
                    x=1,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=100,
                            width=40,
                            color=colors.BLUE,
                            tooltip="15000",
                            border_radius=0,
                        ),
                    ],
                ),
                BarChartGroup(
                    x=2,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=30,
                            width=40,
                            color=colors.BLUE,
                            tooltip="16000",
                            border_radius=0,
                        ),
                    ],
                ),
                BarChartGroup(
                    x=3,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=60,
                            width=40,
                            color=colors.BLUE,
                            tooltip="10093",
                            border_radius=0,
                        ),
                    ],
                ),
                BarChartGroup(
                    x=4,
                    bar_rods=[
                        BarChartRod(
                            from_y=0,
                            to_y=70,
                            width=40,
                            color=colors.BLUE,
                            tooltip="10093",
                            border_radius=0,
                        ),
                    ],
                ),
            ],
            border=border.all(2, colors.GREY_400),
            top_axis=ChartAxis(
                labels_size=10, title=Text("NASDAQ100", weight='bold'), title_size=20,
            ),
            bottom_axis=ChartAxis(
                labels=[
                    ChartAxisLabel(
                        value=0, label=Container(Text("Mon"), padding=10)
                    ),
                    ChartAxisLabel(
                        value=1, label=Container(Text("Tue"), padding=10)
                    ),
                    ChartAxisLabel(
                        value=2, label=Container(Text("Wed"), padding=10)
                    ),
                    ChartAxisLabel(
                        value=3, label=Container(Text("Thur"), padding=10)
                    ),
                    ChartAxisLabel(
                        value=4, label=Container(Text("Fri"), padding=10)
                    ),
                ],
                labels_size=40,
            ),
            horizontal_grid_lines=ChartGridLines(
                color=colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=colors.with_opacity(1, color='WHITE54'),
            max_y=110,
            interactive=True,
            expand=True,
        )

    def build(self):
        return self.barChart()
