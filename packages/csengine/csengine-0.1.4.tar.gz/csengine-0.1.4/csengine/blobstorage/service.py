from typing import Any, Optional

from csengine.service import Service


class BlobStorageService(Service):
    chunk_size_default = 65536

    def __init__(self, provider, name=None, app=None):
        super().__init__(name=name, app=app)
        self._provider = provider

    async def upload(self, data: Any, name: Optional[str] = None, chunk_size: Optional[int] = None):
        return await self._provider.upload(data, name, chunk_size or self.chunk_size_default)

    async def download(self, name: str, dest: str, chunk_size: Optional[int] = None):
        return await self._provider.download(name, dest, chunk_size or self.chunk_size_default)

    async def delete(self, name: str):
        return await self._provider.delete(name)
