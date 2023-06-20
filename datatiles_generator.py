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
from data_tiles_generator.utils import reproject_source, load_tms, axes_directions, tilepoint2pix


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
    for source in sources_list:
        for zoom in zoom_list:
            output_json = {
                'data': []
            }
            tile = tms.tile(source.location.x, source.location.y, zoom)
            output_folder = os.path.join(output_dir, f'{zoom}/{tile.x}')
            os.makedirs(output_folder, exist_ok=True)
            output_file = os.path.join(output_folder, f'{tile.y}.json')
            output_json['data'].extend([source.src_index, *tilepoint2pix(reproject_source(source, dest_crs),
                                                                         tms.xy_bounds(tile),
                                                                         tilesize)])
            if not os.path.isfile(output_file):
                with open(output_file, 'w') as output_json_file:
                    json.dump(
                        {
                            'items': len(output_json['data']) // 3,
                            'data': output_json['data']
                        }, output_json_file
                    )
            else:
                with open(output_file, 'r') as output_json_file:
                    output_json_dict = json.load(output_json_file)
                output_json_dict['data'].extend(output_json['data'])
                output_json_dict['items'] = len(output_json_dict['data']) // 3
                with open(output_file, 'w') as output_json_file:
                    json.dump(
                        output_json_dict, output_json_file
                    )





if __name__ == '__main__':
    try:
        cli()
    except Exception as e:
        raise e
