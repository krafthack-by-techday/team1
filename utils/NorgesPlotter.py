from typing import Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objs as go


class NorgesPlotter:
    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the NorgesPlotter with a DataFrame containing Norwegian data.

        :param data: A pandas DataFrame containing the data to be plotted.
        """
        self.data = data
        self.fig = go.Figure()
        self.fig.update_layout(
            plot_bgcolor="white",
            yaxis=dict(showgrid=False),
            xaxis=dict(showgrid=False),
            hovermode="x unified",
        )

    def add_line(
        self,
        x_col: str,
        y_col: str,
        name: str,
        title: str = "Line Plot",
        x_title: str = "Tid",
        y_title: str = "Kostnad",
        data: pd.DataFrame = None,
        line_color: str = None,
    ) -> None:
        """
        Adds a line trace to the plot using the provided x and y columns.

        :param x_col: The column name for the x-axis.
        :param y_col: The column name for the y-axis.
        :param name: The name of the trace (used in the legend).
        :param title: The title of the plot.
        :param x_title: The label for the x-axis.
        :param y_title: The label for the y-axis.
        """
        dataset = data if data is not None else self.data
        self.fig.add_trace(
            go.Scatter(
                x=dataset.index if x_col == "index" else dataset[x_col],
                y=dataset[y_col],
                mode="lines",
                name=name,
                line=dict(color=line_color, width=5) if line_color else None,
            )
        )
        self.fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title)

    def shade_between_lines(
        self,
        trace1_index=0,
        trace2_index=1,
        color_above="#C2EDA9",
        color_below="#FEEDC9",
    ):
        """
        Shades between two traces even if x values are timestamps.
        """
        trace1 = self.fig.data[trace1_index]
        trace2 = self.fig.data[trace2_index]

        x = pd.to_datetime(trace1["x"])  # convert to datetime just in case

        y1: np.ndarray = trace1["y"]
        y2: np.ndarray = trace2["y"]

        # 1) compute where y1 >= y2
        above = y1 >= y2
        # find the boundaries of each contiguous segment
        # we'll look for indices where 'above' flips
        flip_idx = np.nonzero(np.diff(above.astype(int)))[0] + 1
        # include start and end
        seg_bounds = np.concatenate(([0], flip_idx, [len(x)]))

        # 2) for each segment, build & plot one filled polygon
        for i in range(len(seg_bounds) - 1):
            start, end = seg_bounds[i], seg_bounds[i + 1]
            xi = x[start:end]
            y1i = y1[start:end]
            y2i = y2[start:end]
            # skip degenerate
            if len(xi) < 2:
                continue

            # build closed loop: go out on y1, back on y2
            xx = np.concatenate([xi, xi[::-1]])
            yy = np.concatenate([y1i, y2i[::-1]])

            color = color_above if above[start] else color_below

            self.fig.add_trace(
                go.Scattergl(
                    x=xx,
                    y=yy,
                    mode="none",  # no lines or markers
                    fill="toself",
                    fillcolor=color,
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

        # x = pd.to_datetime(trace1["x"])  # convert to datetime just in case
        # y1 = trace1["y"]
        # y2 = trace2["y"]

        # for i in range(len(x) - 1):
        #     x0 = x[i]
        #     x1 = x[i + 1]
        #     y1_0 = y1[i]
        #     y1_1 = y1[i + 1]
        #     y2_0 = y2[i]
        #     y2_1 = y2[i + 1]

        #     fill_color = (
        #         color_above if (y1_0 + y1_1) / 2 > (y2_0 + y2_1) / 2 else color_below
        #     )

        #     self.fig.add_trace(
        #         go.Scatter(
        #             x=[x0, x1, x1, x0],
        #             y=[y1_0, y1_1, y2_1, y2_0],
        #             mode="lines",
        #             fill="toself",
        #             fillcolor=fill_color,
        #             line=dict(width=0),
        #             hoverinfo="skip",
        #             showlegend=False,
        #         )
        #     )

        # self.fig.add_trace(
        #     go.Bar(
        #         x=[None],
        #         y=[None],
        #         marker=dict(color=color_above),
        #         name="Norgespris dyrere",
        #         showlegend=True,
        #         hoverinfo="skip",
        #     )
        # )

        # self.fig.add_trace(
        #     go.Bar(
        #         x=[None],
        #         y=[None],
        #         marker=dict(color=color_below),
        #         name="SPOT dyrere",
        #         showlegend=True,
        #         hoverinfo="skip",
        #     )
        # )

    def show_plot(self, streamlit_mode=False) -> Union[None, go.Figure]:
        """
        Displays the plot. If in Streamlit mode, it uses Streamlit's plotting function.

        :param streamlit_mode: If True, uses Streamlit to display the plot.
        """
        if self.fig is None:
            raise ValueError(
                "No plot has been created. Please create a plot first using plot_lines()."
            )

        if streamlit_mode:
            return self.fig
        else:
            self.fig.show(config={"displayModeBar": False})


if __name__ == "__main__":
    # A small example for showing the plot
    data = pd.DataFrame(
        {
            "x": pd.date_range(start="2023-01-01 00:00", periods=10, freq="h"),
            "y1": [10, 15, 13, 17, 20, 25, 30, 29, 40, 17],
            "y2": [20, 25, 13, 7, 10, 23, 28, 25, 37, 13],
        }
    )

    plotter = NorgesPlotter(data)
    plotter.add_line(
        x_col="x",
        y_col="y1",
        title="Example Line Plot",
        name="line1",
        x_title="Tid",
        y_title="Kostnad",
        line_color="#469d13",
    )
    plotter.add_line(
        x_col="x",
        y_col="y2",
        title="Example Line Plot",
        name="line2",
        x_title="Tid",
        y_title="Kostnad",
        line_color="#d29d2f",
    )
    plotter.shade_between_lines()
    plotter.show_plot()
