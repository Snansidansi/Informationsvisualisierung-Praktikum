import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, Input, Output, State
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def create_pairwise_r2_heatmap(df):
    columns = list(df.columns)
    n = len(columns)
    matrix = np.full((n, n), np.nan)
    for i, col_x in enumerate(columns):
        for j, col_y in enumerate(columns):
            if i == j:
                matrix[i, j] = 1.0
            else:
                sub = df[[col_x, col_y]].dropna()
                if len(sub) < 2:
                    matrix[i, j] = np.nan
                else:
                    corr = sub[col_x].corr(sub[col_y])
                    matrix[i, j] = corr ** 2
    fig = px.imshow(
        matrix,
        x=columns,
        y=columns,
        color_continuous_scale="RdBu_r",
        title="Alle Paare R² (Heatmap)",
        labels=dict(x="Attribut", y="Attribut", color="R²"),
        template="plotly_dark",
    )
    fig.update_layout(title_font=dict(size=16))
    return dcc.Graph(figure=fig)

def create_pairwise_r2_bar_chart(df):
    columns = list(df.columns)
    pairs_r2 = []
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            col_x = columns[i]
            col_y = columns[j]
            sub = df[[col_x, col_y]].dropna()
            if len(sub) < 2:
                continue
            corr = sub[col_x].corr(sub[col_y])
            if np.isnan(corr):
                continue
            r2 = corr ** 2
            pairs_r2.append({"Paar": f"{col_x} & {col_y}", "R2": r2})
    df_pairs = pd.DataFrame(pairs_r2)
    df_pairs = df_pairs.sort_values("R2", ascending=False)
    fig = px.bar(
        df_pairs,
        x="Paar",
        y="R2",
        title="Alle Paare R² (Balkendiagram)",
        labels={"R2": "R²"},
        template="plotly_dark"
    )
    fig.update_layout(title_font=dict(size=16), xaxis_tickangle=-80)
    return dcc.Graph(figure=fig)

def doRegression(df: pd.DataFrame):
    options = [{"label": col, "value": col} for col in df.columns]
    initial_value = options[0]["value"] if options else None

    return html.Div([
        html.Details([
            html.Summary("Heatmap und Balkendiagramm aller Attributpaare (R²)"),
            create_pairwise_r2_heatmap(df),
            html.Div(style={"height": "20px"}),
            create_pairwise_r2_bar_chart(df)
        ], style={"paddingBottom": "20px"}),

        html.Label("Attribut für die y-Achse:"),
        dcc.Dropdown(
            id="y-achse", 
            options=options, 
            value=initial_value,
            style={"backgroundColor": "#333", "color": "#000"}
        ),

        html.Div(id="summary-diagram-container", style={"paddingBottom": "30px"}),
        html.Div(id="diagrams"),
    ])


@callback(
    Output("diagrams", "children"),
    Output("summary-diagram-container", "children"),
    Input("y-achse", "value"),
    State("data-store", "data")
)
def update_diagrams(y_attribute: str, stored_data):
    if not y_attribute or not stored_data:
        return [], []

    df = pd.DataFrame(stored_data)
    
    childrenWithR2 = []
    r2_values = []
    pearson_values = []
    rmse_values = []
    
    for x_attribute in df.columns:
        if x_attribute == y_attribute:
            continue

        diagram, r2_value, pearson, rmse = getLinearRegressionDiagram(df, x_attribute, y_attribute)
        childrenWithR2.append((diagram, r2_value)) 
        
        r2_values.append({
            "Attribut": x_attribute,
            "R2": r2_value
        })
        pearson_values.append({
            "Attribut": x_attribute,
            "Pearson-r": pearson
        })
        rmse_values.append({
            "Attribut": x_attribute,
            "RMSE": rmse
        })

    childrenWithR2 = sorted(childrenWithR2, key=lambda item: item[1], reverse=True)
    children = [item[0] for item in childrenWithR2]

    summary_fig_r2 = _create_summary_bar_chart(r2_values, "R2", "Bestimmtheitsmaß (R²-Score)")
    summary_fig_pearson = _create_summary_bar_chart(pearson_values, "Pearson-r", "Pearson-Korrelationskoeffizient")
    summary_fig_rmse = _create_summary_bar_chart(rmse_values, "RMSE", "Root Mean Squared Error (RMSE)")
    
    summary_graph_r2 = dcc.Graph(figure=summary_fig_r2)
    summary_graph_pearson = dcc.Graph(figure=summary_fig_pearson)
    summary_graph_rmse = dcc.Graph(figure=summary_fig_rmse)
    
    summary_graph = html.Div([
        summary_graph_r2,
        html.Br(),
        summary_graph_pearson,
        html.Br(),
        summary_graph_rmse
    ])
        
    return children, summary_graph


def _create_summary_bar_chart(data, value_column, y_label):
    if not data:
        return px.bar(title="Keine Daten verfügbar")
    
    df = pd.DataFrame(data)
    df = df.sort_values(by=value_column, ascending=False)
    
    fig = px.bar(
        df, 
        x="Attribut", 
        y=value_column,
        title=f"<b>{y_label} der paarweisen Attribute</b>",
        labels={value_column: y_label, "Attribut": "X-Attribut"},
        template="plotly_dark"
    )
    
    return fig


def _add_residuals_to_plot(df, x_col, y_col, y_pred):
    residuals = df[y_col] - y_pred

    err_up = np.where(residuals < 0, np.abs(residuals), 0)
    err_down = np.where(residuals > 0, residuals, 0)

    plot_df = df.copy()
    plot_df["Distance"] = residuals

    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        trendline="ols",
        template="plotly_dark",
        hover_data={"Distance": ":.3f"},
    )

    fig.update_traces(
        error_y=dict(
            type="data",
            symmetric=False,
            array=err_up,
            arrayminus=err_down,
            color="gray",
            thickness=1,
            width=0,
        ),
        selector=dict(mode="markers"),
    )
    return fig


def getLinearRegressionDiagram(df: pd.DataFrame, x_attribute: str, y_attribute: str):
    clean_df = df[[x_attribute, y_attribute]].dropna()

    X = clean_df[[x_attribute]]
    y = clean_df[y_attribute]

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    r_corr = clean_df[x_attribute].corr(clean_df[y_attribute])

    r2 = r2_score(y, y_pred)

    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)

    fig = _add_residuals_to_plot(clean_df, x_attribute, y_attribute, y_pred)

    fig.data[1].line.color = "red"
    fig.data[1].line.width = 3

    fig.update_layout(
        title=f"<b>Regression: {y_attribute} nach {x_attribute}</b><br>"
        f"<sup>Pearson-r: {r_corr:.3f} | R²-Note: {r2:.3f} | Durchschnittlicher Fehler (RMSE): {rmse:.3f}</sup>"
    )

    return dcc.Graph(figure=fig), r2, r_corr, rmse
