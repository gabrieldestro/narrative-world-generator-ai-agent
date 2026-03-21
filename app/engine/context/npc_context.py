from app.model.game_state import GameState


def get_npc_context(state: GameState):
    location = state["player_state"]["current_location"]

    npcs_here = [
        npc for npc in state["npcs"].values()
        if npc["current_location"] == location and npc["status"] == "active"
    ]

    if not npcs_here:
        return state

    npc_context = ""
    for npc in npcs_here:
        npc_context += f"""
        Nome: {npc['name']}
        Descrição: {npc['description']}
        Objetivos: {", ".join(npc['goals'])}
        """

    return npc_context