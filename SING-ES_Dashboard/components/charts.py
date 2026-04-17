import plotly.express as px
import streamlit as st
from config import THEME

def render_line_chart(data, x, y, title="", height=350, color=None):
    """Graphique en ligne standardisé"""
    fig = px.line(data, x=x, y=y, title=title, markers=True, color=color)
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=16, color=THEME['text_primary'])
    )
    return fig

def render_bar_chart(data, x, y, title="", orientation='v', height=350, color=None):
    """Graphique en barres standardisé"""
    if orientation == 'h':
        fig = px.bar(data, x=y, y=x, title=title, orientation='h', color=color)
    else:
        fig = px.bar(data, x=x, y=y, title=title, color=color)
    
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=16, color=THEME['text_primary'])
    )
    return fig

def render_pie_chart(data, names, values, title="", height=350, hole=0.4):
    """Graphique en camembert/donut standardisé"""
    fig = px.pie(data, names=names, values=values, title=title, hole=hole)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font=dict(size=16, color=THEME['text_primary'])
    )
    return fig

def render_metric_card(label, value, delta=None, delta_color="normal"):
    """Carte de métrique avec style personnalisé"""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)