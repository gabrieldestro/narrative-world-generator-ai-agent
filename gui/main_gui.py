import sys
import os
import streamlit as st
import time

# Garante que o diretório raiz está no path para importar o modulo app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Gerador de Mundos Narrativos", page_icon="🌍", layout="wide")

st.sidebar.title("🌍 IA Narrativa")
page = st.sidebar.radio("Navegação", [
    "Dashboard", 
    "Simulador Interativo", 
    "Gerador de Histórias", 
    "Leitor de Narrativas",
    "Editor de Templates", 
    "Configurações"
])

with st.spinner(f"Carregando {page}..."):
    # Pequeno delay apenas para a animação do loading ser percebida visualmente, 
    # pois o carregamento local no Streamlit é instantâneo na maioria das vezes.
    time.sleep(0.3)
    
    if page == "Dashboard":
        from gui.views.dashboard import render
        render()
    elif page == "Simulador Interativo":
        from gui.views.simulator import render
        render()
    elif page == "Gerador de Histórias":
        from gui.views.story_gen import render
        render()
    elif page == "Leitor de Narrativas":
        from gui.views.story_reader import render
        render()
    elif page == "Editor de Templates":
        from gui.views.template_editor import render
        render()
    elif page == "Configurações":
        from gui.views.settings import render
        render()
