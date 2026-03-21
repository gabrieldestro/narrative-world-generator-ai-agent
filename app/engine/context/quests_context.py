from app.model.game_state import GameState


def get_quests_context(state: GameState):
    quests_context = ""
    for quest in state["quests"].values():
        if quest["status"] == "active":
            quests_context += f"""
                ID: {quest['id']}
                Nome: {quest['name']}
                Descrição: {quest['description']}
                """
            
    return quests_context