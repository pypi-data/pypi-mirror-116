from elasticsearch import Elasticsearch

from ..provider import BaseESProvider


class ESProvider(BaseESProvider):
    client_class = Elasticsearch

    async def create(self, model, key, values):
        pk = values.get(self._get_pk_field(model))
        self._client.index(index=self._get_index(model), id=pk, body=values)
        return self._wrap(model, values)

    async def save(self, model, obj):
        pk = getattr(obj, self._get_pk_field(model))
        self._client.index(index=self._get_index(model), id=pk, body=obj.dict())
        return obj

    async def get(self, model, key):
        values = self._client.get(self._get_index(model), id=key)['_source']
        return self._wrap(model, values)

    async def get_dict(self, model, pk):
        return self._client.get(self._get_index(model), id=pk)['_source']

    async def select(self, model, query):
        res = self._client.search(index=self._get_index(model), body={"query": query})
        return [self._wrap(model, hit['_source']) for hit in res['hits']['hits']]

    async def select_dict_objects(self, model, query):
        res = self._client.search(index=self._get_index(model), body={"query": query})
        return [hit['_source'] for hit in res['hits']['hits']]
