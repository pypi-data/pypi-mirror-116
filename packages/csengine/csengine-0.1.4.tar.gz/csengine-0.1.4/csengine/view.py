from typing import Optional, Any

from .app import App
from .component import Component


class View(Component):
    def __init__(self, name: Optional[str] = None, app: Optional[App] = None) -> None:
        name = name or self.__class__.__name__[:-len('View')]
        super().__init__(name=name, app=app)


class Action:
    def __init__(self, view: View) -> None:
        self.view: View = view
        assert view.app
        self.app: App = view.app

    async def execute(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()
