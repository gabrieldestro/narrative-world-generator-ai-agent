from app.model.game_state import GameState


def get_locations_context(state: GameState):
    locations_context = ""
    for location in state["world"]["locations"].values():
        locations_context += f"""
            ID: {location['id']}
            Nome: {location['name']}\n
            Descrição: {location['description']}\n
            Locais conectados: {", ".join(location['connected_to'])}
    """
        
    return locations_context