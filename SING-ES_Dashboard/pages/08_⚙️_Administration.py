import streamlit as st
import pandas as pd
from components.charts import render_bar_chart, render_pie_chart

st.set_page_config(page_title="Administration | SING-ES", page_icon="⚙️", layout="wide")

st.markdown("""
<div class="main-header">
    <h1>⚙️ Administration Système</h1>
    <p>Gestion et configuration du système SING-ES</p>
</div>
""", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.error("Veuillez charger les données depuis l'application principale.")
    st.stop()

data = st.session_state.data

# Onglets
tab1, tab2, tab3, tab4 = st.tabs(["📊 Statistiques", "🔧 Configuration", "📁 Données", "ℹ️ Informations"])

with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Statistiques Globales du Système")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎓 Étudiants", f"{len(data['etudiants']):,}")
    with col2:
        st.metric("🏛️ Établissements", f"{len(data['etablissements']):,}")
    with col3:
        st.metric("👨‍🏫 Enseignants", f"{len(data['enseignants']):,}")
    with col4:
        st.metric("🔬 Laboratoires", f"{len(data['laboratoires']):,}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 Publications", f"{len(data['publications']):,}")
    with col2:
        st.metric("💼 Insertions", f"{len(data['insertion']):,}")
    with col3:
        total_capacite = data['etablissements']['capacite_totale'].sum()
        st.metric("🏗️ Capacité Totale", f"{total_capacite:,}")
    with col4:
        budget_total = data['laboratoires']['budget_annuel_mad'].sum()
        st.metric("💰 Budget Recherche", f"{budget_total/1e6:.1f}M MAD")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Récapitulatif
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Récapitulatif par Entité")
    
    recap_data = pd.DataFrame({
        'Entité': ['Établissements', 'Étudiants', 'Enseignants', 'Laboratoires', 'Publications', 'Insertions'],
        'Nombre': [
            len(data['etablissements']),
            len(data['etudiants']),
            len(data['enseignants']),
            len(data['laboratoires']),
            len(data['publications']),
            len(data['insertion'])
        ]
    })
    
    fig = render_bar_chart(recap_data, 'Entité', 'Nombre', height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Configuration du Système")
    
    st.markdown("#### Paramètres Généraux")
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Nom de l'Application", value="SING-ES Dashboard", disabled=True)
        st.text_input("Version", value="1.0.0", disabled=True)
    
    with col2:
        st.text_input("Environnement", value="Production", disabled=True)
        st.text_input("Dernière Mise à Jour", value="2026-04-16", disabled=True)
    
    st.markdown("#### Filtres Actifs")
    
    from config import REGIONS, TYPES_ETABLISSEMENTS, ANNEES_UNIVERSITAIRES
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.multiselect("Régions", options=REGIONS, default=REGIONS[:4])
    with col2:
        st.multiselect("Types d'Établissements", options=TYPES_ETABLISSEMENTS, default=TYPES_ETABLISSEMENTS)
    with col3:
        st.selectbox("Année Universitaire", options=ANNEES_UNIVERSITAIRES, index=len(ANNEES_UNIVERSITAIRES)-1)
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Gestion des Données")
    
    st.markdown("#### Aperçu des Données")
    
    # Afficher un aperçu de chaque dataset
    for key, df in data.items():
        st.markdown(f"##### {key.capitalize()}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre de lignes", f"{len(df):,}")
        with col2:
            st.metric("Nombre de colonnes", f"{len(df.columns)}")
        with col3:
            # Vérifier s'il y a des valeurs nulles
            null_count = df.isnull().sum().sum()
            st.metric("Valeurs nulles", f"{null_count:,}")
        
        with st.expander(f"Voir les 5 premières lignes de {key}"):
            st.dataframe(df.head(), use_container_width=True)
        
        st.markdown("---")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### Informations sur le Système")
    
    st.markdown("""
    #### SING-ES - Système d'Information National de Gestion de l'Enseignement Supérieur
    
    **Description:**
    Tableau de bord décisionnel pour le Ministère de l'Enseignement Supérieur du Royaume du Maroc.
    
    **Fonctionnalités:**
    - 📊 Visualisation des données nationales
    - 🎓 Gestion des étudiants et établissements
    - 👥 Ressources humaines et enseignants-chercheurs
    - 📚 Formations et accréditations
    - 🔬 Recherche scientifique et publications
    - 💼 Insertion professionnelle des diplômés
    - ⚙️ Administration et configuration
    
    **Technologies:**
    - Streamlit (Framework Web)
    - Plotly (Visualisation)
    - Pandas (Manipulation de données)
    - Python 3.x
    
    **Contact:**
    Ministère de l'Enseignement Supérieur, de la Recherche Scientifique et de l'Innovation
    Royaume du Maroc
    
    © 2026 - Tous droits réservés
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
