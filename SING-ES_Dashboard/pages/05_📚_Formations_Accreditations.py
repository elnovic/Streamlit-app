import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import render_bar_chart, render_pie_chart

st.set_page_config(page_title="Formations & Accréditations | SING-ES", page_icon="📚", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>📚 Formations & Accréditations</h1>
    <p>Suivi des programmes de formation et processus d'accréditation</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs
total_etudiants = len(data['etudiants'])
niveaux = data['etudiants']['niveau'].nunique()
licences = len(data['etudiants'][data['etudiants']['niveau'] == 'Licence'])
masters = len(data['etudiants'][data['etudiants']['niveau'] == 'Master'])
doctorats = len(data['etudiants'][data['etudiants']['niveau'] == 'Doctorat'])

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Étudiants", f"{total_etudiants:,}")
with col2:
    st.metric("Niveaux", f"{niveaux}")
with col3:
    st.metric("Licences", f"{licences:,}", f"{licences/total_etudiants*100:.1f}%" if total_etudiants > 0 else "0%")
with col4:
    st.metric("Masters", f"{masters:,}", f"{masters/total_etudiants*100:.1f}%" if total_etudiants > 0 else "0%")
with col5:
    st.metric("Doctorats", f"{doctorats:,}", f"{doctorats/total_etudiants*100:.1f}%" if total_etudiants > 0 else "0%")

st.markdown("---")

# Onglets
tab1, tab2, tab3 = st.tabs(["📊 Niveaux", "📈 Répartition", "🎯 Accréditations"])

with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Répartition par Niveau de Formation")
    
    niveau_counts = data['etudiants']['niveau'].value_counts().reset_index()
    niveau_counts.columns = ['Niveau', 'Effectif']
    niveau_counts = niveau_counts.sort_values('Effectif', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = render_bar_chart(niveau_counts, 'Niveau', 'Effectif', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = render_pie_chart(niveau_counts, 'Niveau', 'Effectif', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tableau détaillé
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Détail par Niveau")
    
    for niveau in niveau_counts['Niveau'].values:
        count = len(data['etudiants'][data['etudiants']['niveau'] == niveau])
        pct = f"{count/total_etudiants*100:.1f}%" if total_etudiants > 0 else "0%"
        st.metric(f"{niveau}", f"{count:,}", pct)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Répartition par Année d'Inscription")
    
    annee_counts = data['etudiants']['annee_inscription'].value_counts().sort_index().reset_index()
    annee_counts.columns = ['Année', 'Effectif']
    
    fig = render_bar_chart(annee_counts, 'Année', 'Effectif', height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Répartition par Genre")
        genre_counts = data['etudiants']['genre'].value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Nombre']
        fig = render_pie_chart(genre_counts, 'Genre', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Répartition par Nationalité")
        nat_counts = data['etudiants']['nationalite'].value_counts().reset_index()
        nat_counts.columns = ['Nationalité', 'Nombre']
        fig = render_pie_chart(nat_counts.head(8), 'Nationalité', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Statut d'Accréditation des Établissements")
    
    accreditation_counts = data['etablissements']['statut_accreditation'].value_counts().reset_index()
    accreditation_counts.columns = ['Statut', 'Nombre']
    
    col1, col2 = st.columns(2)
    with col1:
        fig = render_pie_chart(accreditation_counts, 'Statut', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = render_bar_chart(accreditation_counts, 'Statut', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tableau des établissements par accréditation
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Établissements par Statut d'Accréditation")
    
    statut_filter = st.selectbox(
        "Filtrer par statut",
        options=data['etablissements']['statut_accreditation'].unique()
    )
    
    df_filtered = data['etablissements'][data['etablissements']['statut_accreditation'] == statut_filter]
    st.dataframe(df_filtered[['nom', 'type', 'region', 'statut_accreditation']], use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
