"""
SING-ES : Système d'Information National de Gestion de l'Enseignement Supérieur
Tableau de Bord Décisionnel - Ministère de l'Enseignement Supérieur (Maroc)
Design inspiré de la maquette officielle
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Import des modules
from config import THEME, REGIONS, TYPES_ETABLISSEMENTS, ANNEES_UNIVERSITAIRES
from data_simulator import load_all_data

# ---------------------------
# CONFIGURATION DE LA PAGE
# ---------------------------
st.set_page_config(
    page_title="SING-ES | Tableau de Bord",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# CHARGEMENT DU CSS
# ---------------------------
def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            print("✅ CSS loaded successfully")
    except Exception as e:
        print(f"❌ Error loading CSS: {e}")

load_css()

# ---------------------------
# CHARGEMENT DES DONNÉES
# ---------------------------
@st.cache_data
def load_data():
    return load_all_data()

with st.spinner("Chargement des données nationales..."):
    data = load_data()
    st.session_state.data = data

# ---------------------------
# BARRE LATÉRALE
# ---------------------------
with st.sidebar:
    st.markdown("## 🎓 SING-ES")
    st.markdown("#### Ministère de l'Enseignement Supérieur")
    st.markdown("#### de la Recherche et de l'Innovation")
    st.markdown("---")
    
    st.markdown('<p class="sidebar-filter-label">🔍 Filtres</p>', unsafe_allow_html=True)
    
    annee_ref = st.selectbox(
        "Année Universitaire",
        options=ANNEES_UNIVERSITAIRES,
        index=len(ANNEES_UNIVERSITAIRES)-1
    )
    
    regions_sel = st.multiselect(
        "Régions",
        options=REGIONS,
        default=REGIONS[:4]
    )
    
    types_sel = st.multiselect(
        "Types d'Établissements",
        options=TYPES_ETABLISSEMENTS,
        default=TYPES_ETABLISSEMENTS
    )
    
    st.markdown("---")
    st.markdown("### Synthèse Nationale")
    st.metric("Total Étudiants", "1,310,000")
    st.metric("Établissements", "387")
    st.metric("Enseignants", "25,480")
    st.metric("Laboratoires", "1,245")

# ---------------------------
# EN-TÊTE PRINCIPAL
# ---------------------------
st.markdown("""
<div class="main-header">
    <h1>Tableau de Bord</h1>
    <div class="subtitle">Année universitaire 2024-2025</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# KPI CARDS (Style exact de l'image)
# ---------------------------
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">🎓 Étudiants Inscrits</div>
        <div class="kpi-value">131 000</div>
        <div class="kpi-trend up">
            <span class="kpi-trend-icon">↗</span> +8.2% vs année précédente
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">🏛️ Établissements</div>
        <div class="kpi-value">387</div>
        <div class="kpi-trend up">
            <span class="kpi-trend-icon">↗</span> +12 vs année précédente
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">🔬 Laboratoires de Recherche</div>
        <div class="kpi-value">1 245</div>
        <div class="kpi-trend up">
            <span class="kpi-trend-icon">↗</span> +5.4% vs année précédente
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">💼 Taux d'Insertion</div>
        <div class="kpi-value">67%</div>
        <div class="kpi-trend down">
            <span class="kpi-trend-icon">↘</span> -2.1% vs année précédente
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# GRAPHIQUES (Ligne 1)
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("<h3>Évolution des Effectifs Étudiants</h3>", unsafe_allow_html=True)
    
    annees = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
    effectifs = [850000, 920000, 980000, 1050000, 1120000, 1200000, 1310000]
    
    fig = px.area(
        x=annees, y=effectifs,
        labels={'x': '', 'y': ''}
    )
    fig.update_traces(
        line=dict(color='#006633', width=3),
        fillcolor='rgba(0, 102, 51, 0.1)'
    )
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickmode='linear',
            dtick=1,
            gridcolor='#E9ECF2'
        ),
        yaxis=dict(
            gridcolor='#E9ECF2',
            tickformat=','
        ),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Répartition par Région")
    
    regions_data = pd.DataFrame({
        'Région': ['Casablanca-Settat', 'Rabat-Salé-Kénitra', 'Marrakech-Safi', 'Fès-Meknès', 
                   'Tanger-Tétouan', 'Souss-Massa', 'Oriental', 'Béni Mellal'],
        'Étudiants': [320000, 280000, 180000, 160000, 120000, 95000, 80000, 75000]
    })
    
    fig = px.bar(
        regions_data,
        x='Étudiants',
        y='Région',
        orientation='h',
        color='Étudiants',
        color_continuous_scale=['#006633', '#C1272D']
    )
    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        yaxis=dict(autorange="reversed"),
        xaxis=dict(gridcolor='#E9ECF2')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# TABLEAU RECHERCHE
