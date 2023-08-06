from typing import Optional

from .app import App
from .component import Component


class Service(Component):
    def __init__(self, name: Optional[str] = None, app: Optional[App] = None) -> None:
        name = name or self.__class__.__name__[:-len('Service')]
        super().__init__(name=name, app=app)
