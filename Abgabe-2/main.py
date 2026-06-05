import html
import sys
import plotly.io as pio

from datenbereinigung import clean_data
from dash import Dash

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv command line argument übergeben")
        exit(1)

    cleaned_data = clean_data(csvPath, True)

    app = Dash()
    pio.default = "seaborn"
    app.layout = html.Div([
        html.H1(children = "Abgabe 2")
    ])

    app.run(debug=True)