WORLD_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "create_location",
            "description": "Cria um novo local no mundo",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "connected_to": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["name", "description", "connected_to"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_npc",
            "description": "Cria um novo NPC",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "appearance": {"type": "string"},
                    "personality": {"type": "string"},
                    "goals": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "current_location": {"type": "string"},
                    "status": {"type": "string"}
                },
                "required": ["id", "name", "current_location", "status"]
            }
        }
    }
]