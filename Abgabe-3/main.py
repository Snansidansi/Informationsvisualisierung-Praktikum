import sys
import dash_bootstrap_components as dbc
from dash import dcc, html

from datenbereinigung import clean_data
from visualisierung import render_evaluation_visualization
from train import train_10fold, train_bootstrap_632
from dash import Dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv als command line argument übergeben")
        exit(1)

    cleaned_data = clean_data(csvPath)

    results_10fold, preds_10fold, models_10fold = train_10fold(cleaned_data)
    results_bootstrap = train_bootstrap_632(cleaned_data)

    app.layout = html.Div([
        html.H1(
            children="Abgabe 3 - Klassifikation und Evaluation", 
            style={'marginBottom': '40px', 'textAlign': 'center', 'fontWeight': 'bold', 'color': '#2c3e50'}
        ),
        dcc.Store(id="data-store", data=cleaned_data.to_dict("records")),
        dcc.Tabs([
            dcc.Tab(
                children=html.Div(
                    render_evaluation_visualization(cleaned_data, results_10fold, results_bootstrap, preds_10fold, models_10fold), 
                    style={'padding': '30px', 'backgroundColor': '#ffffff'}
                )
            )
        ], style={'paddingX': '10px'})
    ], style={
        'padding': '30px', 
        'backgroundColor': '#f8f9fa', 
        'fontFamily': 'Arial, sans-serif'
    })

    app.run(debug=True)