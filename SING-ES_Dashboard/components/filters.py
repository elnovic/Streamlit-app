import streamlit as st
from config import REGIONS, TYPES_ETABLISSEMENTS, ANNEES_UNIVERSITAIRES, NIVEAUX_FORMATION, GRADES

def render_sidebar_filters(include_annee=True, include_regions=True, include_types=True, 
                           include_niveaux=False, include_grades=False):
    """
    Affiche les filtres dans la sidebar et retourne les valeurs sélectionnées
    """
    filters = {}
    
    st.markdown("### 🔍 Filtres")
    
    if include_annee:
        filters['annee'] = st.selectbox(
            "📅 Année Universitaire",
            options=ANNEES_UNIVERSITAIRES,
            index=len(ANNEES_UNIVERSITAIRES)-1,
            key="filter_annee"
        )
    
    if include_regions:
        filters['regions'] = st.multiselect(
            "📍 Régions",
            options=REGIONS,
            default=REGIONS[:4],
            key="filter_regions"
        )
    
    if include_types:
        filters['types'] = st.multiselect(
            "🏛️ Types d'Établissements",
            options=TYPES_ETABLISSEMENTS,
            default=TYPES_ETABLISSEMENTS,
            key="filter_types"
        )
    
    if include_niveaux:
        filters['niveaux'] = st.multiselect(
            "📚 Niveaux de Formation",
            options=NIVEAUX_FORMATION,
            default=NIVEAUX_FORMATION,
            key="filter_niveaux"
        )
    
    if include_grades:
        filters['grades'] = st.multiselect(
            "👨‍🏫 Grades",
            options=GRADES,
            default=GRADES,
            key="filter_grades"
        )
    
    return filters

def apply_filters(df, filters, col_region='region', col_type='type', col_niveau='niveau', col_grade='grade'):
    """
    Applique les filtres sélectionnés au dataframe
    """
    df_filtered = df.copy()
    
    if 'regions' in filters and filters['regions'] and col_region in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_region].isin(filters['regions'])]
    
    if 'types' in filters and filters['types'] and col_type in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_type].isin(filters['types'])]
    
    if 'niveaux' in filters and filters['niveaux'] and col_niveau in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_niveau].isin(filters['niveaux'])]
    
    if 'grades' in filters and filters['grades'] and col_grade in df_filtered.columns:
        df_filtered = df_filtered[df_filtered[col_grade].isin(filters['grades'])]
    
    return df_filtered