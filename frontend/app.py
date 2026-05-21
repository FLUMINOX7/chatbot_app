import streamlit as st
from list_functions import afficher_tache, ajouter_tache, initialiser_taches


initialiser_taches()
st.set_page_config(layout="wide")

st.title("Ma TodoList")

# Ajouter une nouvelle tâche
new_task = st.text_input("Ajouter une tâche")
if st.button("Ajouter"):
    ajouter_tache(new_task) # Utilisations de la fonction d'ajout de tâche définie dans list_functions.py

# Afficher les tâches
st.subheader("Liste des tâches")
afficher_tache() # Utilisations de la fonction d'affichage de tâche définie dans list_functions.py  
