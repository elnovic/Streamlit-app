import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components.charts import render_bar_chart, render_pie_chart, render_line_chart

st.set_page_config(page_title="Gestion Étudiants | SING-ES", page_icon="🎓", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>🎓 Gestion des Étudiants</h1>
    <p>Suivi des effectifs, parcours et données démographiques</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs étudiants
total_etudiants = len(data['etudiants'])
nouveaux = len(data['etudiants'][data['etudiants']['annee_inscription'] == '2024-2025'])
feminin = len(data['etudiants'][data['etudiants']['genre'] == 'F'])
etrangers = len(data['etudiants'][data['etudiants']['nationalite'] != 'Marocaine'])

# Prévenir division par zéro dans les pourcentages
if total_etudiants > 0:
    pct_nouveaux = f"{nouveaux/total_etudiants*100:.1f}%"
    pct_feminin = f"{feminin/total_etudiants*100:.1f}%"
else:
    pct_nouveaux = "0.0%"
    pct_feminin = "0.0%"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Étudiants", f"{total_etudiants:,}")
with col2:
    st.metric("Nouveaux Inscrits", f"{nouveaux:,}", pct_nouveaux)
with col3:
    st.metric("Étudiantes", f"{feminin:,}", pct_feminin)
with col4:
    st.metric("Étudiants Étrangers", f"{etrangers:,}")

st.markdown("---")

# Onglets
tab1, tab2, tab3 = st.tabs(["📊 Démographie", "📈 Parcours", "💰 Bourses"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("#### Pyramide des Âges")
        # Simulation d'âges
        ages = pd.DataFrame({
            'Âge': list(range(18, 31)),
            'Hommes': [12000, 15000, 18000, 20000, 22000, 21000, 19000, 17000, 15000, 13000, 11000, 9000, 7000],
            'Femmes': [13000, 16000, 19000, 21000, 23000, 22000, 20000, 18000, 16000, 14000, 12000, 10000, 8000]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(y=ages['Âge'], x=ages['Hommes'], name='Hommes', orientation='h', marker_color='#006233'))
        fig.add_trace(go.Bar(y=ages['Âge'], x=-ages['Femmes'], name='Femmes', orientation='h', marker_color='#C1272D'))
        fig.update_layout(barmode='relative', height=400, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("#### Répartition par Nationalité")
        # Préparer proprement le dataframe pour le camembert
        nat_counts = data['etudiants']['nationalite'].value_counts().reset_index(name='count').head(6)
        # nat_counts a maintenant les colonnes ['nationalite', 'count']
        fig = render_pie_chart(nat_counts, 'nationalite', 'count', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("#### Répartition par Niveau de Formation")
    
    niveau_counts = data['etudiants']['niveau'].value_counts().reset_index()
    niveau_counts.columns = ['Niveau', 'Effectif']
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = render_bar_chart(niveau_counts, 'Niveau', 'Effectif', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(niveau_counts, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("#### Gestion des Bourses")
    
    # Données simulées
    bourses_data = pd.DataFrame({
        'Type de Bourse': ['Mérite', 'Sociale', 'Excellence', 'Coopération', 'Spécifique'],
        'Nombre': [15000, 45000, 5000, 8000, 12000],
        'Montant Moyen (MAD)': [3000, 2000, 5000, 4000, 2500]
    })
    
    col1, col2 = st.columns(2)
    with col1:
        fig = render_pie_chart(bourses_data, 'Type de Bourse', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = render_bar_chart(bourses_data, 'Type de Bourse', 'Montant Moyen (MAD)', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### Détail des Bourses")
    st.dataframe(bourses_data, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)