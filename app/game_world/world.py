import uuid

from app.model.game_state import GameState

DEFAULT_WORLD = {
        "name": "Aventuras na vila Dunmar",
        "additional_info": "Nenhuma",
        "player_state": {
            "name": "Stranger",
            "current_location": "praça",
            "description": "Um aventureiro de olhos castanhos e cabelos castanhos.",
            "inventory": []
        },
        "genres": ["aventura", "ação"],
        "quests": {},
        "world": {
            "world_prompt": [
                "Vila medieval chamada Dunmar.",
                "Tensões políticas silenciosas.",
                "Rumores sobre criaturas na floresta.",
                "Uma ordem secreta atua nas sombras."
            ],
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
            "1": {
                "id": "1",
                "name": "Roderick",
                "description": "Taverneiro desconfiado, observador e pragmático.",
                "goals": ["Manter a taverna segura", "Descobrir segredos da vila"],
                "current_location": "taverna",
                "memory": [],
                "status": "active"
            },
            "2": {
                "id": "2",
                "name": "Elira",
                "description": "Mercadora ambiciosa e persuasiva.",
                "goals": ["Expandir negócios", "Descobrir oportunidades lucrativas"],
                "current_location": "praça",
                "memory": [],
                "status": "active"
            }
        },
        "turn_state": None,
        "scene_log": [],
        "turn_number": 1,
        "tool_executor": None
    }

def initialize_world() -> GameState:
    return DEFAULT_WORLD