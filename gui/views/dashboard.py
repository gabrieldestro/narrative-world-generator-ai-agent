import streamlit as st

def render():
    st.title("Bem-vindo ao Gerador de Mundos Narrativos 🌍")
    st.markdown("""
    Esta interface gráfica (GUI) foi construída para validar os conceitos do gerador narrativo de forma visual.
    A arquitetura foi projetada com uma camada de **Facade (API)**, permitindo que no futuro esta interface 
    seja facilmente substituída por um Frontend Web moderno (ex: Angular) enquanto a lógica em Python vira um 
    servidor Backend (ex: FastAPI).
    
    ### Navegação
    - **Simulador Interativo**: Permite jogar as simulações turno a turno.
    - **Gerador de Histórias**: Permite gerar narrativas contínuas.
    - **Editor de Templates**: Visualize e edite seus mundos JSON.
    - **Configurações**: Edite seu arquivo `.env` facilmente.
    """)
    st.info("Utilize a barra lateral para navegar.")
