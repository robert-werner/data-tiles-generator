import json

import requests
from click import command
from requests.adapters import HTTPAdapter, Retry

import options
from data_tiles_generator import Sources
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
    retries = Retry(total=100,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    with session.get(SOURCES_URL, headers=HEADERS, data={
        'urn': [urn]
    }) as sources_request:
        sources_list = Sources(sources_request.text)

    tms = load_tms(dest_crs, tilesize)
    output_datatile = {'items': 0, 'data': []}
    for zoom in zoom_list:
        for source in sources_list:
            output_datatile['data'].append(
                source.src_index
            )
            output_datatile['items'] += 1
            if source.has_geo:
                reprojected_location = reproject_source(source, dest_crs)
                tile = tms.tile(reprojected_location.x, reprojected_location.y, zoom)
                tile_bbox = tms.xy_bounds(tile)
                tile_ul_x, tile_ul_y = tms.ul(tile).x, tms.ul(tile).y
                pix_x = (tile_ul_x - tile_bbox.left) / (tile_bbox.right - tile_bbox.left)
                pix_y = (tile_bbox.top - tile_ul_y) / (tile_bbox.top - tile_bbox.bottom)
                output_datatile['data'].extend(
                    [pix_x * tilesize,
                     pix_y * tilesize]
                )
            else:
                output_datatile['data'].extend(
                    [None, None]
                )
    print(output_datatile)



if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        raise e
