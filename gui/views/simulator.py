import streamlit as st
from app.api_facade import api_start_simulation, api_process_turn, api_list_templates, api_save_simulation

def render():
    st.title("Simulador Interativo")
    
    if "sim_state" not in st.session_state:
        st.session_state.sim_state = None
        
    if st.session_state.sim_state is None:
        st.subheader("Nova Simulação")
        templates = api_list_templates()
        
        if templates:
            selected_template = st.selectbox("Escolha um template", templates)
            if st.button("Iniciar"):
                with st.spinner("Inicializando o mundo e gerando ferramentas..."):
                    st.session_state.sim_state = api_start_simulation(selected_template)
                st.rerun()
        else:
            st.warning("Nenhum template encontrado em 'worlds/'.")
    else:
        state = st.session_state.sim_state
        
        st.subheader(f"Turno: {state.get('turn_number', 0)}")
        st.write(f"**Local Atual:** {state.get('player_state', {}).get('current_location', 'Desconhecido')}")
        
        # Histórico (Scene Log)
        st.markdown("### Histórico da Cena")
        log_container = st.container(height=300)
        with log_container:
            for log in state.get('scene_log', []):
                st.write(log)
                
        # Ações
        st.markdown("### Suas Ações")
        col1, col2 = st.columns(2)
        
        with col1:
            action_text = st.text_input("O que você faz?")
            if st.button("Agir"):
                if action_text:
                    payload = {"player_choice_type": "act", "player_content": action_text, "target_npc_id": None}
                    with st.spinner("Processando turno..."):
                        st.session_state.sim_state = api_process_turn(state, payload)
                    st.rerun()
                    
        with col2:
            speech_text = st.text_input("O que você diz?")
            if st.button("Falar"):
                if speech_text:
                    payload = {"player_choice_type": "speak", "player_content": speech_text, "target_npc_id": None}
                    with st.spinner("Processando turno..."):
                        st.session_state.sim_state = api_process_turn(state, payload)
                    st.rerun()
                    
        st.markdown("---")
        col3, col4, col5 = st.columns(3)
        with col3:
            if st.button("Apenas Continuar"):
                payload = {"player_choice_type": "continue", "player_content": "", "target_npc_id": None}
                with st.spinner("Processando turno..."):
                    st.session_state.sim_state = api_process_turn(state, payload)
                st.rerun()
        with col4:
            if st.button("Salvar Jogo"):
                api_save_simulation(state)
                st.success("Jogo salvo!")
        with col5:
            if st.button("Encerrar Sessão"):
                st.session_state.sim_state = None
                st.rerun()
