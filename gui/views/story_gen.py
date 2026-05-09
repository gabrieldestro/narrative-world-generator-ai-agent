import streamlit as st
from app.api_facade import api_generate_story, api_list_templates, api_list_story_saves, api_resume_story

def render():
    st.title("Gerador de Histórias Automático")
    st.markdown("Selecione um mundo e deixe a IA criar uma história completa, ou retome uma geração anterior.")
    
    tab1, tab2 = st.tabs(["Nova História", "Retomar Geração"])
    
    with tab1:
        st.subheader("Nova História")
        templates = api_list_templates()
        if not templates:
            st.warning("Nenhum template encontrado.")
        else:
            selected_template = st.selectbox("Escolha um template", templates, key="new_story")
            
            # Show history
            from app.api_facade import api_get_template
            template_data = api_get_template(selected_template)
            history = template_data.get("history", "")
            if history:
                st.info(f"**Sobre o Mundo:**\n\n{history}")
                
            if st.button("Gerar História", type="primary"):
                with st.spinner("A IA está escrevendo a história... Isso pode demorar vários minutos."):
                    try:
                        final_state = api_generate_story(selected_template)
                        st.success("História gerada com sucesso!")
                        st.session_state.story_result = final_state
                    except Exception as e:
                        st.error(f"Ocorreu um erro: {e}")
                        
    with tab2:
        st.subheader("Retomar Geração")
        saves = api_list_story_saves()
        if not saves:
            st.info("Nenhuma história em andamento encontrada.")
        else:
            selected_save = st.selectbox("Escolha um save", saves, key="resume_story")
            if st.button("Retomar", type="primary"):
                with st.spinner("A IA está retomando a história... Isso pode demorar vários minutos."):
                    try:
                        final_state = api_resume_story(selected_save)
                        st.success("História retomada e concluída com sucesso!")
                        st.session_state.story_result = final_state
                    except Exception as e:
                        st.error(f"Ocorreu um erro: {e}")
                        
    if "story_result" in st.session_state:
        st.markdown("---")
        st.markdown("### Resultado Final")
        st.text_area("História", st.session_state.story_result.get("story", "História não encontrada no state."), height=400)
