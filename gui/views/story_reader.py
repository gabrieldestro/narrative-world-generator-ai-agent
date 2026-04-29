import streamlit as st
from app.api_facade import api_list_exported_stories, api_get_exported_story

def render():
    st.title("Leitor de Narrativas")
    st.markdown("Leia as histórias completas geradas pela IA.")
    
    stories = api_list_exported_stories()
    
    if not stories:
        st.warning("Nenhuma história exportada encontrada. Gere uma história primeiro!")
        return
        
    selected_story = st.selectbox("Selecione uma história para ler", stories)
    
    if selected_story:
        content = api_get_exported_story(selected_story)
        if content:
            st.markdown("---")
            st.markdown(f"### Lendo: {selected_story}")
            st.text_area("Conteúdo", value=content, height=600, disabled=True)
            st.markdown("---")
            
            # Optionally, we can add a download button
            st.download_button(
                label="Baixar Arquivo de Texto",
                data=content,
                file_name=selected_story,
                mime="text/plain"
            )
        else:
            st.error("Não foi possível carregar a história.")
