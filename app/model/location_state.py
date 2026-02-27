from typing import TypedDict

class LocationState(TypedDict):
    name: str
    description: str
    connected_to: list[str]
