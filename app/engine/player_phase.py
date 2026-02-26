def player_phase(state):

    print("\nTurno", state["turn_number"])
    print("Local:", state["player_location"])
    print("\n1 - Agir")
    print("2 - Falar")
    print("3 - Não fazer nada")

    choice = input("> ")

    if choice == "1":
        action = input("Descreva sua ação: ")
        state["turn_state"] = {
            "player_choice_type": "act",
            "player_content": action,
            "target_npc_id": None
        }

    elif choice == "2":
        speech = input("O que você quer dizer? ")
        target = input("Para quem? ")

        target_id = None
        for npc_id, npc in state["npcs"].items():
            if npc["name"].lower() == target.lower():
                target_id = npc_id

        state["turn_state"] = {
            "player_choice_type": "speak",
            "player_content": speech,
            "target_npc_id": target_id
        }

    else:
        state["turn_state"] = {
            "player_choice_type": "wait",
            "player_content": "",
            "target_npc_id": None
        }

    return state