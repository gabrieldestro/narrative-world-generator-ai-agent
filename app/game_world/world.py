import uuid

from app.model.game_state import GameState

def initialize_world() -> GameState:

    tavern_id = str(uuid.uuid4())
    merchant_id = str(uuid.uuid4())

    return {
        "name": "Aventuras na vila Dunmar",
        "player_state": {
            "name": "Stranger",
            "current_location": "praça",
            "description": "Um aventureiro de olhos castanhos e cabelos castanhos."
        },
        "genres": ["aventura", "ação"],
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
                    "description": "Ambiente quente, cheiro de cerveja e madeira.",
                    "connected_to": ["praça"]
                },
                "praça": {
                    "name": "praça",
                    "description": "Centro da vila com uma antiga fonte de pedra.",
                    "connected_to": ["taverna"]
                }
            }
        },
        "npcs": {
            tavern_id: {
                "id": tavern_id,
                "name": "Roderick",
                "appearance": "",
                "personality": "Taverneiro desconfiado, observador e pragmático.",
                "goals": ["Manter a taverna segura", "Descobrir segredos da vila"],
                "current_location": "taverna",
                "memory": [],
                "status": "active"
            },
            merchant_id: {
                "id": merchant_id,
                "name": "Elira",
                "appearance": "",
                "personality": "Mercadora ambiciosa e persuasiva.",
                "goals": ["Expandir negócios", "Descobrir oportunidades lucrativas"],
                "current_location": "praça",
                "memory": [],
                "status": "active"
            }
        },
        "turn_state": None,
        "scene_log": [],
        "turn_number": 1
    }