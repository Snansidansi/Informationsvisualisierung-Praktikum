import html
import sys
import lineare_regression
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output

from datenbereinigung import clean_data
from dash import Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv command line argument übergeben")
        exit(1)

    cleaned_data = clean_data(csvPath, True)

    app.layout = html.Div([
        html.H1(children="Abgabe 2 - Regression und Clustering", style={'marginBottom': '30px'}),
        dcc.Store(id="data-store", data=cleaned_data.to_dict("records")),
        dcc.Tabs([
            dcc.Tab(label="Lineare Regression", children=html.Div(lineare_regression.doRegression(cleaned_data), style={'padding': '20px'})),
            dcc.Tab(label="K-Means Clustering", children=html.Div(style={'padding': '20px'}))
        ], style={'padding': '20px'})
    ], style={'padding': '20px'})

    app.run(debug=True)
