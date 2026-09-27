import streamlit as st
from supabase import create_client, Client

# Configuration de la page
st.set_page_config(page_title="Mes Achats", page_icon="🛒", layout="centered")
st.title("🛒 Gestion de mes Listes d'Achats")

# Initialisation du client Supabase depuis les Secrets Streamlit
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["supabase"]["SUPABASE_URL"]
    key = st.secrets["supabase"]["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

# --- FONCTIONS DE BASE DE DONNÉES (Supabase) ---

def charger_articles(categorie: str):
    """Récupère la liste des articles non achetés pour une catégorie donnée."""
    response = (
        supabase.table("achats")
        .select("*")
        .eq("categorie", categorie)
        .eq("achete", False)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data

def ajouter_article(categorie: str, titre: str, auteur_marque: str = "", genre_details: str = ""):
    """Ajoute un nouvel article dans Supabase."""
    supabase.table("achats").insert({
        "categorie": categorie,
        "titre": titre,
        "auteur_marque": auteur_marque,
        "genre_details": genre_details,
        "achete": False
    }).execute()

def marquer_comme_achete(article_id: int):
    """Passe l'article au statut acheté (true)."""
    supabase.table("achats").update({"achete": True}).eq("id", article_id).execute()


# --- INTERFACE UTILISATEUR (Streamlit) ---

onglets = st.tabs(["📚 Livres", "🏃‍♂️ Sport", "📦 Autre"])

# ----------------- ONGLET LIVRES -----------------
with onglets[0]:
    with st.form("form_livre", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        titre = c1.text_input("Titre")
        auteur = c2.text_input("Auteur")
        genre = c3.text_input("Genre (ex: économie, biographie)")
        
        if st.form_submit_button("Ajouter à la liste") and titre:
            ajouter_article("Livre", titre, auteur, genre)
            st.success("Livre ajouté !")
            st.rerun()

    livres = charger_articles("Livre")
    for item in livres:
        c_box, c_texte = st.columns([0.5, 4])
        if c_box.checkbox("", key=f"item_{item['id']}"):
            marquer_comme_achete(item['id'])
            st.rerun()
        
        details = f" - {item['auteur_marque']}" if item['auteur_marque'] else ""
        genre_txt = f" *(Genre: {item['genre_details']})*" if item['genre_details'] else ""
        c_texte.write(f"**{item['titre']}**{details}{genre_txt}")

# ----------------- ONGLET SPORT -----------------
with onglets[1]:
    with st.form("form_sport", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        article = c1.text_input("Article (ex: Sac étanche)")
        pratique = c2.text_input("Pratique")
        marque = c3.text_input("Marque / Magasin")
        
        if st.form_submit_button("Ajouter à la liste") and article:
            ajouter_article("Sport", article, marque, pratique)
            st.success("Article sport ajouté !")
            st.rerun()

    sports = charger_articles("Sport")
    for item in sports:
        c_box, c_texte = st.columns([0.5, 4])
        if c_box.checkbox("", key=f"item_{item['id']}"):
            marquer_comme_achete(item['id'])
            st.rerun()
        
        pratique_txt = f" ({item['genre_details']})" if item['genre_details'] else ""
        marque_txt = f" - {item['auteur_marque']}" if item['auteur_marque'] else ""
        c_texte.write(f"**{item['titre']}**{pratique_txt}{marque_txt}")

# ----------------- ONGLET AUTRE -----------------
with onglets[2]:
    with st.form("form_autre", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        article = c1.text_input("Article")
        genre = c2.text_input("Genre")
        details = c3.text_input("Détails")
        
        if st.form_submit_button("Ajouter à la liste") and article:
            ajouter_article("Autre", article, genre, details)
            st.success("Article ajouté !")
            st.rerun()

    autres = charger_articles("Autre")
    for item in autres:
        c_box, c_texte = st.columns([0.5, 4])
        if c_box.checkbox("", key=f"item_{item['id']}"):
            marquer_comme_achete(item['id'])
            st.rerun()
        
        genre_txt = f" - {item['auteur_marque']}" if item['auteur_marque'] else ""
        detail_txt = f" ({item['genre_details']})" if item['genre_details'] else ""
        c_texte.write(f"**{item['titre']}**{genre_txt}{detail_txt}")
