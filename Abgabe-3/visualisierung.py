import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from sklearn.metrics import confusion_matrix, classification_report


def render_evaluation_visualization(df_clean, results_10fold, results_bootstrap, predictions_10fold, fitted_models, model_name="Decision Tree"):
    y_true = df_clean["Survived"]
    
    y_pred = predictions_10fold[model_name]
    model = fitted_models[model_name]
    
    evaluation_component = generate_evaluation_results_component(results_10fold, results_bootstrap)
    confusion_component = generate_confusion_matrix_component(y_true, y_pred, model_name)
    tree_component = generate_decision_tree_component(df_clean, model, model_name)
    
    full_layout_output = html.Div([
        html.Div(evaluation_component, style={"marginBottom": "60px"}),
        html.Div(confusion_component, style={"marginBottom": "60px"}),
        html.Div(tree_component)
    ])
    
    return full_layout_output


def generate_evaluation_results_component(results_10fold, results_bootstrap):
    combined_results = results_10fold.copy()
    combined_results = combined_results.merge(results_bootstrap, on="Klassifizierer")
    
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=list(combined_results.columns),
            fill_color='#f1f3f4',
            align='left',
            font=dict(size=12, color='black', family='Arial, sans-serif')
        ),
        cells=dict(
            values=[combined_results[col] for col in combined_results.columns],
            fill_color='white',
            align='left',
            font=dict(size=11, color='black', family='Arial, sans-serif')
        )
    )])
    
    fig_table.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_white"
    )
    
    metrics = ["Genauigkeit", "Präzision", "Recall", "F1"]
    fig_metrics = go.Figure()
    colors = ['#1a73e8', '#d93025', '#f9ab00', '#188038']
    text_colors = ['white', 'white', 'black', 'white']
    
    for i, metric in enumerate(metrics):
        fig_metrics.add_trace(go.Bar(
            x=combined_results["Klassifizierer"],
            y=combined_results[metric],
            name=metric,
            marker_color=colors[i % len(colors)],
            text=[f"{val:.2f}" for val in combined_results[metric]],
            textposition='auto',
            textfont=dict(color=text_colors[i % len(text_colors)]),
            hovertext=[f"{metric}: {val:.4f}" for val in combined_results[metric]],
            hoverinfo="text",
            hoverlabel=dict(
                bgcolor=[colors[i % len(colors)]] * len(combined_results),
                font_color='black'
            )
        ))
    
    fig_metrics.update_layout(
        title="Vergleich der Metriken (10-Fold Cross Validation)",
        xaxis_title="Klassifizierer",
        yaxis_title="Wert",
        barmode='group',
        template="plotly_white",
        height=450,
        font=dict(family='Arial, sans-serif')
    )
    
    fig_bootstrap = go.Figure(go.Bar(
        x=combined_results["Klassifizierer"],
        y=combined_results["Bootstrap 0.632"],
        marker_color='#1a73e8',
        text=[f"{val:.2f}" for val in combined_results["Bootstrap 0.632"]],
        textposition='auto',
        textfont=dict(color='white'),
        hovertext=[f"Bootstrap 0.632: {val:.4f}" for val in combined_results["Bootstrap 0.632"]],
        hoverinfo="text",
        hoverlabel=dict(
            bgcolor=['#1a73e8'] * len(combined_results),
            font_color='black'
        )
    ))
    
    fig_bootstrap.update_layout(
        title="Bootstrap 0.632 Accuracy Ergebnisse",
        xaxis_title="Klassifizierer",
        yaxis_title="Accuracy",
        template="plotly_white",
        height=450,
        font=dict(family='Arial, sans-serif')
    )
    
    return html.Div([
        html.H3("Statistische Ergebnisse der Evaluierung", style={'marginBottom': '20px'}),
        dcc.Graph(figure=fig_table),
        dcc.Graph(figure=fig_metrics),
        dcc.Graph(figure=fig_bootstrap)
    ])


def generate_confusion_matrix_component(y_true, y_pred, model_name):
    cm = confusion_matrix(y_true, y_pred)
    
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Nicht überlebt (0)', 'Überlebt (1)'],
        y=['Nicht überlebt (0)', 'Überlebt (1)'],
        colorscale='Blues',
        text=cm,
        texttemplate="%{text}",
        textfont={"size": 16, "color": "black", "family": "Arial"}
    ))
    
    fig_cm.update_layout(
        title=f"Confusion Matrix ({model_name} - basierend auf 10-Fold CV)",
        xaxis_title="Vorhergesagter Wert",
        yaxis_title="Tatsächlicher Wert",
        template="plotly_white",
        height=450,
        font=dict(family='Arial, sans-serif')
    )
    
    report_dict = classification_report(y_true, y_pred, output_dict=True, target_names=['Nicht überlebt', 'Überlebt'])
    report_df = pd.DataFrame(report_dict).transpose()
    
    rows = []
    for idx in report_df.index:
        row = [idx,
               f"{report_df.loc[idx, 'precision']:.4f}" if 'precision' in report_df.columns and isinstance(report_df.loc[idx, 'precision'], float) else report_df.loc[idx, 'precision'],
               f"{report_df.loc[idx, 'recall']:.4f}" if 'recall' in report_df.columns and isinstance(report_df.loc[idx, 'recall'], float) else report_df.loc[idx, 'recall'],
               f"{report_df.loc[idx, 'f1-score']:.4f}" if 'f1-score' in report_df.columns and isinstance(report_df.loc[idx, 'f1-score'], float) else report_df.loc[idx, 'f1-score'],
               int(report_df.loc[idx, 'support']) if 'support' in report_df.columns else '']
        rows.append(row)
    
    fig_report = go.Figure(data=[go.Table(
        header=dict(
            values=["Klasse", "Präzision", "Recall", "F1-Score", "Support"],
            fill_color='#f1f3f4',
            align='left',
            font=dict(size=12, color='black', family='Arial, sans-serif')
        ),
        cells=dict(
            values=[[row[0] for row in rows], [row[1] for row in rows], [row[2] for row in rows], [row[3] for row in rows], [row[4] for row in rows]],
            fill_color='white',
            align='left',
            font=dict(size=11, color='black', family='Arial, sans-serif')
        )
    )])
    
    fig_report.update_layout(
        title="Klassifikationsbericht",
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_white"
    )
    
    return html.Div([
        html.H3("Confusion Matrix und Klassifikationsbericht", style={'marginTop': '40px', 'marginBottom': '20px'}),
        dcc.Graph(figure=fig_cm),
        dcc.Graph(figure=fig_report)
    ])


