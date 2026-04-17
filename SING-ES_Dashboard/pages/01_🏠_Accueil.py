import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.charts import render_bar_chart, render_pie_chart, render_line_chart

st.set_page_config(page_title="Accueil | SING-ES", page_icon="🏠", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>🏠 Accueil - Tableau de Bord National</h1>
    <p>Vue d'ensemble du Système d'Information National de Gestion de l'Enseignement Supérieur</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs principaux
total_etudiants = len(data['etudiants'])
total_etablissements = len(data['etablissements'])
total_enseignants = len(data['enseignants'])
total_laboratoires = len(data['laboratoires'])
total_publications = len(data['publications'])

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎓 Étudiants", f"{total_etudiants:,}")
with col2:
    st.metric("🏛️ Établissements", f"{total_etablissements:,}")
with col3:
    st.metric("👨‍🏫 Enseignants", f"{total_enseignants:,}")
with col4:
    st.metric("🔬 Laboratoires", f"{total_laboratoires:,}")
with col5:
    st.metric("📚 Publications", f"{total_publications:,}")

st.markdown("---")

# Graphiques principaux
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Évolution des Effectifs Étudiants")
    annees = list(range(2018, 2026))
    effectifs = [850000, 920000, 980000, 1050000, 1120000, 1200000, 1310000, total_etudiants]
    df_evol = pd.DataFrame({'Année': annees, 'Effectif': effectifs})
    fig = render_line_chart(df_evol, 'Année', 'Effectif', height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Répartition par Région")
    region_counts = data['etablissements']['region'].value_counts().reset_index()
    region_counts.columns = ['Région', 'Nombre']
    fig = render_bar_chart(region_counts.head(10), 'Région', 'Nombre', orientation='h', height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Répartition par type d'établissement
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🏛️ Types d'Établissements")
    type_counts = data['etablissements']['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Nombre']
    fig = render_pie_chart(type_counts, 'Type', 'Nombre', height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Répartition par Genre")
    genre_counts = data['etudiants']['genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Nombre']
    fig = render_pie_chart(genre_counts, 'Genre', 'Nombre', height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tableau récapitulatif
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 📋 Résumé des Établissements par Région")
resume = data['etablissements'].groupby('region').agg({
    'id_etablissement': 'count',
    'capacite_totale': 'sum'
}).reset_index()
resume.columns = ['Région', 'Nombre Établissements', 'Capacité Totale']
resume = resume.sort_values('Nombre Établissements', ascending=False)
st.dataframe(resume, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
