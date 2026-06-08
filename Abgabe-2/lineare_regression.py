import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, Input, Output, State
from sklearn.linear_model import LinearRegression

def doRegression(df: pd.DataFrame):
    options = [{'label': col, 'value': col} for col in df.columns]
    initial_value = options[0]['value'] if options else None

    return html.Div([
        html.Label("Wähle ein Attribut für die y-Achse aus: "),
        dcc.Dropdown(id="y-achse", options=options, value=initial_value),
        html.Div(id="diagrams")
    ])

@callback(
    Output("diagrams", "children"),
    Input("y-achse", "value"),
    State("daten-speicher", "data")
)
def update_diagrams(y_attribute: str, gespeicherte_daten):
    if not y_attribute or not gespeicherte_daten:
        return []

    df = pd.DataFrame(gespeicherte_daten)
    
    children = []
    for x_attribute in df.columns:
        if x_attribute == y_attribute:
            continue
            
        if not pd.api.types.is_numeric_dtype(df[x_attribute]):
            continue
            
        diagram = getLinearRegressionDiagram(df, x_attribute, y_attribute)
        children.append(diagram) 
        
    return children

def getLinearRegressionDiagram(df: pd.DataFrame, x_attribute: str, y_attribute: str):
    fig = px.scatter(df, x=x_attribute, y=y_attribute, trendline="ols", template='plotly_dark')
    fig.data[1].line.color = 'red'
    fig.data[1].line.width = 3
    return dcc.Graph(figure=fig)