from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Any, Optional

from pydantic import BaseModel


class Observer:
    async def handle_notification(self, notification: Notification) -> None:
        raise NotImplementedError()


class Observable:
    def __init__(self) -> None:
        self._observers: Dict[str, List[Observer]] = defaultdict(list)

    def subscribe(self, event: str, observer: Observer) -> None:
        self._observers[event].append(observer)

    async def notify(self, notification: Notification) -> None:
        for observer in self._observers.get(notification.name, []):
            await observer.handle_notification(notification)


class Notification(BaseModel):
    name: str
    body: Optional[Any]  # we can restrict to Dict[str, Any]?
    typ: Optional[str]


class Event(Notification):
    def __init__(__pydantic_self__, **data: Any) -> None:
        data['typ'] = 'Event'
        super().__init__(**data)
