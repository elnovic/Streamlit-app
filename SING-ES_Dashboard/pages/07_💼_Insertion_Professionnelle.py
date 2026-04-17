import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.charts import render_bar_chart, render_pie_chart

st.set_page_config(page_title="Insertion Professionnelle | SING-ES", page_icon="💼", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>💼 Insertion Professionnelle</h1>
    <p>Suivi de l'emploi et de l'insertion des diplômés</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs
total_enquetes = len(data['insertion'])
if total_enquetes > 0:
    en_emploi = len(data['insertion'][data['insertion']['statut_emploi'].isin(['CDI', 'CDD', 'Auto-entrepreneur'])])
    taux_emploi = (en_emploi / total_enquetes) * 100
    salaire_moyen = data['insertion']['salaire_mensuel_mad'].mean()
    delai_moyen = data['insertion']['delai_insertion_mois'].mean()
else:
    en_emploi = 0
    taux_emploi = 0
    salaire_moyen = 0
    delai_moyen = 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Enquêtes", f"{total_enquetes:,}")
with col2:
    st.metric("Taux d'Emploi", f"{taux_emploi:.1f}%")
with col3:
    st.metric("Salaire Moyen", f"{salaire_moyen:,.0f} MAD" if salaire_moyen > 0 else "N/A")
with col4:
    st.metric("Délai Moyen", f"{delai_moyen:.1f} mois" if delai_moyen > 0 else "N/A")

st.markdown("---")

# Onglets
tab1, tab2, tab3 = st.tabs(["📊 Statuts", "💰 Salaires", "📈 Secteurs"])

with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Répartition par Statut d'Emploi")
    
    statut_counts = data['insertion']['statut_emploi'].value_counts().reset_index()
    statut_counts.columns = ['Statut', 'Nombre']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = render_pie_chart(statut_counts, 'Statut', 'Nombre', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = render_bar_chart(statut_counts, 'Statut', 'Nombre', orientation='h', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Détails
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Détails par Statut")
    
    for statut in statut_counts['Statut'].values:
        count = len(data['insertion'][data['insertion']['statut_emploi'] == statut])
        pct = f"{count/total_enquetes*100:.1f}%" if total_enquetes > 0 else "0%"
        st.metric(statut, f"{count:,}", pct)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Analyse des Salaires")
    
    # Filtrer les données avec salaire
    data_salaire = data['insertion'][data['insertion']['salaire_mensuel_mad'].notna()]
    
    if len(data_salaire) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Distribution des Salaires")
            fig = px.histogram(data_salaire, x='salaire_mensuel_mad', nbins=30, 
                             labels={'salaire_mensuel_mad': 'Salaire (MAD)'})
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Salaire par Secteur")
            salaire_secteur = data_salaire.groupby('secteur')['salaire_mensuel_mad'].mean().reset_index()
            salaire_secteur.columns = ['Secteur', 'Salaire Moyen']
            salaire_secteur = salaire_secteur.sort_values('Salaire Moyen', ascending=False)
            fig = render_bar_chart(salaire_secteur, 'Secteur', 'Salaire Moyen', orientation='h', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques
        st.markdown("### Statistiques des Salaires")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Salaire Moyen", f"{data_salaire['salaire_mensuel_mad'].mean():,.0f} MAD")
        with col2:
            st.metric("Salaire Médian", f"{data_salaire['salaire_mensuel_mad'].median():,.0f} MAD")
        with col3:
            st.metric("Salaire Max", f"{data_salaire['salaire_mensuel_mad'].max():,.0f} MAD")
        with col4:
            st.metric("Salaire Min", f"{data_salaire['salaire_mensuel_mad'].min():,.0f} MAD")
    else:
        st.info("Aucune donnée de salaire disponible")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Répartition par Secteur d'Activité")
    
    # Filtrer les données en emploi
    data_emploi = data['insertion'][data['insertion']['secteur'].notna()]
    
    if len(data_emploi) > 0:
        secteur_counts = data_emploi['secteur'].value_counts().reset_index()
        secteur_counts.columns = ['Secteur', 'Nombre']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = render_pie_chart(secteur_counts, 'Secteur', 'Nombre', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = render_bar_chart(secteur_counts, 'Secteur', 'Nombre', height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Délai d'insertion par secteur
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Délai d'Insertion par Secteur")
        
        delai_secteur = data_emploi[data_emploi['delai_insertion_mois'].notna()].groupby('secteur')['delai_insertion_mois'].mean().reset_index()
        delai_secteur.columns = ['Secteur', 'Délai Moyen (mois)']
        delai_secteur = delai_secteur.sort_values('Délai Moyen (mois)', ascending=True)
        
        fig = render_bar_chart(delai_secteur, 'Secteur', 'Délai Moyen (mois)', orientation='h', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Aucune donnée de secteur disponible")
