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
