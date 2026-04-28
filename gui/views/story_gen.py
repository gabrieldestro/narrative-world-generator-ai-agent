import streamlit as st
from app.api_facade import api_generate_story, api_list_templates

def render():
    st.title("Gerador de Histórias Automático")
    st.markdown("Selecione um mundo e deixe a IA criar uma história completa.")
    
    templates = api_list_templates()
    if not templates:
        st.warning("Nenhum template encontrado.")
        return
        
    selected_template = st.selectbox("Escolha um template", templates)
    
    if st.button("Gerar História"):
        with st.spinner("A IA está escrevendo a história... Isso pode demorar vários minutos."):
            try:
                final_state = api_generate_story(selected_template)
                st.success("História gerada com sucesso!")
                
                st.markdown("### Resultado Final")
                st.text_area("História", final_state.get("story", "História não encontrada no state."), height=400)
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
