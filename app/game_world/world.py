import uuid

from model.game_state import GameState

def initialize_game() -> GameState:

    tavern_id = str(uuid.uuid4())
    merchant_id = str(uuid.uuid4())

    return {
        "world": {
            "world_prompt": """
            Vila medieval chamada Dunmar.
            Tensões políticas silenciosas.
            Rumores sobre criaturas na floresta.
            Uma ordem secreta atua nas sombras.
            """,
            "global_events": [],
            "locations": {
                "taverna": {
                    "name": "taverna",
                    "description": "Ambiente quente, cheiro de cerveja e madeira."
                },
                "praça": {
                    "name": "praça",
                    "description": "Centro da vila com uma antiga fonte de pedra."
                }
            }
        },
        "npcs": {
            tavern_id: {
                "id": tavern_id,
                "name": "Roderick",
                "personality": "Taverneiro desconfiado, observador e pragmático.",
                "goals": ["Manter a taverna segura", "Descobrir segredos da vila"],
                "current_location": "taverna",
                "memory": [],
                "status": "active"
            },
            merchant_id: {
                "id": merchant_id,
                "name": "Elira",
                "personality": "Mercadora ambiciosa e persuasiva.",
                "goals": ["Expandir negócios", "Descobrir oportunidades lucrativas"],
                "current_location": "praça",
                "memory": [],
                "status": "active"
            }
        },
        "player_location": "taverna",
        "turn_state": None,
        "scene_log": [],
        "turn_number": 1
    }