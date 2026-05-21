import json
from pathlib import Path
import streamlit as st


TASKS_FILE = Path(__file__).with_name("tasks.json")


def charger_taches():
    """Charge les tâches depuis le fichier JSON local dans la session Streamlit."""
    if TASKS_FILE.exists():
        with TASKS_FILE.open("r", encoding="utf-8") as file: # Lire le json depuis le fichier local
            st.session_state["tasks"] = json.load(file)
    else:
        st.session_state["tasks"] = []


def sauvegarder_taches():
    """Enregistre les tâches courantes dans un fichier JSON local."""
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(st.session_state["tasks"], file, ensure_ascii=False, indent=2)


def supprimer_confirmations():
    """Supprime tous les états de confirmation de suppression."""
    for key in list(st.session_state.keys()):
        if key.startswith("confirm_delete_"): # Supprimer les clés de confirmation de suppression
            del st.session_state[key]


def initialiser_taches():
    """Initialise les tâches à partir du stockage local une seule fois par session."""
    if "tasks" not in st.session_state:
        charger_taches()


def ajouter_tache(new_task):
    """Ajoute une tâche à la liste des tâches dans la session Streamlit."""
    cleaned_task = new_task.strip()
    if cleaned_task != "":
        st.session_state["tasks"].append({"task": cleaned_task, "done": False})
        sauvegarder_taches()
        st.rerun()

def afficher_tache():
    """Affiche la liste des tâches dans la session Streamlit."""
    with st.container(height=500): # ajout d'une scrollbar si la liste est trop longue
        for i, t in enumerate(st.session_state["tasks"]):
            col1, col2 = st.columns([0.72, 0.28])
            confirm_key = f"confirm_delete_{i}"
            with col1:
                st.write(("Terminé - " if t["done"] else "À faire - ") + t["task"])
            with col2:
                if st.session_state.get(confirm_key, False):
                    st.caption("Confirmer ?")
                    confirm_col, cancel_col = st.columns(2)
                    with confirm_col:
                        if st.button("Confirmer", key=f"confirm_{i}"):
                            st.session_state["tasks"].pop(i)
                            supprimer_confirmations()
                            sauvegarder_taches()
                            st.rerun() # Rafraîchit l'affichage après suppression
                    with cancel_col:
                        if st.button("Annuler", key=f"cancel_{i}"):
                            st.session_state[confirm_key] = False
                            st.rerun() # Revient à l'affichage normal
                else:
                    done_col, delete_col = st.columns(2)
                    with done_col:
                        if st.button("Terminé", key=f"done_{i}"):
                            st.session_state["tasks"][i]["done"] = True
                            sauvegarder_taches()
                            st.rerun() # Rafraîchit l'affichage après modification
                    with delete_col:
                        if st.button("Supprimer", key=f"delete_{i}"):
                            st.session_state[confirm_key] = True
                            st.rerun() # Affiche la confirmation