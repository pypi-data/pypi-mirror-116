from typing import Optional

from .app import App
from .component import Component
from .observer import Observer, Notification


class Command(Component, Observer):
    def __init__(self, name: Optional[str] = None, app: Optional[App] = None) -> None:
        name = name or self.__class__.__name__[:-len('Command')]
        super().__init__(name=name, app=app)

    async def execute(self, notification: Notification) -> None:
        raise NotImplementedError()

    async def handle_notification(self, notification: Notification) -> None:
        return await self.execute(notification)
