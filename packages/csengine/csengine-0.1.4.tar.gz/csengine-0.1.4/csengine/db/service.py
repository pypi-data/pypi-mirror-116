from csengine.service import Service


class ModelService(Service):
    model = None

    async def create(self, **values):
        return await self.model.manager.create(**values)

    async def select(self, filt):
        return await self.model.manager.select(filt)

    async def select_object(self, filt):
        return await self.model.manager.select_object(filt)

    async def get(self, pk):
        return await self.model.manager.get(pk)

    async def save(self, obj):
        return await self.model.manager.save(obj)

    async def select_vos(self, filt):
        return await self.model.manager.select_vos(filt)

    async def select_vo(self, filt):
        return await self.model.manager.select_vo(filt)

    async def get_vo(self, pk=None):
        return await self.model.manager.get_vo(pk)


class DataModelService(ModelService):
    model = None
    data = None
    pk_field = None

    async def select(self, **filt):
        instances = (self.model(**item) for item in self.data)
        for key, value in filt.items():
            instances = filter(lambda dt: getattr(dt, key, None) == value, instances)
        return list(instances)

    async def select_object(self, **filt):
        instances = await self.select(**filt)
        return instances[0] if instances else None

    async def get(self, pk=None):
        pk_field = self.pk_field or self.model.Meta.pk_field
        instances = await self.select(**{pk_field: pk})
        return instances[0] if instances else None

    async def select_vos(self, **filt):
        objects = await self.select(**filt)
        return [obj.dict() for obj in objects]

    async def select_vo(self, **filt):
        instance = await self.select_object(**filt)
        return instance.dict() if instance else None

    async def get_vo(self, pk=None):
        instance = await self.get(pk)
        return instance.dict() if instance else None
