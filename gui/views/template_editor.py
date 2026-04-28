import streamlit as st
import json
from app.api_facade import api_list_templates, api_get_template, api_save_template

DEFAULT_TEMPLATE = {
    "name": "Nome do Mundo",
    "world": {
        "description": "Descrição do mundo",
        "locations": ["Local 1", "Local 2"],
        "history": "História do mundo..."
    },
    "npcs": {
        "npc_1": {
            "name": "Exemplo",
            "description": "Um NPC de exemplo.",
            "location": "Local 1"
        }
    },
    "player_state": {
        "name": "Protagonista",
        "inventory": [],
        "current_location": "Local 1"
    },
    "turn_number": 0,
    "scene_log": []
}

def render():
    st.title("Editor de Templates de Mundo")
    
    templates = api_list_templates()
    options = ["+ Criar Novo Template"] + templates
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Templates")
        selected = st.radio("Selecione um template", options)
        
    with col2:
        st.subheader("Editor")
        
        if selected == "+ Criar Novo Template":
            new_filename = st.text_input("Nome do arquivo", value="novo_mundo.json")
            json_str = json.dumps(DEFAULT_TEMPLATE, indent=4, ensure_ascii=False)
            
            edited_json = st.text_area("JSON do Template", value=json_str, height=500)
            
            if st.button("Criar Template", type="primary"):
                if not new_filename.endswith(".json"):
                    new_filename += ".json"
                    
                try:
                    parsed_data = json.loads(edited_json)
                    api_save_template(new_filename, parsed_data)
                    st.success(f"Template '{new_filename}' criado com sucesso!")
                    st.rerun()
                except json.JSONDecodeError:
                    st.error("Erro de sintaxe no JSON. Verifique a formatação.")
                    
        elif selected:
            data = api_get_template(selected)
            json_str = json.dumps(data, indent=4, ensure_ascii=False)
            
            edited_json = st.text_area("JSON do Template", value=json_str, height=500)
            
            if st.button("Salvar Alterações", type="primary"):
                try:
                    parsed_data = json.loads(edited_json)
                    api_save_template(selected, parsed_data)
                    st.success("Template salvo com sucesso!")
                except json.JSONDecodeError:
                    st.error("Erro de sintaxe no JSON. Verifique a formatação.")
