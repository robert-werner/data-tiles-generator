import os

from pyproj import CRS

from data_tiles_generator.config import HOST, DATASERVER_API, SOURCES_LIST

CUSTOM_TMS = {
    'EPSG:3575': {
        'crs': CRS.from_epsg(3575),
        'extent': [-180.0,
                   45.0,
                   180.0,
                   90.0],
        'extent_crs': CRS.from_epsg(4326)}
}
SOURCES_URL = os.path.join(HOST, DATASERVER_API, SOURCES_LIST)
