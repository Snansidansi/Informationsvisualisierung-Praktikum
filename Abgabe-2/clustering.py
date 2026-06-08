import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from plotly.subplots import make_subplots
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
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[f"k-means (k={k})" for k in k_values],
        horizontal_spacing=0.1,
        vertical_spacing=0.15
    )
    
    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    
    for k, (row, col) in zip(k_values, positions):
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(scaled_data)
        plot_df['Current_Cluster'] = [f"Cluster {c}" for c in cluster_labels]
        
        for cluster_id in sorted(plot_df['Current_Cluster'].unique()):
            subset = plot_df[plot_df['Current_Cluster'] == cluster_id]
            fig.add_trace(
                go.Scatter(
                    x=subset['PCA1'],
                    y=subset['PCA2'],
                    mode='markers',
                    marker=dict(size=7, opacity=0.8),
                    name=cluster_id,
                    text=subset['Wine_ID'],
                    hovertemplate="<b>Wein Index: %{text}</b><br>PCA1: %{x:.2f}<br>PCA2: %{y:.2f}<extra></extra>",
                    legendgroup=f"group_{k}",
                    showlegend=(row == 1 and col == 1)
                ),
                row=row, col=col
            )
            
        fig.update_xaxes(title_text="Hauptkomponente 1", row=row, col=col)
        fig.update_yaxes(title_text="Hauptkomponente 2", row=row, col=col)

    fig.update_layout(
        title="Weindaten: Cluster-Projektion via PCA in 2D",
        height=800,
        template="plotly_dark"
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
