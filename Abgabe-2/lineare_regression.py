import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, callback, Input, Output, State
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def doRegression(df: pd.DataFrame):
    options = [{'label': col, 'value': col} for col in df.columns]
    initial_value = options[0]['value'] if options else None

    return html.Div([
        html.Label("Attribut für die y-Achse:"),
        dcc.Dropdown(id="y-achse", options=options, value=initial_value),

        html.Div(id="summary-diagram-container", style={'paddingBottom': '30px'}),
        html.Div(id="diagrams")
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
    
    for x_attribute in df.columns:
        if x_attribute == y_attribute:
            continue

        diagram, r2_value = getLinearRegressionDiagram(df, x_attribute, y_attribute)
        childrenWithR2.append((diagram, r2_value)) 
        
        r2_values.append({
            'Attribut': x_attribute,
            'R2': r2_value
        })

    childrenWithR2 = sorted(childrenWithR2, key=lambda item: item[1], reverse=True)
    children = [item[0] for item in childrenWithR2]

    if r2_values:
        df_r2 = pd.DataFrame(r2_values)
        df_r2 = df_r2.sort_values(by="R2", ascending=False)
        
        summary_fig = px.bar(
            df_r2, 
            x='Attribut', 
            y='R2',
            title="<b>R²-Score der paarweisen Attribute</b>",
            labels={'R2': 'Bestimmtheitsmaß (R²-Score)', 'Attribut': 'X-Attribut'},
            template='plotly_dark'
        )
        summary_graph = dcc.Graph(figure=summary_fig)
    else:
        summary_graph = html.Div("Keine numerischen Paare gefunden.")
        
    return children, summary_graph

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

    return dcc.Graph(figure=fig), r2