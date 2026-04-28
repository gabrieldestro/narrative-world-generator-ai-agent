import streamlit as st
from app.api_facade import api_get_env, api_update_env

def render():
    st.title("Configurações do Sistema")
    st.markdown("Gerencie as variáveis de ambiente sem precisar editar o arquivo `.env` manualmente.")
    
    env_vars = api_get_env()
    
    with st.form("settings_form"):
        st.subheader("Configurações da Inteligência Artificial")
        
        # Provider
        current_provider = env_vars.get("PROVIDER_NAME", "local")
        provider_options = ["local", "openai"]
        provider_index = provider_options.index(current_provider) if current_provider in provider_options else 0
        provider_name = st.selectbox("Provedor LLM (PROVIDER_NAME)", provider_options, index=provider_index)
        
        # Base URL & Model Name
        llm_model = st.text_input("Nome do Modelo (LLM_MODEL)", value=env_vars.get("LLM_MODEL", "gpt-4o-mini"))
        base_url = st.text_input("URL Base da API (BASE_URL)", value=env_vars.get("BASE_URL", ""))
        temperature = st.number_input("Temperatura (TEMPERATURE)", min_value=0.0, max_value=2.0, value=float(env_vars.get("TEMPERATURE", "0.7") or 0.7), step=0.1)

        # Token
        st.markdown("---")
        st.subheader("Autenticação")
        st.caption("O token só é obrigatório se estiver usando a OpenAI ou outros serviços externos pagos.")
        token = st.text_input("Token da API (TOKEN)", value=env_vars.get("TOKEN", ""), type="password")

        st.markdown("---")
        st.subheader("Configurações de Simulação")
        
        sim_type_val = env_vars.get("SIMULATION_TYPE", "1")
        sim_type = st.selectbox("Tipo de Simulação (SIMULATION_TYPE)", ["LITE (0)", "COMPLETE (1)"], index=0 if str(sim_type_val) == "0" else 1)
            
        auto_play_val = env_vars.get("AUTO_PLAY", "0")
        auto_play = st.selectbox("Modo Espectador / Auto Play (AUTO_PLAY)", ["Desligado (0)", "Ligado (1)"], index=0 if str(auto_play_val) == "0" else 1)
            
        debug_val = env_vars.get("DEBUG", "0")
        debug_mode = st.selectbox("Modo Debug de Logs (DEBUG)", ["Desligado (0)", "Ligado (1)"], index=0 if str(debug_val) == "0" else 1)

        st.markdown("---")
        st.subheader("Gerador de Histórias Longevas")
        chapter_parts = st.number_input("Partes por Capítulo (STORY_CHAPTER_PARTS)", min_value=1, value=int(env_vars.get("STORY_CHAPTER_PARTS", "3") or 3))
        
        # Botão único de Salvar
        submitted = st.form_submit_button("Salvar Todas as Configurações", type="primary", use_container_width=True)
        
        if submitted:
            # Salva todas as variáveis
            api_update_env("PROVIDER_NAME", provider_name)
            api_update_env("LLM_MODEL", llm_model)
            api_update_env("BASE_URL", base_url)
            api_update_env("TEMPERATURE", str(temperature))
            api_update_env("TOKEN", token)
            
            api_update_env("SIMULATION_TYPE", "0" if "0" in sim_type else "1")
            api_update_env("AUTO_PLAY", "0" if "0" in auto_play else "1")
            api_update_env("DEBUG", "0" if "0" in debug_mode else "1")
            
            api_update_env("STORY_CHAPTER_PARTS", str(chapter_parts))
            
            st.success("Todas as configurações foram salvas com sucesso no `.env`!")
