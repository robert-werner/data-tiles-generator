import json

from data_tiles_generator.classes.response import Response
from data_tiles_generator.classes.source import Source


class Sources(Response):

    def __init__(self, request_response):
        super().__init__(json.loads(request_response))
        self.sources_root = self.root['response']['sources']

    @property
    def count(self):
        return int(self.sources_root['count'])

    @property
    def page(self):
        return int(self.sources_root['info']['page'])

    @property
    def page_count(self):
        return int(self.sources_root['info']['pagecount'])

    @property
    def page_size(self):
        return int(self.sources_root['info']['pagesize'])

    @property
    def total(self):
        return int(self.sources_root['info']['total'])

    def __iter__(self):
        for item in self.sources_root['items']:
            yield Source(item)
