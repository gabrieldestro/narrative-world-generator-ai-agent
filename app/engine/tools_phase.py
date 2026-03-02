from typing import Any, Dict

from app.model.game_state import GameState
from app.tools.create_location import create_location
from app.tools.create_npc import create_npc


def tools_phase(state: Dict[str, Any]):

    tool_calls = state.get("pending_tool_calls", [])

    if not tool_calls:
        return {}

    executor = state["tool_executor"]

    results = []

    for call in tool_calls:
        tool_name = call["name"]
        args = call["arguments"]

        result = executor.execute(tool_name, args)

        results.append(result)

    return {
        "pending_tool_calls": [],
        "scene_log": state["scene_log"] + results
    }