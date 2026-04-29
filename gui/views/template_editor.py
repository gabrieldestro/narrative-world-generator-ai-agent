import streamlit as st
import json
import time
from app.api_facade import api_list_templates, api_get_template, api_save_template

DEFAULT_TEMPLATE = {
    "name": "Novo Mundo",
    "additional_info": "",
    "player_state": {
        "name": "Protagonista",
        "current_location": "1",
        "description": "",
        "inventory": [],
        "objective": ""
    },
    "genres": [],
    "quests": {},
    "world": {
        "world_prompt": [],
        "global_events": [],
        "locations": {
            "1": {
                "id": "1",
                "name": "Local Inicial",
                "description": "Um lugar tranquilo.",
                "connected_to": []
            }
        }
    },
    "npcs": {},
    "history": "",
    "simulation_id": None,
    "turn_state": None,
    "scene_log": [],
    "turn_number": 1
}

def init_session(selected_name, is_new=False):
    if "editor_current_file" not in st.session_state or st.session_state.editor_current_file != selected_name:
        st.session_state.editor_current_file = selected_name
        if is_new:
            st.session_state.template_data = json.loads(json.dumps(DEFAULT_TEMPLATE))
        else:
            data = api_get_template(selected_name)
            # Ensure complex structures exist
            if "world" not in data: data["world"] = {}
            if "locations" not in data["world"]: data["world"]["locations"] = {}
            if "npcs" not in data: data["npcs"] = {}
            if "player_state" not in data: data["player_state"] = {}
            st.session_state.template_data = data

