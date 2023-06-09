from datetime import datetime

from shapely.geometry import shape


class Source:

    def __init__(self, source_dict):
        self._source = source_dict
        self.has_geo = bool(self.location)

    @property
    def meteo_range(self):
        return int(self._source['meteoRange'])

    @property
    def mid(self):
        return self._source['mid']

    @property
    def name(self):
        return self._source['name']

    @property
    def objs(self):
        return self._source['objs']

    @property
    def owner_org(self):
        return self._source['ownerOrg']

    @property
    def src_group(self):
        return self._source['src']['group']

    @property
    def src_index(self):
        if 'index' in self._source['src']:
            return int(self._source['src']['index'])
        return None

    @property
    def src_tid(self):
        return self._source['srctid']

    @property
    def last_insert(self):
        return datetime.fromtimestamp(int(self._source['last_insert']))

    @property
    def link(self):
        return self._source['link']

    @property
    def bindings(self):
        _bindings = list(self._source['metadata']['binding'])
        return _bindings

    @property
    def location(self):
        if self._source['shape'] is not None:
            return shape(self._source['shape'])

    @property
    def crs(self):
        if self.location:
            return self.location['crs']['properties']['name']

    @property
    def sid(self):
        return self._source['sid']

    @property
    def country(self):
        return self._source['country']

    @property
    def region(self):
        return self._source['region']
