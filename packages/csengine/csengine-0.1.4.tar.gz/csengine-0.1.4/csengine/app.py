import logging
from typing import Dict, Optional, List

from .command import Command
from .observer import Observable, Notification
from .service import Service
from .view import View

logger = logging.getLogger(__name__)


class App:
    """Facade class initializes and caches native Application, Services (Model component) and
    View Components, and provides a single place to access to them.

    Services expose an API for manipulating the Data Model
    (including data retrieved from remote services).

    View components deal with API Endpoints and UI.
    """
    event_manager_class = Observable

    def __init__(self) -> None:
        self.services: Dict[str, Service] = {}
        self.views: Dict[str, View] = {}
        self.commands: Dict[str, Command] = {}
        self._event_manager = self._create_event_manager()

    def _create_event_manager(self) -> Observable:
        return self.event_manager_class()

    def register_service(self, service: Service) -> Service:
        self.services[service.name] = service
        service.app = self
        return service

    def register_view(self, view: View) -> View:
        self.views[view.name] = view
        view.app = self
        return view

    def register_command(self, command: Command, events: Optional[List[str]] = None) -> Command:
        self.commands[command.name] = command
        command.app = self
        events = events or [command.__class__.__name__[:-len('Command')]]
        for event in events:
            self._event_manager.subscribe(event, command)
        return command

    async def notify(self, notification: Notification) -> None:
        await self._event_manager.notify(notification)

    async def init(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def on_init(self) -> None:
        logger.info('App initializing.')
        for service in self.services.values():
            await service.init()
        for view in self.views.values():
            await view.init()

    async def on_close(self) -> None:
        logger.info('App closing.')
        for service in self.services.values():
            await service.close()
        for view in self.views.values():
            await view.close()