def render_editor_form():
    data = st.session_state.template_data
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Mundo", "Locais", "Jogador", "NPCs", "Avançado"])
    
    with tab1:
        st.subheader("Geral e Mundo")
        data["name"] = st.text_input("Nome do Template", value=data.get("name", "Novo Mundo"))
        data["additional_info"] = st.text_area("Informações Adicionais (Regras, Estilo)", value=data.get("additional_info", ""), height=150)
        
        genres_str = ", ".join(data.get("genres", []))
        edited_genres = st.text_input("Gêneros (separados por vírgula)", value=genres_str)
        data["genres"] = [g.strip() for g in edited_genres.split(",") if g.strip()]
        
        st.markdown("---")
        st.markdown("**World Prompts**")
        world = data.get("world", {})
        
        prompts = world.get("world_prompt", [])
        if st.button("➕ Adicionar Prompt", key="add_prompt"):
            prompts.append("Novo evento ou descrição...")
            st.rerun()
            
        prompts_to_delete = []
        for i, prompt in enumerate(prompts):
            col_p1, col_p2 = st.columns([9, 1])
            with col_p1:
                prompts[i] = st.text_input(f"Prompt {i+1}", value=prompt, key=f"prompt_{i}", label_visibility="collapsed")
            with col_p2:
                if st.button("🗑️", key=f"del_prompt_{i}"):
                    prompts_to_delete.append(i)
                    
        for i in sorted(prompts_to_delete, reverse=True):
            prompts.pop(i)
            if prompts_to_delete: st.rerun()
            
        world["world_prompt"] = prompts
        
        events_str = "\n".join(world.get("global_events", []))
        edited_events = st.text_area("Eventos Globais", value=events_str, height=100)
        world["global_events"] = [e.strip() for e in edited_events.split("\n") if e.strip()]
        
        data["history"] = st.text_area("História / Background", value=data.get("history", ""), height=150)
        data["world"] = world

    with tab2:
        st.subheader("Locais (Locations)")
        locations = data["world"].get("locations", {})
        
        # Determine next ID
        existing_loc_ids = [int(loc_id) for loc_id in locations.keys() if loc_id.isdigit()]
        next_loc_id = str(max(existing_loc_ids) + 1) if existing_loc_ids else "1"
        
        if st.button("➕ Adicionar Local", key="add_loc"):
            locations[next_loc_id] = {
                "id": next_loc_id,
                "name": f"Novo Local {next_loc_id}",
                "description": "",
                "connected_to": []
            }
            st.rerun()
            
        locs_to_delete = []
        for loc_id, loc_data in locations.items():
            with st.expander(f"📍 [{loc_id}] {loc_data.get('name', 'Sem Nome')}", expanded=False):
                loc_data["name"] = st.text_input(f"Nome", value=loc_data.get("name", ""), key=f"loc_name_{loc_id}")
                loc_data["description"] = st.text_area(f"Descrição", value=loc_data.get("description", ""), key=f"loc_desc_{loc_id}")
                
                conn_str = ", ".join(loc_data.get("connected_to", []))
                edited_conn = st.text_input(f"Conectado a (IDs separados por vírgula)", value=conn_str, key=f"loc_conn_{loc_id}")
                loc_data["connected_to"] = [c.strip() for c in edited_conn.split(",") if c.strip()]
                
                if st.button(f"🗑️ Remover Local {loc_id}", key=f"del_loc_{loc_id}"):
                    locs_to_delete.append(loc_id)
        
        for loc_id in locs_to_delete:
            del locations[loc_id]
            if locs_to_delete: st.rerun()
            
        data["world"]["locations"] = locations

    with tab3:
        st.subheader("Estado do Jogador")
        player_state = data.get("player_state", {})
        
        player_state["name"] = st.text_input("Nome do Protagonista", value=player_state.get("name", ""))
        player_state["current_location"] = st.text_input("Localização Atual (ID)", value=player_state.get("current_location", "1"))
        player_state["description"] = st.text_area("Descrição Física/Psicológica", value=player_state.get("description", ""))
        player_state["objective"] = st.text_area("Objetivo Principal", value=player_state.get("objective", ""))
        
        inventory_str = "\n".join(player_state.get("inventory", []))
        edited_inventory_str = st.text_area("Inventário (Um item por linha)", value=inventory_str)
        player_state["inventory"] = [item.strip() for item in edited_inventory_str.split("\n") if item.strip()]
        
        data["player_state"] = player_state

    with tab4:
        st.subheader("NPCs")
        npcs = data.get("npcs", {})
        
        # Determine next ID
        existing_npc_ids = [int(npc_id) for npc_id in npcs.keys() if npc_id.isdigit()]
        next_npc_id = str(max(existing_npc_ids) + 1) if existing_npc_ids else "1"
        
        if st.button("➕ Adicionar NPC", key="add_npc"):
            npcs[next_npc_id] = {
                "id": next_npc_id,
                "name": f"Novo NPC {next_npc_id}",
                "description": "",
                "goals": [],
                "current_location": "1",
                "sensitivity": None,
                "memory": [],
                "status": "active"
            }
            st.rerun()
            
        npcs_to_delete = []
        for npc_id, npc_data in npcs.items():
            with st.expander(f"👤 [{npc_id}] {npc_data.get('name', 'Sem Nome')}", expanded=False):
                npc_data["name"] = st.text_input("Nome", value=npc_data.get("name", ""), key=f"npc_name_{npc_id}")
                npc_data["current_location"] = st.text_input("Localização Atual (ID)", value=npc_data.get("current_location", "1"), key=f"npc_loc_{npc_id}")
                npc_data["description"] = st.text_area("Descrição", value=npc_data.get("description", ""), key=f"npc_desc_{npc_id}", height=100)
                
                goals_str = "\n".join(npc_data.get("goals", []))
                edited_goals = st.text_area("Objetivos / Metas (Um por linha)", value=goals_str, key=f"npc_goals_{npc_id}", height=100)
                npc_data["goals"] = [g.strip() for g in edited_goals.split("\n") if g.strip()]
                
                npc_data["status"] = st.text_input("Status", value=npc_data.get("status", "active"), key=f"npc_status_{npc_id}")
                
                if st.button(f"🗑️ Remover NPC {npc_id}", key=f"del_npc_{npc_id}"):
                    npcs_to_delete.append(npc_id)
                    
        for npc_id in npcs_to_delete:
            del npcs[npc_id]
            if npcs_to_delete: st.rerun()
            
        data["npcs"] = npcs

    with tab5:
        st.subheader("Sistema & Estado Avançado")
        
        st.info("O Turn Number é gerenciado automaticamente e iniciará em 1 na simulação.")
        
        quests_str = json.dumps(data.get("quests", {}), indent=4, ensure_ascii=False)
        edited_quests_str = st.text_area("Quests (JSON)", value=quests_str, height=150)
        try:
            data["quests"] = json.loads(edited_quests_str)
        except:
            pass # Keep previous if invalid
            
        scene_log_str = json.dumps(data.get("scene_log", []), indent=4, ensure_ascii=False)
        edited_scene_log_str = st.text_area("Scene Log Inicial (JSON)", value=scene_log_str, height=150)
        try:
            data["scene_log"] = json.loads(edited_scene_log_str)
        except:
            pass
            
        # Ignore simulation_id, turn_state, turn_number but keep them in data
        data["turn_number"] = 1
        if "simulation_id" not in data: data["simulation_id"] = None
        if "turn_state" not in data: data["turn_state"] = None
            
def render():
    st.title("Editor de Templates de Mundo")
    
    templates = api_list_templates()
    options = ["+ Criar Novo Template"] + templates
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Templates")
        selected = st.radio("Selecione um template", options, key="template_selector")
        
    with col2:
        st.subheader("Editor")
        
        if selected == "+ Criar Novo Template":
            init_session("+ Criar Novo Template", is_new=True)
            
            new_filename = st.text_input("Nome do arquivo (ex: novo_mundo.json)", value="novo_mundo.json")
            render_editor_form()
            
            st.markdown("---")
            if st.button("Criar Template", type="primary", use_container_width=True):
                if not new_filename.endswith(".json"):
                    new_filename += ".json"
                api_save_template(new_filename, st.session_state.template_data)
                st.success(f"Template '{new_filename}' criado com sucesso!")
                time.sleep(1)
                st.session_state.editor_current_file = None # Reset session to force reload
                st.rerun()
                    
        elif selected:
            init_session(selected, is_new=False)
            
            render_editor_form()
            
            st.markdown("---")
            if st.button("Salvar Alterações", type="primary", use_container_width=True):
                api_save_template(selected, st.session_state.template_data)
                st.success("Template salvo com sucesso!")
