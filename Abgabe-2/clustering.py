import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score, davies_bouldin_score
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

def render_full_clustering(df_clean):
    scatter_component = generate_cluster_scatter_component(df_clean)
    scree_component = generate_scree_plot_component(df_clean)
    
    full_layout_output = html.Div([
        html.Div(scatter_component, style={"marginBottom": "50px"}),
        html.Div(scree_component)
    ])
    
    return full_layout_output

def prepare_features(df_clean):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_clean)
    return scaled_data

def generate_cluster_scatter_component(df_clean):
    scaled_data = prepare_features(df_clean)
    
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)
    
    plot_df = pd.DataFrame(pca_data, columns=['PCA1', 'PCA2'])
    
    plot_df['Wine_ID'] = df_clean.index.astype(str)
    
    k_values = [2, 3, 4, 5]
    cluster_scores = []
    
    fig = make_subplots(
        rows=4, cols=2,
        # subplot_titles=[f"k-means (k={k})" for k in k_values],
        horizontal_spacing=0.1,
        vertical_spacing=0.15
    )

    colors = px.colors.qualitative.Plotly
    
    for k, row in zip(k_values, range(1, 4+1)):
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_data)
        plot_df['Current_Cluster'] = [f"Cluster {c}" for c in cluster_labels]

        for cluster_id, cluster_name in enumerate(sorted(plot_df['Current_Cluster'].unique())):
            subset = plot_df[plot_df['Current_Cluster'] == cluster_name]
            color = colors[cluster_id % len(colors)]
            fig.add_trace(
                go.Scatter(
                    x=subset['PCA1'],
                    y=subset['PCA2'],
                    mode='markers',
                    marker=dict(size=7, opacity=0.8, color=color),
                    name=cluster_name,
                    text=subset['Wine_ID'],
                    hovertemplate="<b>Wein Index: %{text}</b><br>PCA1: %{x:.2f}<br>PCA2: %{y:.2f}<extra></extra>",
                    showlegend=False,
                ),
                row=row, col=1
            )

        davies_bouldin = davies_bouldin_score(scaled_data, cluster_labels)

        x_min, x_max = plot_df["PCA1"].min(), plot_df["PCA1"].max()
        y_min, y_max = plot_df["PCA2"].min(), plot_df["PCA2"].max()

        x_pos = x_max + 0.05 * (x_max - x_min)
        y_pos = y_min + 0.05 * (y_max - y_min)

        axis_suffix = "" if row == 1 else str(2 * row - 1)

        fig.add_annotation(
            x=x_pos, y=y_pos,
            xref=f"x{axis_suffix}", yref=f"y{axis_suffix}",
            text= f"Davies-Bouldin: {davies_bouldin:.3f}",
            showarrow=False,
            align="right",
            xanchor="right", yanchor="bottom",
            font=dict(size=11, color="red"),
        )

        fig.update_xaxes(title_text="Hauptkomponente 1", row=row, col=1)
        fig.update_yaxes(title_text="Hauptkomponente 2", row=row, col=1)

        full_silhouette = silhouette_samples(scaled_data, cluster_labels)
        silhouette_avg = silhouette_score(scaled_data, cluster_labels)

        y_lower = 10
        for cluster_id in range(k):
            cluster_silhouette = full_silhouette[cluster_labels == cluster_id]
            cluster_wine_idxs = plot_df.loc[cluster_labels == cluster_id, "Wine_ID"].to_numpy()

            sort_idx = np.argsort(cluster_silhouette)

            cluster_silhouette = cluster_silhouette[sort_idx]
            cluster_wine_idxs = cluster_wine_idxs[sort_idx]

            color = colors[cluster_id % len(colors)]

            y_upper = y_lower + cluster_silhouette.shape[0]

            fig.add_trace(
                go.Bar(
                    x=cluster_silhouette, y=np.arange(y_lower, y_upper),
                    orientation="h",
                    marker=dict(
                        color=color,
                        line=dict(width=0),
                    ),
                    width=1.0,
                    customdata=np.column_stack([
                        cluster_wine_idxs,
                        np.full(cluster_silhouette.shape[0], cluster_id),
                        cluster_silhouette,
                    ]),
                    hovertemplate=(
                        "<b>Wein Index: %{customdata[0]}</b><br>"
                        "Cluster: %{customdata[1]}<br>"
                        "Silhouette: %{customdata[2]:.3f}"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                ),
                row=row, col=2,
            )
            y_lower = y_upper + 10

        fig.add_vline(
            x=silhouette_avg,
            line=dict(color="red", dash="dash", width=2),
            row=row, col=2,
        )
        fig.add_annotation(
            x=silhouette_avg,
            y=y_lower + 5,
            text=f"Ø Silhouette: {silhouette_avg:.3f}<br>",
            showarrow=False,
            font=dict(size=11, color="red"),
            xanchor="left",
            xref=f"x{2 * row}",
            yref=f"y{2 * row}",
        )
        fig.update_xaxes(
            title_text="Silhouettenkoeffizient",
            range=[-0.2, 0.5],
            zeroline=True,
            zerolinewidth=1,
            zerolinecolor="gray",
            row=row, col=2,
        )
        fig.update_yaxes(
            title_text="Cluster",
            showticklabels=False,
            range=[0, y_lower + 20],
            row=row, col=2,
        )

        cluster_scores.append({
            "k": k,
            "silhouette": silhouette_avg,
            "davies_bouldin": davies_bouldin,
        })

    scores_df = pd.DataFrame(cluster_scores)
    scores_df["silhouette_rank"] = scores_df["silhouette"].rank(ascending=False, method="min")
    scores_df["davies_bouldin_rank"] = scores_df["davies_bouldin"].rank(ascending=True, method="min")
    scores_df["combined_rank"] = scores_df["silhouette_rank"] + scores_df["davies_bouldin_rank"]
    best_k = scores_df.sort_values(["combined_rank", "silhouette_rank", "davies_bouldin_rank"]).iloc[0]["k"]

    best_row = k_values.index(best_k) + 1
    axis_key = "yaxis" if best_row == 1 else f"yaxis{2 * best_row - 1}"
    y0, y1 = fig.layout[axis_key].domain

    fig.add_shape(
        type="rect",
        xref="paper", yref="paper",
        x0=-0.1, x1=1.1,
        y0=y0-0.05, y1=y1+0.05,
        fillcolor="rgba(220, 220, 220, 0.12)",
        line=dict(width=0),
        layer="below",
    )
    fig.add_annotation(
        x=-0.06, y=(y0 + y1) / 2,
        xref="paper", yref="paper",
        text="<b>Am besten</b>",
        showarrow=False,
        textangle=-90,
        font=dict(size=14, color="lightgray"),
        xanchor="center", yanchor="middle",
    )
    
    fig.update_layout(
        title="Weindaten: Cluster-Projektion via PCA in 2D und Silhouette",
        height=1200,
        margin=dict(l=110, r=110, t=90, b=60),
        template="plotly_dark",
        barmode="overlay",
        bargap=0,
    )
    
    return dcc.Graph(figure=fig)

def generate_scree_plot_component(df_clean):
    scaled_data = prepare_features(df_clean)
    
    pca_full = PCA()
    pca_full.fit(scaled_data)
    
    explained_variance = pca_full.explained_variance_ratio_ * 100
    
    components = [f"PC {i}" for i in range(1, len(explained_variance) + 1)]
    
    cumulative_variance = np.cumsum(explained_variance)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=components,
        y=explained_variance,
        name='Individuelle Varianz (%)',
        marker_color='royalblue'
    ))
    
    fig.add_trace(go.Scatter(
        x=components,
        y=cumulative_variance,
        mode='lines+markers',
        name='Kumulierte Varianz (%)',
        line=dict(color='firebrick', width=2)
    ))
    
    fig.update_layout(
        title="Scree Plot: Erklärte Varianz durch Hauptkomponenten",
        xaxis_title="Hauptkomponente (PC)",
        yaxis_title="Erklaerte Varianz in %",
        template="plotly_dark",
        height=500
    )
    
    return dcc.Graph(figure=fig)
