import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import render_bar_chart, render_pie_chart

st.set_page_config(page_title="Ressources Humaines | SING-ES", page_icon="👥", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>👥 Ressources Humaines</h1>
    <p>Gestion des enseignants-chercheurs et personnel académique</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs
total_enseignants = len(data['enseignants'])
permanents = len(data['enseignants'][data['enseignants']['statut'] == 'Permanent'])
contractuels = len(data['enseignants'][data['enseignants']['statut'] == 'Contractuel'])

# Calculer les pourcentages en toute sécurité
pct_permanents = f"{permanents/total_enseignants*100:.1f}%" if total_enseignants > 0 else "0%"
pct_contractuels = f"{contractuels/total_enseignants*100:.1f}%" if total_enseignants > 0 else "0%"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Enseignants", f"{total_enseignants:,}")
with col2:
    st.metric("Permanents", f"{permanents:,}", pct_permanents)
with col3:
    st.metric("Contractuels", f"{contractuels:,}", pct_contractuels)
with col4:
    specialites = data['enseignants']['specialite'].nunique()
    st.metric("Spécialités", f"{specialites}")

st.markdown("---")

# Onglets
tab1, tab2, tab3 = st.tabs(["📊 Grades", "📈 Statuts", "🎓 Spécialités"])

with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Répartition par Grade")
    
    grade_counts = data['enseignants']['grade'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Nombre']
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig = render_bar_chart(grade_counts, 'Grade', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.dataframe(grade_counts, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Statut des Enseignants")
        statut_counts = data['enseignants']['statut'].value_counts().reset_index()
        statut_counts.columns = ['Statut', 'Nombre']
        fig = render_pie_chart(statut_counts, 'Statut', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### Répartition par Statut et Grade")
        # Créer un tableau croisé statut vs grade
        cross_tab = pd.crosstab(data['enseignants']['statut'], data['enseignants']['grade'])
        st.dataframe(cross_tab, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Répartition par Spécialité")
    
    specialite_counts = data['enseignants']['specialite'].value_counts().reset_index()
    specialite_counts.columns = ['Spécialité', 'Nombre']
    specialite_counts = specialite_counts.sort_values('Nombre', ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        fig = render_bar_chart(specialite_counts.head(10), 'Spécialité', 'Nombre', orientation='h', height=400)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = render_pie_chart(specialite_counts.head(8), 'Spécialité', 'Nombre', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tableau détaillé
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Détail des Enseignants")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        grade_filter = st.multiselect(
            "Grade",
            options=data['enseignants']['grade'].unique(),
            default=data['enseignants']['grade'].unique()
        )
    with col2:
        specialite_filter = st.multiselect(
            "Spécialité",
            options=data['enseignants']['specialite'].unique(),
            default=data['enseignants']['specialite'].unique()
        )
    
    df_filtered = data['enseignants'][
        (data['enseignants']['grade'].isin(grade_filter)) &
        (data['enseignants']['specialite'].isin(specialite_filter))
    ]
    
    st.dataframe(df_filtered, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
