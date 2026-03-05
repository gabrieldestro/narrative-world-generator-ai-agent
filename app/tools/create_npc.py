from app.model.game_state import GameState


def create_npc(
    state: GameState,
    id: str,
    name: str,
    description: str,
    goals: list[str],
    current_location: str,
    status: str
):
    print(f"calling create_npc tool: {id} {name} {description} {goals} {current_location} {status}")

    if id in state["npcs"]:
        return state

    if current_location not in state["world"]["locations"]:
        return state

    state["npcs"][id] = {
        "id": id,
        "name": name,
        "description": description,
        "goals": goals,
        "current_location": current_location,
        "memory": [],
        "status": status
    }

    print(f"NPC criado!")

    return state