# ---------------------------
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 🔬 Indicateurs de Recherche par Université")

recherche_data = pd.DataFrame({
    'Université': ['Université Mohammed V', 'Université Hassan II', 'Université Cadi Ayyad', 
                   'Université Ibn Zohr', 'Université Sidi Mohamed Ben Abdellah'],
    'Labos': [45, 38, 32, 28, 25],
    'Publications': [1250, 980, 850, 720, 680],
    'Brevets': [23, 18, 15, 12, 10],
    'Budget R&D': ['12.5M MAD', '10.2M MAD', '8.7M MAD', '7.1M MAD', '6.3M MAD']
})

# Conversion en HTML pour un style parfait
table_html = """
<table class="data-table">
    <thead>
        <tr>
            <th>Université</th>
            <th class="numeric">Labos</th>
            <th class="numeric">Publications</th>
            <th class="numeric">Brevets</th>
            <th>Budget R&D</th>
        </tr>
    </thead>
    <tbody>
"""
for _, row in recherche_data.iterrows():
    table_html += f"""
        <tr>
            <td class="university-name">{row['Université']}</td>
            <td class="numeric">{row['Labos']}</td>
            <td class="numeric">{row['Publications']}</td>
            <td class="numeric">{row['Brevets']}</td>
            <td>{row['Budget R&D']}</td>
        </tr>
    """
table_html += """
    </tbody>
</table>
"""
st.markdown(table_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# SECTION INSERTION
# ---------------------------
st.markdown('<div class="content-card">', unsafe_allow_html=True)
st.markdown("### 💼 Insertion Professionnelle des Lauréats")

col1, col2 = st.columns([1, 1.5])

with col1:
    # Donut chart
    labels = ['Emploi stable', 'Emploi temporaire', 'Poursuite d\'études', 'Recherche d\'emploi']
    values = [45, 22, 18, 15]
    colors = ['#006633', '#C1272D', '#D69E2E', '#718096']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values,
        hole=0.65,
        marker=dict(colors=colors),
        textinfo='percent',
        textposition='inside',
        textfont=dict(size=12, color='white', family='Inter')
    )])
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=10, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(family='Inter', size=11)
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Taux d'Insertion par Secteur")
    secteurs = pd.DataFrame({
        'Secteur': ['Informatique', 'Finance', 'Santé', 'Industrie', 'Commerce', 'Éducation'],
        'Taux': [78, 72, 88, 65, 60, 82]
    })
    fig = px.bar(
        secteurs.sort_values('Taux'),
        x='Taux',
        y='Secteur',
        orientation='h',
        color='Taux',
        color_continuous_scale=['#006633', '#C1272D'],
        text='Taux'
    )
    fig.update_traces(texttemplate='%{text}%', textposition='outside')
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=50, t=10, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(range=[0, 100], gridcolor='#E9ECF2'),
        yaxis=dict(gridcolor='#E9ECF2')
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# PIED DE PAGE
# ---------------------------
st.markdown("""
<div class="divider"></div>
<div style="text-align: center; color: #8792A2; font-size: 13px; padding: 20px 0;">
    <strong>SING-ES</strong> — Système d'Information National de Gestion de l'Enseignement Supérieur<br>
    Ministère de l'Enseignement Supérieur, de la Recherche et de l'Innovation — Royaume du Maroc
</div>
""", unsafe_allow_html=True)