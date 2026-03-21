from typing import TypedDict

class LocationState(TypedDict):
    id: str
    name: str
    description: str
    connected_to: list[str]
