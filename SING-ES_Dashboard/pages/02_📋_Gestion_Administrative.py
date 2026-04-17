import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import render_bar_chart, render_pie_chart

st.set_page_config(page_title="Gestion Administrative | SING-ES", page_icon="📋", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>📋 Gestion Administrative</h1>
    <p>Administration et gestion des établissements d'enseignement supérieur</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs
total_etablissements = len(data['etablissements'])
accredites = len(data['etablissements'][data['etablissements']['statut_accreditation'] == 'Accrédité'])
en_cours = len(data['etablissements'][data['etablissements']['statut_accreditation'] == 'En cours'])
capacite_totale = data['etablissements']['capacite_totale'].sum()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Établissements", f"{total_etablissements:,}")
with col2:
    st.metric("Accrédités", f"{accredites:,}", f"{accredites/total_etablissements*100:.1f}%" if total_etablissements > 0 else "0%")
with col3:
    st.metric("En cours", f"{en_cours:,}")
with col4:
    st.metric("Capacité Totale", f"{capacite_totale:,}")

st.markdown("---")

# Onglets
tab1, tab2, tab3 = st.tabs(["🏛️ Établissements", "📊 Statuts", "📍 Géographie"])

with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Liste des Établissements")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.multiselect(
            "Type d'établissement",
            options=data['etablissements']['type'].unique(),
            default=data['etablissements']['type'].unique()
        )
    with col2:
        region_filter = st.multiselect(
            "Région",
            options=data['etablissements']['region'].unique(),
            default=data['etablissements']['region'].unique()
        )
    
    # Filtrage
    df_filtered = data['etablissements'][
        (data['etablissements']['type'].isin(type_filter)) &
        (data['etablissements']['region'].isin(region_filter))
    ]
    
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Statut d'Accréditation")
        statut_counts = data['etablissements']['statut_accreditation'].value_counts().reset_index()
        statut_counts.columns = ['Statut', 'Nombre']
        fig = render_pie_chart(statut_counts, 'Statut', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Répartition par Type")
        type_counts = data['etablissements']['type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Nombre']
        fig = render_bar_chart(type_counts, 'Type', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Distribution Géographique")
    
    region_stats = data['etablissements'].groupby('region').agg({
        'id_etablissement': 'count',
        'capacite_totale': ['sum', 'mean']
    }).reset_index()
    region_stats.columns = ['Région', 'Nombre', 'Capacité Totale', 'Capacité Moyenne']
    region_stats = region_stats.sort_values('Nombre', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = render_bar_chart(region_stats, 'Région', 'Nombre', orientation='h', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = render_bar_chart(region_stats, 'Région', 'Capacité Totale', orientation='h', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
