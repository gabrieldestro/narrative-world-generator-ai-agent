WORLD_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "move_player",
            "description": "Move o jogador para um local conectado ao atual",
            "parameters": {
                "type": "object",
                "properties": {
                    "to_location": {
                        "type": "string",
                        "description": "Nome do local de destino"
                    }
                },
                "required": ["to_location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_npc",
            "description": "Move um NPC para outro local conectado",
            "parameters": {
                "type": "object",
                "properties": {
                    "npc_id": {"type": "string"},
                    "to_location": {"type": "string"}
                },
                "required": ["npc_id", "to_location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "change_npc_status",
            "description": "Altera o status de um NPC (active ou inactive)",
            "parameters": {
                "type": "object",
                "properties": {
                    "npc_id": {
                        "type": "string",
                        "description": "ID do NPC"
                    },
                    "status": {
                        "type": "string",
                        "description": "Novo status do NPC",
                        "enum": ["active", "inactive"]
                    }
                },
                "required": ["npc_id", "status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_quest",
            "description": "Marca uma quest como completada",
            "parameters": {
                "type": "object",
                "properties": {
                    "quest_id": {"type": "string"}
                },
                "required": ["quest_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_item",
            "description": "Adiciona um item ao inventário do jogador",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"}
                },
                "required": ["item"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_item",
            "description": "Remove um item do inventário do jogador",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"}
                },
                "required": ["item"]
            }
        }
    },
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
                    "description": {"type": "string"},
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
    },
    {
        "type": "function",
        "function": {
            "name": "add_world_fact",
            "description": "Adiciona uma nova informação estrutural ao mundo",
            "parameters": {
                "type": "object",
                "properties": {
                    "fact": {
                        "type": "string",
                        "description": "Nova informação sobre o mundo"
                    }
                },
                "required": ["fact"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_world_fact",
            "description": "Edita uma informação existente sobre o mundo",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Índice da informação a ser editada"
                    },
                    "fact": {
                        "type": "string",
                        "description": "Nova versão da informação"
                    }
                },
                "required": ["index", "fact"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "remove_world_fact",
            "description": "Remove uma informação do mundo que não é mais verdadeira",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Índice da informação a ser removida"
                    }
                },
                "required": ["index"]
            }
        }
    }
]