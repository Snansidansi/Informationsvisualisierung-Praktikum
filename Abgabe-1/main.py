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
        html.Label("Attribut:"),
        dcc.Dropdown(
            options=selectable_attributes,
            value="On Loan",
            id="attributs"
        ),
        html.Div([
            html.Label("Nationality:"),
            dcc.Dropdown(
                id="nationality_dropdown",
                options=nationality_options,
                value="All"
            ),
            html.Label("Club:"),
            dcc.Dropdown(
                id="club_dropdown",
                options=club_options,
                value="All"
            ),
        ]),
        html.Div(id="attributs-output-container")
    ]

@callback(
    Output("attributs-output-container", "children"),
    Input("attributs", "value"),
    Input("nationality_dropdown", "value"),
    Input("club_dropdown", "value")
)
def update_output(selected_attribute, selected_nationality, selected_club):
    filtered_data = data.copy()
    if selected_nationality and selected_nationality != "All":
        filtered_data = filtered_data[filtered_data['Nationality'] == selected_nationality]
    if selected_club and selected_club != "All":
        filtered_data = filtered_data[filtered_data['Club Name'] == selected_club]

    text = html.Div(f"You have selected {selected_attribute}")
    
    if selected_attribute == "Known As" or selected_attribute == "Full Name":
        visualization = show_sorted_alphabetical_list_with_image_link(filtered_data, selected_attribute, image_col_name="Image Link")
    elif selected_attribute == "Value(in Euro)":
        data_column = filtered_data[selected_attribute]
        data_without_null = data_column[data_column > 0]
        visualization = html.Div([
            show_value_histogram(data_without_null, type="log"),
            show_value_histogram(data_without_null, type="linear")
            ])
    elif selected_attribute == "Preferred Foot":
        visualization = html.Div([
            show_pie_chart(filtered_data[selected_attribute]),
            show_value_histogram(filtered_data[selected_attribute], type="log")
            ])
    elif selected_attribute == "On Loan":
        visualization = show_pie_chart(filtered_data[selected_attribute])
    elif selected_attribute in ["National Team Name", "National Team Position"]:
        data_column = filtered_data[selected_attribute]
        data_without_no_Team = data_column[data_column != "No National Team"]
        visualization = html.Div([
            show_value_histogram(filtered_data[selected_attribute], type="linear", title="Histogramm mit linearer Scala und Spielern ohne Team"),
            show_value_histogram(data_without_no_Team, type="log", title="Histogramm mit log Scala ohne Spieler ohne Team")
            ])

        if selected_attribute == "National Team Name":
            df_cleaned = filtered_data[[selected_attribute, "National Team Image Link"]].dropna()
            df_cleaned = df_cleaned[df_cleaned[selected_attribute] != "No National Team"]
            df_unique_teams = df_cleaned.drop_duplicates(subset=[selected_attribute])

            team_list_component = show_sorted_alphabetical_list_with_image_link(
                    df_unique_teams, 
                    data_column_name=selected_attribute, 
                    image_col_name="National Team Image Link"
                    )

            visualization.children.append(html.H2("Bilder zu den Teams"))
            visualization.children.append(team_list_component)
    elif selected_attribute in ["Positions Played", "Best Position", "Club Name"]:
        visualization = show_value_histogram(filtered_data[selected_attribute].explode(), type="linear")
    else:
        visualization = html.Div([
            show_value_histogram(filtered_data[selected_attribute], type="linear"),
            show_value_histogram(filtered_data[selected_attribute], type="log")
            ])

    return [text, visualization]

if __name__ == "__main__":
    try:
        csvPath = sys.argv[1]
    except Exception as e:
        print("Bitte den Dateipfad zu der csv command line argument übergeben")
        exit(1)

    data = datenbereinigung.clean_data(csvPath)

    nationality_options = [{"label": "All", "value": "All"}] + [{"label": nat, "value": nat} for nat in sorted(data['Nationality'].dropna().unique())]
    club_options = [{"label": "All", "value": "All"}] + [{"label": clb, "value": clb} for clb in sorted(data['Club Name'].dropna().unique())]

    app = Dash()
    app.layout = html.Div([
        html.H1(children="Abgabe 1"),
        *render_attribute_selection()
    ])

    app.run(debug=True)
