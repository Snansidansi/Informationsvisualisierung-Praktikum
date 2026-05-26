from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import sys
import datenbereinigung
from visualisierung import show_sorted_alphabetical_list_with_image_link, show_pie_chart, show_value_histogram

data = None

def render_attribute_selection():
    excluded_attributes = ['Image Link', 'National Team Image Link']
    selectable_attributes = [col for col in data.columns if col not in excluded_attributes]
    return [
        dcc.Dropdown(
            options=selectable_attributes,
            value="On Loan",
            id="attributs"
        ),
        html.Div(id="attributs-output-container")
    ]

@callback(
    Output("attributs-output-container", "children"),
    Input("attributs", "value")
)
def update_output(value):
    text = html.Div(f"You have selected {value}")
    
    if value == "Known As" or value == "Full Name":
        visualization = show_sorted_alphabetical_list_with_image_link(data, value, image_col_name="Image Link")
    elif value == "Value(in Euro)":
        data_column = data[value]
        data_without_null = data_column[data_column > 0]
        visualization = html.Div([
            show_value_histogram(data_without_null, type="log"),
            show_value_histogram(data_without_null, type="linear")
            ])
    elif value == "Preferred Foot":
        visualization = html.Div([
            show_pie_chart(data[value]),
            show_value_histogram(data[value], type="log")
            ])
    elif value == "On Loan":
        visualization = show_pie_chart(data[value])
    elif value in ["National Team Name", "National Team Position"]:
        data_column = data[value]
        data_without_no_Team = data_column[data_column != "No National Team"]
        visualization = html.Div([
            show_value_histogram(data[value], type="linear", title="Histogramm mit linearer Scala und Spielern ohne Team"),
            show_value_histogram(data_without_no_Team, type="log", title="Histogramm mit log Scala ohne Spieler ohne Team")
            ])

        if value == "National Team Name":
            df_cleaned = data[[value, "National Team Image Link"]].dropna()
            df_cleaned = df_cleaned[df_cleaned[value] != "No National Team"]
            df_unique_teams = df_cleaned.drop_duplicates(subset=[value])

            team_list_component = show_sorted_alphabetical_list_with_image_link(
                    df_unique_teams, 
                    data_column_name=value, 
                    image_col_name="National Team Image Link"
                    )

            visualization.children.append(html.H2("Bilder zu den Teams"))
            visualization.children.append(team_list_component)
    elif value in ["Positions Played", "Best Position", "Club Name"]:
        visualization = show_value_histogram(data[value].explode(), type="linear")
    else:
        visualization = html.Div([
            show_value_histogram(data[value], type="linear"),
            show_value_histogram(data[value], type="log")
            ])

    return [text, visualization]

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv command line argument übergeben")
        exit(1)

    data = datenbereinigung.clean_data(csvPath)

    app = Dash()
    app.layout = html.Div([
        html.Div(children="Abgabe 1"),
        *render_attribute_selection()
    ])

    app.run(debug=True)
