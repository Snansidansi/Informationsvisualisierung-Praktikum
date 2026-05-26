from dash import Dash, dcc, html, Input, Output, callback
import sys
import datenbereinigung
from visualisierung import show_age_overall_scatter, show_average_overall_per_age, show_average_wage_per_age, show_sorted_alphabetical_list_with_image_link, show_pie_chart, show_value_histogram, show_age_wage_scatter, show_comparison_table

data = None

def render_attribute_selection():
    excluded_attributes = ['Image Link', 'National Team Image Link']
    selectable_attributes = [col for col in data.columns if col not in excluded_attributes]
    selectable_attributes.extend(["Age and Wage(in Euro)", "Age and Overall"])

    return [
        html.Label("Attribut:"),
        dcc.Dropdown(
            options=selectable_attributes,
            value="Age and Wage(in Euro)",
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
        data_without_null = data_column.dropna()
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
    elif selected_attribute == "Age and Wage(in Euro)":
        filtered_data = filtered_data.dropna(subset=['Age', 'Wage(in Euro)'])
        visualization = html.Div([
            show_age_wage_scatter(filtered_data),
            show_average_wage_per_age(filtered_data)
            ])
    elif selected_attribute == "Age and Overall":
        filtered_data = filtered_data.dropna(subset=['Age', 'Overall'])
        visualization = html.Div([
            show_age_overall_scatter(filtered_data),
            show_average_overall_per_age(filtered_data)
            ])
    else:
        visualization = html.Div([
            show_value_histogram(filtered_data[selected_attribute], type="linear"),
            show_value_histogram(filtered_data[selected_attribute], type="log")
            ])

    return [text, visualization]

@callback(
    Output("comparison-output", "children"),
    Input("compare-index1", "value"),
    Input("compare-index2", "value")
)
def update_comparison(index1, index2):
    if index1 is None or index2 is None:
        return html.Div("Bitte gültige Indizes eingeben.")
    try:
        idx1 = int(index1)
        idx2 = int(index2)
    except (ValueError, TypeError):
        return html.Div("Ungültige Eingabe.")
    if idx1 < 0 or idx1 >= len(data) or idx2 < 0 or idx2 >= len(data):
        return html.Div("Index außerhalb des Bereichs.")
    return show_comparison_table(data, idx1, idx2)

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
        *render_attribute_selection(),
        html.H2("Vergleich"),
        html.Label("Zeile 1 Index:"),
        dcc.Input(id="compare-index1", type="number", min=0, max=len(data)-1, step=1, value=0),
        html.Br(),
        html.Label("Zeile 2 Index:"),
        dcc.Input(id="compare-index2", type="number", min=0, max=len(data)-1, step=1, value=min(1, len(data)-1)),
        html.Br(),
        html.Div(id="comparison-output")
    ])

    app.run(debug=True)
