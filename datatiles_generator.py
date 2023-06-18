import json
import os.path
from math import floor

import rasterio.transform
import requests
from click import command
from requests.adapters import HTTPAdapter, Retry

import options
from data_tiles_generator.classes.sources import Sources
from data_tiles_generator.config import HEADERS
from data_tiles_generator.constants import SOURCES_URL
from data_tiles_generator.utils import reproject_source, load_tms, axes_directions


@command(short_help='Генератор дата-тайлов из списков источников')
@options.urn_opt
@options.output_crs_opt
@options.zoom_opt
@options.output_dir_arg
@options.tilesize_opt
def cli(urn, dest_crs, zoom_list, output_dir, tilesize):
    session = requests.Session()
    retries = Retry(total=1,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    with session.post(SOURCES_URL, headers=HEADERS, data=json.dumps({
        "urn": [urn]
    })) as sources_request:
        sources_list = Sources(sources_request.json())
    tms = load_tms(dest_crs, tilesize)
    output_datatile = {'items': 0, 'data': []}
    for source in sources_list:
        for zoom in zoom_list:
            output_datatile['data'].append(
                source.src_index
            )
            output_datatile['items'] += 1
            if source.has_geo:
                reprojected_location_x, reprojected_location_y = reproject_source(source, dest_crs)
                tile = tms.tile(reprojected_location_x, reprojected_location_y, zoom)
                tile_bbox = tms.xy_bounds(tile)
                if dest_crs.is_projected:
                    minx, maxx, miny, maxy = tile_bbox.bottom, tile_bbox.right, tile_bbox.top, tile_bbox.left
                    x_resolution = (maxx - minx) / tilesize
                    y_resolution = (maxy - miny) / tilesize
                    x_pixels = int((reprojected_location_x - minx) / x_resolution)
                    y_pixels = int((maxy - reprojected_location_y) / y_resolution)
                elif dest_crs.is_geographic:
                    minlon, maxlon, minlat, maxlat = tile_bbox.left, tile_bbox.right, tile_bbox.bottom, tile_bbox.top
                    lon_resolution = (maxlon - minlon) / tilesize
                    lat_resolution = (maxlat - minlat) / tilesize
                    x_pixels = int((reprojected_location_x - minlon) / lon_resolution)
                    y_pixels = int((maxlat - reprojected_location_y) / lat_resolution)
                output_datatile['data'].extend(
                    [x_pixels, y_pixels]
                )
            else:
                output_datatile['data'].extend(
                    [None, None]
                )
            output_folder = os.path.join(output_dir, f'{zoom}/{tile.x}')
            output_file = os.path.join(output_folder, f'{tile.y}.json')
            os.makedirs(output_folder, exist_ok=True)
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as output_file_fp:
                    output_file_json = json.load(output_file_fp)
                output_datatile['items'] += output_file_json['items']
                output_datatile['data'].extend(output_file_json['data'])
            with open(output_file, 'w', encoding='utf-8') as zoom_dt:
                json.dump(output_datatile, zoom_dt)
            output_datatile = {'items': 0, 'data': []}



if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        raise e
