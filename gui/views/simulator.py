import streamlit as st
from app.api_facade import (
    api_start_simulation, 
    api_process_turn, 
    api_list_templates, 
    api_save_simulation,
    api_list_simulation_saves,
    api_resume_simulation
)

def render():
    st.title("Simulador Interativo")
    
    if "sim_state" not in st.session_state:
        st.session_state.sim_state = None
        
    if st.session_state.sim_state is None:
        st.subheader("Iniciar Simulação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Nova Simulação**")
            templates = api_list_templates()
            if templates:
                selected_template = st.selectbox("Escolha um template", templates, key="new_sim")
                if st.button("Iniciar Novo"):
                    with st.spinner("Inicializando o mundo..."):
                        st.session_state.sim_state = api_start_simulation(selected_template)
                    st.rerun()
            else:
                st.warning("Nenhum template encontrado.")
                
        with col2:
            st.markdown("**Carregar Jogo Salvo**")
            saves = api_list_simulation_saves()
            if saves:
                selected_save = st.selectbox("Escolha um save", saves, key="load_sim")
                if st.button("Carregar Jogo"):
                    with st.spinner("Carregando o save..."):
                        st.session_state.sim_state = api_resume_simulation(selected_save)
                    st.rerun()
            else:
                st.info("Nenhum save encontrado.")
    else:
        state = st.session_state.sim_state
        
        st.subheader(f"Turno: {state.get('turn_number', 0)}")
        st.write(f"**Local Atual:** {state.get('player_state', {}).get('current_location', 'Desconhecido')}")
        
        # Histórico Completo
        st.markdown("### História")
        log_container = st.container(height=400)
        with log_container:
            for log in state.get('scene_log', []):
                # Se for uma ação do jogador (normalmente começam com algo específico, 
                # mas vamos imprimir de forma elegante)
                if log.startswith("Jogador"):
                    st.markdown(f"**{log}**")
                else:
                    st.markdown(log)
                st.markdown("---")
                
        # Ações
        st.markdown("### Sua vez")
        
        col_type, col_input = st.columns([1, 4])
        with col_type:
            action_type = st.selectbox("Ação", ["Agir", "Falar"])
        with col_input:
            action_input = st.text_input("O que você faz/diz?", key="action_input")
            
        if st.button("Enviar", type="primary"):
            if action_input:
                choice_map = {"Agir": "act", "Falar": "speak"}
                payload = {"player_choice_type": choice_map[action_type], "player_content": action_input, "target_npc_id": None}
                with st.spinner("Processando turno... Isso pode levar um minuto."):
                    st.session_state.sim_state = api_process_turn(state, payload)
                st.rerun()
            else:
                st.warning("Por favor, digite uma ação ou fala.")
                    
        st.markdown("<br><br>", unsafe_allow_html=True)
        col3, col4, col5 = st.columns(3)
        with col3:
            if st.button("Apenas Continuar"):
                payload = {"player_choice_type": "continue", "player_content": "", "target_npc_id": None}
                with st.spinner("Avançando a história..."):
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
