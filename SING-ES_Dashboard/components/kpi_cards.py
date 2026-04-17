import streamlit as st

def render_kpi_card(label, value, trend=None, trend_value=None, icon=None):
    """
    Affiche une carte KPI stylisée
    """
    trend_html = ""
    if trend == "up":
        trend_html = f'<div class="kpi-trend positive">↗ +{trend_value} vs année précédente</div>'
    elif trend == "down":
        trend_html = f'<div class="kpi-trend negative">↘ -{trend_value} vs année précédente</div>'
    elif trend == "neutral":
        trend_html = f'<div class="kpi-trend">→ {trend_value} vs année précédente</div>'
    
    icon_html = f"{icon} " if icon else ""
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{icon_html}{label}</div>
        <div class="kpi-value">{value}</div>
        {trend_html}
    </div>
    """

def render_kpi_grid(kpis):
    """
    Affiche une grille de 4 KPIs
    kpis: liste de dicts avec label, value, trend, trend_value, icon
    """
    cols = st.columns(4)
    for i, kpi in enumerate(kpis[:4]):
        with cols[i]:
            st.markdown(render_kpi_card(**kpi), unsafe_allow_html=True)

def render_metric_row(metrics):
    """
    Affiche une ligne de métriques Streamlit natives
    """
    cols = st.columns(len(metrics))
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(**metric)