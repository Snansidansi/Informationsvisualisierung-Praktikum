import pandas as pd
import plotly.express as px
from dash import dcc
from datenbereinigung import clean_data

def linear_regression(df: pd.DataFrame, x_key: str, y_key: str, dump: bool = False) -> dcc.Graph:
    fig = px.scatter(
        df, x=x_key, y=y_key,
        title=f"Lineare Regression: {x_key} vs {y_key}",
        template="plotly_white",
        trendline="ols",
    )
    if dump:
        fig.show()
    return dcc.Graph(figure=fig)

if __name__ == "__main__":
    df = clean_data("wein.csv")
    linear_regression(df, "Farbwert", "Farbintensitaet", dump=True)
