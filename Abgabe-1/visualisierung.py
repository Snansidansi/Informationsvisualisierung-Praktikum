import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import html, dcc

def show_sorted_alphabetical_list_with_image_link(data_frame, data_column_name, image_col_name):
    df_cleaned = data_frame.dropna(subset=[data_column_name])
    df_sorted = df_cleaned.sort_values(by=data_column_name, ascending=True)

    list_elements = []
    for _, row in df_sorted.iterrows():
        name = row[data_column_name]
        image_url = row.get(image_col_name)

        if (
            pd.notna(image_url)
            and str(image_url).strip() != ""
            and str(image_url).lower() != "nan"
        ):
            element = html.A(
                name,
                href=image_url,
                target="_blank",
                referrerPolicy="no-referrer",
                style={
                    "fontWeight": "bold",
                    "color": "#007bff",
                    "textDecoration": "underline",
                },
            )
        else:
            element = html.Span(name, style={"fontWeight": "bold"})

        list_elements.append(html.Li(element, style={"marginBottom": "10px"}))

    return html.Ul(list_elements)

def show_pie_chart(data_column, title=None):
    if title == None:
        fig_title = data_column.name
    else:
        fig_title = title

    counts = data_column.value_counts()
    fig = px.pie(
        names=counts.index,
        values=counts.values,
        title=fig_title
    )
    return dcc.Graph(figure=fig)

def show_value_histogram(data_column, type="linear", title=None):
    if title == None:
        fig_title = f"Histogramm mit {type} Scala"
    else:
        fig_title = title

    fig = px.histogram(
        data_column,
        x=data_column.name,
        title=fig_title
    )
    fig.update_yaxes(type=type)
    fig.update_xaxes(categoryorder="total ascending")
    return dcc.Graph(figure=fig)

def show_average_wage_per_age(data):
    df_avg = data.groupby("Age")["Wage(in Euro)"].mean().reset_index()

    fig = px.bar(
        df_avg,
        x="Age",
        y="Wage(in Euro)",
        title="Durchschnittsgehalt pro Alter",
        labels={"Age": "Age", "Wage(in Euro)": "Average Wage (in Euro)"},
        template="plotly_white",
    )

    return dcc.Graph(figure=fig)

def show_age_wage_scatter(data):
    fig = px.scatter(
        data,
        x="Age",
        y="Wage(in Euro)",
        title="Gehaltsverteilung nach Alter",
        labels={"Age": "Age", "Wage(in Euro)": "Wage(in Euro)"},
        template="plotly_white",
    )

    fig.update_traces(marker_color="royalblue")

    return dcc.Graph(figure=fig)

def show_average_overall_per_age(data):
    df_avg = data.groupby("Age")["Overall"].mean().reset_index()
    fig = px.bar(
        df_avg,
        x="Age",
        y="Overall",
        title="Durchschnittliches Overall pro Alter",
        labels={"Age": "Age", "Overall": "Average Overall"},
        template="plotly_white",
    )
    return dcc.Graph(figure=fig)

def show_age_overall_scatter(data):
    fig = px.scatter(
        data,
        x="Age",
        y="Overall",
        title="Overall-Verteilung nach Alter",
        labels={"Age": "Age", "Overall": "Overall"},
        template="plotly_white",
    )
    fig.update_traces(marker_color="royalblue")
    return dcc.Graph(figure=fig)

def show_comparison_table(data_frame, index1, index2):
    try:
        row1 = data_frame.iloc[index1]
        row2 = data_frame.iloc[index2]
    except IndexError:
        return html.Div("Index außerhalb des Bereichs", style={"color": "red"})

    header = html.Thead(html.Tr([
        html.Th("Attribut"),
        html.Th(f"Zeile {index1}"),
        html.Th(f"Zeile {index2}")
    ]))

    rows = []
    for col in data_frame.columns:
        val1 = row1[col]
        val2 = row2[col]

        color1 = None
        color2 = None

        try:
            num1 = float(val1) if pd.notna(val1) else None
        except (ValueError, TypeError):
            num1 = None
        try:
            num2 = float(val2) if pd.notna(val2) else None
        except (ValueError, TypeError):
            num2 = None

        if num1 is not None and num2 is not None:
            if num1 < num2:
                color1 = "red"
                color2 = "green"
            elif num1 > num2:
                color1 = "green"
                color2 = "red"
        else:
            if str(val1) != str(val2):
                color1 = "orange"
                color2 = "orange"

        cell1 = html.Td(str(val1), style={"background-color": color1} if color1 else {})
        cell2 = html.Td(str(val2), style={"background-color": color2} if color2 else {})
        row = html.Tr([
            html.Td(col, style={"fontWeight": "bold"}),
            cell1,
            cell2
        ])
        rows.append(row)

    table = html.Table([header, html.Tbody(rows)], style={"borderCollapse": "collapse", "width": "100%"})

    legend = html.Div([
        html.Span("Legende: ", style={"fontWeight": "bold"}),
        html.Span(" ", style={"display": "inline-block", "width": "12px", "height": "12px", "backgroundColor": "red", "marginRight": "4px"}),
        " Kleinerer Wert  ",
        html.Span(" ", style={"display": "inline-block", "width": "12px", "height": "12px", "backgroundColor": "green", "marginRight": "4px"}),
        " Größerer Wert  ",
        html.Span(" ", style={"display": "inline-block", "width": "12px", "height": "12px", "backgroundColor": "orange", "marginRight": "4px"}),
        " Unterschiedlich (nicht numerisch)  ",
        html.Span(" ", style={"display": "inline-block", "width": "12px", "height": "12px", "backgroundColor": "transparent", "border": "1px solid black", "marginRight": "4px"}),
        " Gleiche Werte",
    ], style={"marginBottom": "10px"})

    return html.Div([legend, table])