def generate_decision_tree_component(df_clean, model, model_name="Decision Tree"):
    tree = model.tree_
    feature_names = df_clean.drop(columns="Survived").columns.tolist()
    
    def build_tree_layout(tree_obj, node=0, depth=0, x=0.5, y=0.0, width=1.0, nodes_dict=None, edges_list=None):
        if nodes_dict is None:
            nodes_dict = {}
            edges_list = []
            
        is_leaf = tree_obj.children_left[node] == -1 and tree_obj.children_right[node] == -1
        
        if is_leaf:
            class_idx = np.argmax(tree_obj.value[node])
            class_name = 'Überlebt' if class_idx == 1 else 'Nicht überlebt'
            text = f"Klasse:<br>{class_name}"
        else:
            feature = feature_names[tree_obj.feature[node]]
            threshold = tree_obj.threshold[node]
            text = f"{feature}<br><= {threshold:.2f}"
            
        nodes_dict[node] = {
            'id': node,
            'text': text,
            'x': x,
            'y': y,
            'samples': tree_obj.n_node_samples[node],
            'gini': tree_obj.impurity[node],
            'is_leaf': is_leaf,
            'depth': depth
        }
        
        if not is_leaf:
            left_child = tree_obj.children_left[node]
            right_child = tree_obj.children_right[node]
            
            y_next = y - 1.2
            x_left = x - width / 3.5
            x_right = x + width / 3.5
            
            edges_list.append((node, left_child))
            edges_list.append((node, right_child))
            
            build_tree_layout(tree_obj, left_child, depth+1, x_left, y_next, width/2, nodes_dict, edges_list)
            build_tree_layout(tree_obj, right_child, depth+1, x_right, y_next, width/2, nodes_dict, edges_list)
            
        return nodes_dict, edges_list

    nodes_dict, edges_list = build_tree_layout(tree)
    
    fig_tree = go.Figure()
    
    for edge in edges_list:
        parent, child = edge
        fig_tree.add_trace(go.Scatter(
            x=[nodes_dict[parent]['x'], nodes_dict[child]['x']],
            y=[nodes_dict[parent]['y'], nodes_dict[child]['y']],
            mode='lines',
            line=dict(color='#bdc3c7', width=1.5),
            hoverinfo='none',
            showlegend=False
        ))
    
    node_x, node_y, hover_text, node_colors, node_labels = [], [], [], [], []
    
    for node_id, node_info in nodes_dict.items():
        node_x.append(node_info['x'])
        node_y.append(node_info['y'])
        node_labels.append(f"n={node_info['samples']}")
        hover_text.append(f"Details: {node_info['text']}<br>Gini: {node_info['gini']:.3f}<br>Samples: {node_info['samples']}")
        node_colors.append('#e8f0fe' if not node_info['is_leaf'] else '#e6f4ea')
        
    fig_tree.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=45,
            color=node_colors,
            line=dict(color='#1a73e8', width=2)
        ),
        text=node_labels,
        textposition='middle center',
        textfont=dict(size=10, color='black', family='Arial'),
        hovertext=hover_text,
        hoverinfo='text',
        showlegend=False
    ))
    
    for node_id, node_info in nodes_dict.items():
        fig_tree.add_annotation(
            x=node_info['x'],
            y=node_info['y'] + 0.22,
            text=node_info['text'],
            showarrow=False,
            font=dict(size=10, color='black', family='Arial'),
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor="#dcdcdc",
            borderwidth=1,
            borderpad=4
        )

    max_depth = max(n['depth'] for n in nodes_dict.values())
    
    fig_tree.update_layout(
        title=f"Entscheidungsbaum ({model_name}) - Dynamische Visualisierung",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template="plotly_white",
        height=max(650, (max_depth + 1) * 150),
        margin=dict(l=20, r=20, t=80, b=20),
        font=dict(family='Arial, sans-serif')
    )
    
    return html.Div([
        html.H3("Entscheidungsbaum Visualisierung", style={'marginTop': '40px', 'marginBottom': '20px'}),
        dcc.Graph(figure=fig_tree)
    ])
