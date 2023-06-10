import json
import os.path

import requests
from click import command
from requests.adapters import HTTPAdapter, Retry

import options
from data_tiles_generator.classes.sources import Sources
from data_tiles_generator.config import HEADERS
from data_tiles_generator.constants import SOURCES_URL
from data_tiles_generator.utils import reproject_source, load_tms


@command(short_help='Генератор дата-тайлов из списков источников')
@options.urn_opt
@options.output_crs_opt
@options.zoom_opt
@options.output_dir_arg
@options.resolution_opt
@options.tilesize_opt
def cli(urn, dest_crs, zoom_list, output_dir, resolution, tilesize):
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
    for zoom in zoom_list:
        output_datatile = {'items': 0, 'data': []}
        for source in sources_list:
            output_datatile['data'].append(
                source.src_index
            )
            output_datatile['items'] += 1
            if source.has_geo:
                reprojected_location = reproject_source(source, dest_crs)
                tile = tms.tile(reprojected_location[0], reprojected_location[1], zoom)
                tile_bbox = tms.xy_bounds(tile)
                pix_x = (reprojected_location[0] - tile_bbox.left) / (tile_bbox.right - tile_bbox.left)
                pix_y = (tile_bbox.top - reprojected_location[1]) / (tile_bbox.top - tile_bbox.bottom)
                output_datatile['data'].extend(
                    [int(pix_x * tilesize),
                     int(pix_y * tilesize)]
                )
            else:
                output_datatile['data'].extend(
                    [None, None]
                )
        with open(os.path.join(output_dir, f'{zoom}.json'), 'w', encoding='utf-8') as zoom_dt:
            json.dump(output_datatile, zoom_dt)


if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        raise e
