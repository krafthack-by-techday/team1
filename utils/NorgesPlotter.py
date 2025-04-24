import pandas as pd
import plotly.graph_objects as go

class NorgesPlotter:
    def __init__(self, data: pd.DataFrame):
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
            data: pd.DataFrame = None
        ):
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
            name=name
        ))
        self.fig.update_layout(
            title=title,
            xaxis_title=x_title,
            yaxis_title=y_title

        )

    def shade_between_lines(
            self,
            trace1_index: int = 0,
            trace2_index: int = 1,
            color_above: str = "rgba(255, 0, 0, 0.1)",
            color_below: str = "rgba(0, 0, 255, 0.1)"
        ):
        """
        Shades the area between two existing traces in the plot.

        :param trace1_index: The index of the first trace in the figure.
        :param trace2_index: The index of the second trace in the figure.
        :param color_above: The color to use when the first trace is above the second.
        :param color_below: The color to use when the second trace is above the first.
        """
        # Get the x and y data from the previousely added traces
        trace1 = self.fig.data[trace1_index]
        trace2 = self.fig.data[trace2_index]

        x = trace1['x']
        y1 = trace1['y']
        y2 = trace2['y']

        # Add the first shaded area (y1 > y2)
        self.fig.add_trace(go.Scatter(
            x=x,
            y=[max(y1[i], y2[i]) for i in range(len(y1))],  # Upper boundary
            mode='lines',
            fill='tonexty',
            fillcolor=color_above,
            line=dict(color="rgba(0,0,0,0)"), #hiding the "helper" line
            showlegend=False,
            hoverinfo="skip"
        ))

        # Add the second shaded area (y2 > y1)
        self.fig.add_trace(go.Scatter(
            x=x,
            y=[min(y1[i], y2[i]) for i in range(len(y1))],  # Lower boundary
            mode='lines',
            fill='tonexty',
            fillcolor=color_below,
            line=dict(color='rgba(0,0,0,0)'), #hiding the "helper" line
            showlegend=False,
            hoverinfo="skip"
        ))

        
    def show_plot(self, streamlit_mode=False):
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
        "x": [1, 2, 3, 4, 5],
        "y": [10, 15, 13, 17, 20]
    })
    more_data = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [20, 25, 13, 7, 10]
    })
    
    plotter = NorgesPlotter(data)
    plotter.add_line(
        x_col="x",
        y_col="y",
        title="Example Line Plot",
        name="line1",
        x_title="X-axis",
        y_title="Y-axis"
    )
    plotter.add_line(
        data=more_data,
        x_col="x",
        y_col="y",
        title="Example Line Plot",
        name="line2",
        x_title="X-axis",
        y_title="Y-axis"
    )
    plotter.shade_between_lines()
    plotter.show_plot()
