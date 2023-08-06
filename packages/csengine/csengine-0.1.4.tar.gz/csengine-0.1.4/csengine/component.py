from __future__ import annotations

from typing import Optional

from csengine.app import App


class Component:
    def __init__(self, name: str, app: Optional[App] = None) -> None:
        self.app: Optional[App] = app
        self.name: str = name or self.__class__.__name__

    async def init(self) -> None:
        pass

    async def close(self) -> None:
        pass
