import streamlit as st
import pandas as pd
import os

# Nom de ton fichier
FICHIER_EXCEL = 'Achat.xlsx'

st.set_page_config(page_title="Mes Achats", page_icon="🛒", layout="centered")
st.title("🛒 Gestion de mes Listes d'Achats")

# 1. Fonction pour charger et nettoyer le fichier
def charger_donnees():
    donnees = {}
    if os.path.exists(FICHIER_EXCEL):
        xls = pd.ExcelFile(FICHIER_EXCEL)
        for sheet in xls.sheet_names:
            df = pd.read_excel(FICHIER_EXCEL, sheet_name=sheet)
            
            # Nettoyage des en-têtes décalés pour les onglets Sport et Autre
            if not df.empty and 'Unnamed: 0' in df.columns:
                df.columns = df.iloc[0].fillna('Inconnu')
                df = df[1:].reset_index(drop=True)
            
            # Ajout d'une colonne "Acheté" invisible dans ton Excel de base si elle n'existe pas
            if 'Acheté' not in df.columns:
                df['Acheté'] = False
                
            df = df.fillna("") # Remplacer les cases vides (NaN) par du texte vide
            donnees[sheet] = df
    return donnees

# 2. Fonction pour sauvegarder
def sauvegarder_donnees(donnees_dict):
    with pd.ExcelWriter(FICHIER_EXCEL, engine='openpyxl') as writer:
        for sheet, df in donnees_dict.items():
            df.to_excel(writer, sheet_name=sheet, index=False)

# Chargement en mémoire dans Streamlit
if 'listes' not in st.session_state:
    st.session_state.listes = charger_donnees()

# Interface avec onglets correspondant à ton fichier Excel
onglets = st.tabs(["📚 Livres", "🏃‍♂️ Sport", "📦 Autre"])

# --- ONGLET 1 : LIVRES ---
with onglets[0]:
    df_livre = st.session_state.listes.get('Livre', pd.DataFrame(columns=['Auteur', 'Titre', 'Genre', 'Acheté']))
    
    with st.form("form_livre", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        titre = c1.text_input("Titre")
        auteur = c2.text_input("Auteur")
        genre = c3.text_input("Genre (ex: économie, biographie)")
        
        if st.form_submit_button("Ajouter à la liste") and titre:
            nouveau = pd.DataFrame([{'Auteur': auteur, 'Titre': titre, 'Genre': genre, 'Acheté': False}])
            st.session_state.listes['Livre'] = pd.concat([df_livre, nouveau], ignore_index=True)
            sauvegarder_donnees(st.session_state.listes)
            st.rerun()

    # Affichage des livres non achetés
    for index, row in df_livre[df_livre['Acheté'] == False].iterrows():
        c_box, c_texte = st.columns([0.5, 4])
        if c_box.checkbox("", key=f"livre_{index}"):
            st.session_state.listes['Livre'].at[index, 'Acheté'] = True
            sauvegarder_donnees(st.session_state.listes)
            st.rerun()
        c_texte.write(f"**{row['Titre']}** - {row['Auteur']} *(Genre: {row['Genre']})*")

# --- ONGLET 2 : SPORT ---
with onglets[1]:
    df_sport = st.session_state.listes.get('Sport', pd.DataFrame(columns=['Article', 'Genre', 'Colonne1', 'Acheté']))
    
    with st.form("form_sport", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        article = c1.text_input("Article (ex: Sac étanche)")
        genre = c2.text_input("Pratique (ex: Trek, Randonnée, Vélo)")
        marque = c3.text_input("Marque / Magasin")
        
        if st.form_submit_button("Ajouter à la liste") and article:
            nouveau = pd.DataFrame([{'Article': article, 'Genre': genre, 'Colonne1': marque, 'Acheté': False}])
            st.session_state.listes['Sport'] = pd.concat([df_sport, nouveau], ignore_index=True)
            sauvegarder_donnees(st.session_state.listes)
            st.rerun()

    # Affichage des articles de sport
    for index, row in df_sport[df_sport['Acheté'] == False].iterrows():
        c_box, c_texte = st.columns([0.5, 4])
        if c_box.checkbox("", key=f"sport_{index}"):
            st.session_state.listes['Sport'].at[index, 'Acheté'] = True
            sauvegarder_donnees(st.session_state.listes)
            st.rerun()
        detail = f" - {row['Colonne1']}" if row.get('Colonne1') else ""
        c_texte.write(f"**{row['Article']}** ({row['Genre']}){detail}")

# --- ONGLET 3 : AUTRE ---
with onglets[2]:
    df_autre = st.session_state.listes.get('Autre', pd.DataFrame(columns=['Article', 'Genre', 'Colonne1', 'Acheté']))
    
    with st.form("form_autre", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        article = c1.text_input("Article")
        genre = c2.text_input("Genre")
        detail = c3.text_input("Détails")
        
        if st.form_submit_button("Ajouter à la liste") and article:
            nouveau = pd.DataFrame([{'Article': article, 'Genre': genre, 'Colonne1': detail, 'Acheté': False}])
            st.session_state.listes['Autre'] = pd.concat([df_autre, nouveau], ignore_index=True)
            sauvegarder_donnees(st.session_state.listes)
            st.rerun()

    # Affichage des autres articles
    for index, row in df_autre[df_autre['Acheté'] == False].iterrows():
        c_box, c_texte = st.columns([0.5, 4])
        if c_box.checkbox("", key=f"autre_{index}"):
            st.session_state.listes['Autre'].at[index, 'Acheté'] = True
            sauvegarder_donnees(st.session_state.listes)
            st.rerun()
        detail = f" - {row['Colonne1']}" if row.get('Colonne1') else ""
        c_texte.write(f"**{row['Article']}** - {row['Genre']}{detail}")