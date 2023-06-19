import morecantile
from pyproj import CRS, Transformer


def reproject_shape(shape, src_crs, dest_crs):
    dest_crs_def = None  # PureC-style костыль, на стороне PyPROJ
    src_crs_def = None
    dest_crs_def = CRS.from_user_input(dest_crs)
    src_crs_def = CRS.from_user_input(src_crs)
    if not src_crs_def:
        raise Exception(f'Определение исходной СК {dest_crs} отсутствует!')
    if not dest_crs_def:
        raise Exception(f'Определение конечной СК {dest_crs} отсутствует!')
    return Transformer.from_crs(crs_from=src_crs_def, crs_to=dest_crs_def, always_xy=True).transform(shape.x, shape.y)


def reproject_source(source, dest_crs):
    src_crs = source.crs
    return reproject_shape(source.location, src_crs, dest_crs)


def load_tms(dest_crs, tilesize):
    dest_crs_name = ":".join(dest_crs.to_authority(auth_name='EPSG'))
    KNOWN_TMS = {
        'EPSG:4326': 'WGS1984Quad',
        'EPSG:3857': 'WebMercatorQuad'
    }
    if dest_crs_name in KNOWN_TMS:
        tms = morecantile.tms.get(KNOWN_TMS[dest_crs_name]).copy(update={
            'tileWidth': tilesize,
            'tileHeight': tilesize
        },
            deep=True)
    else:
        tms_params = {
            'crs': dest_crs,
            'extent': dest_crs.area_of_use.bounds,
            'extent_crs': CRS.from_epsg(4326), 'tile_width': tilesize, 'tile_height': tilesize}
        tms = morecantile.TileMatrixSet.custom(**tms_params)
    return tms


def axes_directions(crs):
    axes = []
    for axis in crs.axis_info:
        axes.append(axis.direction)
    axes = list(set(axes))
    if len(axes) == 1:
        return axes[0]
    return axes


def tilepoint2pix(source, crs, bbox, resolution, x, y):
    if source.has_geo:
        tile_bbox = bbox
        if crs.is_projected:
            minx, maxx, miny, maxy = tile_bbox.bottom, tile_bbox.right, tile_bbox.top, tile_bbox.left
            x_resolution = (maxx - minx) / resolution
            y_resolution = (maxy - miny) / resolution
            x_pixels = int((x - minx) / x_resolution)
            y_pixels = int((maxy - y) / y_resolution)
        elif crs.is_geographic:
            minlon, maxlon, minlat, maxlat = tile_bbox.left, tile_bbox.right, tile_bbox.bottom, tile_bbox.top
            lon_resolution = (maxlon - minlon) / resolution
            lat_resolution = (maxlat - minlat) / resolution
            x_pixels = int((x - minlon) / lon_resolution)
            y_pixels = int((maxlat - y) / lat_resolution)
        return x_pixels, y_pixels
    return None, None
