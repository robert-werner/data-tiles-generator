import morecantile
from pyproj import CRS, Transformer, transform

from data_tiles_generator.constants import CUSTOM_TMS


def reproject_shape(shape, src_crs, dest_crs):
    dest_crs_def = None  # PureC-style костыль, на стороне PyPROJ
    src_crs_def = None
    dest_crs_def = CRS.from_user_input(dest_crs)
    src_crs_def = CRS.from_user_input(src_crs)
    if not src_crs_def:
        raise Exception(f'Определение исходной СК {dest_crs} отсутствует!')
    if not dest_crs_def:
        raise Exception(f'Определение конечной СК {dest_crs} отсутствует!')
    project = Transformer.from_crs(src_crs_def, dest_crs_def, always_xy=True).transform
    return transform(project, shape)


def reproject_source(source, dest_crs):
    src_crs = source.crs
    return reproject_shape(source.location, src_crs, dest_crs)


def load_tms(dest_crs, tilesize):
    if dest_crs in CUSTOM_TMS:
        tms_params = CUSTOM_TMS[dest_crs]
        tms_params['tile_width'] = tilesize
        tms_params['tile_height'] = tilesize
        tms = morecantile.TileMatrixSet.custom(**tms_params)
    else:
        tms_params = {'extent': list(CRS.from_user_input(dest_crs).area_of_use.bounds),
                      'crs': CRS.from_user_input(dest_crs), 'extent_crs': CRS.from_epsg(4326),
                      'tile_width': tilesize,
                      'tile_height': tilesize}
        tms = morecantile.TileMatrixSet.custom(**tms_params)
    return tms


def affine_from_tile(tile, tms):
    ...

