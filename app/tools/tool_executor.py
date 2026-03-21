from typing import Callable, Dict, Any


class ToolExecutor:

    def __init__(self):
        self.tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable):
        self.tools[name] = func

    def execute(self, name: str, args: Dict[str, Any], state):
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not registered.")

        return self.tools[name](state=state, **args)