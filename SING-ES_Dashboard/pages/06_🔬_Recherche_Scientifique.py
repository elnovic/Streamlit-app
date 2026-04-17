import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import render_bar_chart, render_pie_chart, render_line_chart

st.set_page_config(page_title="Recherche Scientifique | SING-ES", page_icon="🔬", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>🔬 Recherche Scientifique</h1>
    <p>Laboratoires, publications et indicateurs de recherche</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# KPIs
total_laboratoires = len(data['laboratoires'])
total_publications = len(data['publications'])
publications_sci = len(data['publications'][data['publications']['type'] == 'Article'])
impact_moyen = data['publications']['impact_factor'].mean()

# Afficher l'impact moyen en toute sécurité
impact_display = f"{impact_moyen:.2f}" if not pd.isna(impact_moyen) else "N/A"

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Laboratoires", f"{total_laboratoires:,}")
with col2:
    st.metric("Publications", f"{total_publications:,}")
with col3:
    st.metric("Articles", f"{publications_sci:,}", f"{publications_sci/total_publications*100:.1f}%" if total_publications > 0 else "0%")
with col4:
    st.metric("Impact Factor Moyen", impact_display)

st.markdown("---")

# Onglets
tab1, tab2, tab3 = st.tabs(["🔬 Laboratoires", "📚 Publications", "📊 Indicateurs"])

with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Laboratoires de Recherche")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Répartition par Domaine")
        domaine_counts = data['laboratoires']['domaine'].value_counts().reset_index()
        domaine_counts.columns = ['Domaine', 'Nombre']
        fig = render_pie_chart(domaine_counts, 'Domaine', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Budget par Laboratoire")
        # Top 10 laboratoires par budget
        top_labos = data['laboratoires'].nlargest(10, 'budget_annuel_mad')
        fig = render_bar_chart(top_labos, 'nom', 'budget_annuel_mad', orientation='h', height=350)
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tableau des laboratoires
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Liste des Laboratoires")
    st.dataframe(data['laboratoires'], use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Publications Scientifiques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Type de Publications")
        type_counts = data['publications']['type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Nombre']
        fig = render_pie_chart(type_counts, 'Type', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Évolution des Publications")
        # Utiliser l'ID pour simuler une évolution (pas de date dans les données)
        pubs_par_type = data['publications']['type'].value_counts().reset_index()
        pubs_par_type.columns = ['Type', 'Nombre']
        fig = render_bar_chart(pubs_par_type, 'Type', 'Nombre', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Publications avec impact factor
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Publications avec Facteur d'Impact")
    
    pubs_impact = data['publications'][data['publications']['impact_factor'].notna()]
    if len(pubs_impact) > 0:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Publications avec Impact", f"{len(pubs_impact):,}")
            st.metric("Impact Moyen", f"{pubs_impact['impact_factor'].mean():.2f}")
        with col2:
            st.metric("Impact Max", f"{pubs_impact['impact_factor'].max():.2f}")
            st.metric("Impact Min", f"{pubs_impact['impact_factor'].min():.2f}")
    
    st.dataframe(pubs_impact, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Indicateurs de Performance")
    
    # Ratio publications par laboratoire
    if total_laboratoires > 0:
        ratio_pubs_lab = total_publications / total_laboratoires
        st.metric("Publications par Laboratoire", f"{ratio_pubs_lab:.1f}")
    
    # Répartition par domaine
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Budget Total par Domaine")
        budget_domaine = data['laboratoires'].groupby('domaine')['budget_annuel_mad'].sum().reset_index()
        budget_domaine.columns = ['Domaine', 'Budget Total']
        budget_domaine = budget_domaine.sort_values('Budget Total', ascending=False)
        fig = render_bar_chart(budget_domaine, 'Domaine', 'Budget Total', orientation='h', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### chercheurs par Domaine")
        chercheurs_domaine = data['laboratoires'].groupby('domaine')['nb_chercheurs'].sum().reset_index()
        chercheurs_domaine.columns = ['Domaine', 'Nb Chercheurs']
        chercheurs_domaine = chercheurs_domaine.sort_values('Nb Chercheurs', ascending=False)
        fig = render_bar_chart(chercheurs_domaine, 'Domaine', 'Nb Chercheurs', orientation='h', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
