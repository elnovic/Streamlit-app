"""
Générateur de données réalistes pour SING-ES
Basé sur des ordres de grandeur réels de l'enseignement supérieur marocain
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Graine aléatoire fixe pour reproductibilité
np.random.seed(42)
random.seed(42)

# Import des constantes (sans Streamlit pour éviter les problèmes)
REGIONS = [
    "Tanger-Tétouan-Al Hoceïma", "Oriental", "Fès-Meknès", "Rabat-Salé-Kénitra",
    "Béni Mellal-Khénifra", "Casablanca-Settat", "Marrakech-Safi", "Drâa-Tafilalet",
    "Souss-Massa", "Guelmim-Oued Noun", "Laâyoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab"
]

TYPES_ETABLISSEMENTS = ["Université Publique", "École Supérieure Publique", "Établissement Privé", "Institut Spécialisé"]
NIVEAUX_FORMATION = ["Licence", "Master", "Doctorat", "Ingénieur", "Technicien Spécialisé"]
GRADES = ["Professeur de l'Enseignement Supérieur", "Professeur Habilité", "Maître de Conférences", "Professeur Assistant", "Vacataire"]
ANNEES_UNIVERSITAIRES = ["2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"]

def generate_etablissements(n=400):
    """Génère le référentiel des établissements"""
    data = []
    for i in range(n):
        region = random.choice(REGIONS)
        type_etab = random.choice(TYPES_ETABLISSEMENTS)
        
        if "Université" in type_etab:
            nom = f"Université {random.choice(['Mohammed V', 'Hassan II', 'Cadi Ayyad', 'Ibn Zohr', 'Sidi Mohamed Ben Abdellah', 'Chouaib Doukkali', 'Moulay Ismaïl', 'Ibn Tofaïl', 'Sultan Moulay Slimane'])}"
            capacite = random.randint(15000, 80000)
        elif "École" in type_etab:
            nom = f"{random.choice(['ENSAM', 'ENSA', 'ENCG', 'EST', 'FST', 'FSJES', 'ENSIAS', 'INPT'])} - {region.split('-')[0]}"
            capacite = random.randint(1000, 8000)
        else:
            nom = f"{random.choice(['Mundiapolis', 'HEC Maroc', 'EMSI', 'Sup Management', 'UIC', 'AIC'])} - {region.split('-')[0]}"
            capacite = random.randint(500, 5000)
            
        data.append({
            "id_etablissement": f"ETAB-{i+1:04d}",
            "nom": nom,
            "type": type_etab,
            "region": region,
            "ville": region.split('-')[0],
            "capacite_totale": capacite,
            "statut_accreditation": random.choice(["Accrédité", "Accréditation conditionnelle", "En cours"])
        })
    return pd.DataFrame(data)

def generate_etudiants(df_etablissements, n=50000):
    """Génère les données étudiants avec cohérence par établissement"""
    data = []
    for _, etab in df_etablissements.iterrows():
        nb_etudiants = min(etab['capacite_totale'] // 3, random.randint(100, 5000))
        for _ in range(nb_etudiants):
            if len(data) >= n:
                break
            genre = random.choice(["M", "F"])
            data.append({
                "id_etudiant": f"ETU-{len(data)+1:06d}",
                "cne": f"{random.randint(10, 20)}{random.randint(100000, 999999)}",
                "genre": genre,
                "nationalite": "Marocaine" if random.random() < 0.94 else random.choice(["Française", "Sénégalaise", "Ivoirienne", "Tunisienne"]),
                "id_etablissement": etab['id_etablissement'],
                "niveau": random.choice(NIVEAUX_FORMATION),
                "annee_inscription": random.choice(ANNEES_UNIVERSITAIRES)
            })
        if len(data) >= n:
            break
    return pd.DataFrame(data)

def generate_enseignants(df_etablissements, n=15000):
    """Génère les données des enseignants-chercheurs"""
    data = []
    for _, etab in df_etablissements.iterrows():
        nb_enseignants = max(10, etab['capacite_totale'] // 100)
        for _ in range(nb_enseignants):
            if len(data) >= n:
                break
            data.append({
                "id_enseignant": f"ENS-{len(data)+1:05d}",
                "grade": random.choice(GRADES),
                "specialite": random.choice(["Informatique", "Mathématiques", "Physique", "Chimie", "Biologie", "Économie", "Droit", "Littérature", "Médecine", "Ingénierie"]),
                "id_etablissement": etab['id_etablissement'],
                "statut": "Permanent" if random.random() < 0.8 else "Contractuel"
            })
        if len(data) >= n:
            break
    return pd.DataFrame(data)

def generate_laboratoires(df_etablissements, n=800):
    """Génère les laboratoires de recherche"""
    data = []
    for _, etab in df_etablissements.iterrows():
        nb_labos = random.randint(0, 5) if "Université" in etab['type'] else random.randint(0, 2)
        for _ in range(nb_labos):
            data.append({
                "id_laboratoire": f"LAB-{len(data)+1:04d}",
                "nom": f"Laboratoire de {random.choice(['Recherche en', 'Études', 'Ingénierie des', 'Sciences de'])} {random.choice(['Informatique', 'Mathématiques', 'Physique', 'Biotechnologie', 'Énergies Renouvelables', 'Intelligence Artificielle'])}",
                "id_etablissement": etab['id_etablissement'],
                "domaine": random.choice(["Sciences Exactes", "Sciences de l'Ingénieur", "Sciences de la Vie", "Sciences Humaines", "Sciences Économiques"]),
                "nb_chercheurs": random.randint(5, 50),
                "budget_annuel_mad": random.randint(100000, 5000000)
            })
    return pd.DataFrame(data)

def generate_publications(df_laboratoires, n=5000):
    """Génère les publications scientifiques"""
    data = []
    types_pub = ["Article", "Conférence", "Thèse", "Brevets", "Livre"]
    for _, labo in df_laboratoires.iterrows():
        nb_pubs = random.randint(0, 20)
        for _ in range(nb_pubs):
            data.append({
                "id_publication": f"PUB-{len(data)+1:05d}",
                "titre": f"Étude sur {random.choice(['les algorithmes', 'les matériaux', 'le climat', 'l\'économie', 'la santé'])}",
                "id_laboratoire": labo['id_laboratoire'],
                "type": random.choice(types_pub),
                "impact_factor": round(random.uniform(0.5, 8.0), 2) if random.random() < 0.7 else None
            })
    return pd.DataFrame(data)

def generate_insertion(df_etudiants, n=20000):
    """Génère les données d'insertion professionnelle"""
    data = []
    statuts = ["CDI", "CDD", "Stage", "Auto-entrepreneur", "Poursuite d'études", "Recherche d'emploi"]
    secteurs = ["IT", "Finance", "Industrie", "Éducation", "Santé", "Commerce", "Administration", "BTP"]
    
    for _, etudiant in df_etudiants.sample(n=min(n, len(df_etudiants))).iterrows():
        statut = random.choice(statuts)
        en_emploi = statut in ["CDI", "CDD", "Auto-entrepreneur"]
        data.append({
            "id_etudiant": etudiant['id_etudiant'],
            "statut_emploi": statut,
            "secteur": random.choice(secteurs) if en_emploi else None,
            "delai_insertion_mois": random.randint(1, 18) if en_emploi else None,
            "salaire_mensuel_mad": random.randint(4000, 20000) if en_emploi else None
        })
    return pd.DataFrame(data)

def load_all_data():
    """Charge toutes les données simulées"""
    print("Génération des établissements...")
    df_etablissements = generate_etablissements(n=300)
    
    print("Génération des étudiants...")
    df_etudiants = generate_etudiants(df_etablissements, n=50000)
    
    print("Génération des enseignants...")
    df_enseignants = generate_enseignants(df_etablissements, n=15000)
    
    print("Génération des laboratoires...")
    df_laboratoires = generate_laboratoires(df_etablissements, n=800)
    
    print("Génération des publications...")
    df_publications = generate_publications(df_laboratoires, n=5000)
    
    print("Génération des données d'insertion...")
    df_insertion = generate_insertion(df_etudiants, n=20000)
    
    return {
        "etablissements": df_etablissements,
        "etudiants": df_etudiants,
        "enseignants": df_enseignants,
        "laboratoires": df_laboratoires,
        "publications": df_publications,
        "insertion": df_insertion
    }