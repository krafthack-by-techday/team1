import pandas as pd
import plotly.graph_objects as go
import numpy as np
from typing import Optional, Union

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
            x_title: str = "X-axis",
            y_title: str = "Y-axis",
            data: pd.DataFrame = None,
            line_color: str = None
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
        self.fig.add_trace(go.Scatter(
            x=dataset[x_col],
            y=dataset[y_col],
            mode='lines',
            name=name,
            line=dict(color=line_color, width=5) if line_color else None,
        ))
        self.fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title

        )
  

    def shade_between_lines(
        self,
        trace1_index=0,
        trace2_index=1,
        color_above="#C2EDA9",
        color_below="#FEEDC9"
    ) -> None:
        """
        Shades the area between two traces based on which is higher.

        :param trace1_index: The index of the first trace in the figure.
        :param trace2_index: The index of the second trace in the figure.
        :param color_above: Color used when trace1 is above trace2.
        :param color_below: Color used when trace2 is above trace1.
        """
        import plotly.graph_objects as go
        import numpy as np

        # Get traces
        trace1 = self.fig.data[trace1_index]
        trace2 = self.fig.data[trace2_index]

        x = trace1['x']
        y1 = trace1['y']
        y2 = trace2['y']

        # Loop through each pair of consecutive points
        for i in range(len(x) - 1):
            # Coordinates for the current slice
            x0, x1 = x[i], x[i+1]
            y1_0, y1_1 = y1[i], y1[i+1]
            y2_0, y2_1 = y2[i], y2[i+1]

            if y1_0 + y1_1 > y2_0 + y2_1:
                fill_color = color_above
            else:
                fill_color = color_below

            self.fig.add_trace(go.Scatter(
                x=[x0, x1, x1, x0],
                y=[y1_0, y1_1, y2_1, y2_0],
                mode="lines",
                fill="toself",
                fillcolor=fill_color,
                line=dict(width=0),
                showlegend=False,
                hoverinfo="skip"
            ))

        
    def show_plot(self, streamlit_mode=False) -> Union[None, go.Figure]:
        """
        Displays the plot. If in Streamlit mode, it uses Streamlit's plotting function.

        :param streamlit_mode: If True, uses Streamlit to display the plot.
        """
        if self.fig is None:
            raise ValueError("No plot has been created. Please create a plot first using plot_lines().")
        
        if streamlit_mode:
            return self.fig
        else:
            self.fig.show(config={"displayModeBar": False})
        
if __name__ == "__main__":
    # A small example for creating the plot
    data = pd.DataFrame({
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [10, 15, 13, 17, 20, 25, 30, 29, 40, 17]
    })
    more_data = pd.DataFrame({
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "y": [20, 25, 13, 7, 10, 23, 28, 25, 37, 13]
    })
    
    plotter = NorgesPlotter(data)
    plotter.add_line(
        x_col="x",
        y_col="y",
        title="Example Line Plot",
        name="line1",
        x_title="X-axis",
        y_title="Y-axis",
        line_color="#469d13"
    )
    plotter.add_line(
        data=more_data,
        x_col="x",
        y_col="y",
        title="Example Line Plot",
        name="line2",
        x_title="X-axis",
        y_title="Y-axis",
        line_color="#d29d2f"
    )
    plotter.shade_between_lines()
    plotter.show_plot()
