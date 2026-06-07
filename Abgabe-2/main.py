import html
import sys
import lineare_regression
import dash_bootstrap_components as dbc
from dash import dcc

from datenbereinigung import clean_data
from dash import Dash, html

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv command line argument übergeben")
        exit(1)

    cleaned_data = clean_data(csvPath, True)

    app.layout = html.Div([
        html.H1(children = "Abgabe 2"),
        dcc.Store(id='daten-speicher', data=cleaned_data.to_dict('records')),
        lineare_regression.doRegression(cleaned_data)
    ])

    app.run(debug=True)