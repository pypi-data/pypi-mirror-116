import uuid


class ModelManager:

    def __init__(self, model=None, provider=None):
        self._model = model
        self._provider = provider

    def set_model(self, model):
        self._model = model

    def set_provider(self, provider):
        self._provider = provider

    async def create(self, **values):
        raise NotImplementedError()

    async def get(self, pk):
        return await self._provider.get(self._model, pk)

    async def select(self, filt):
        raise NotImplementedError()

    async def select_object(self, **filt):
        objects = await self.select(filt)
        return objects[0] if objects else None

    def wrap(self, values):
        return self._model(**values)

    def generate_key(self, **kwargs):
        return uuid.uuid4().hex


class KVModelManager(ModelManager):

    async def create(self, **values):
        pk = values.get(self._model.Meta.pk_field) or self.generate_key(**values)
        values = dict(values, **{self._model.Meta.pk_field: pk})
        await self._provider.create(self._model, pk, values)
        return self.wrap(values)
