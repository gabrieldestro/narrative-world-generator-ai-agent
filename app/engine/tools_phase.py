from typing import Any, Dict

from app.logging.state_logger import log_game_state
from app.model.game_state import GameState
from app.tools.create_location import create_location
from app.tools.create_npc import create_npc


def tools_phase(state: GameState) -> Dict[str, Any]:

    tool_calls = state.get("pending_tool_calls", [])

    if not tool_calls:
        return {}
    
    log_game_state(state)
    executor = state["tool_executor"]

    results = []

    for call in tool_calls:
        tool_name = call["name"]
        args = call["arguments"]

        result = executor.execute(tool_name, args, state)

        results.append(result)

    return {
        "pending_tool_calls": [],
        "scene_log": state["scene_log"] + results
    }