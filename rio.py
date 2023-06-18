from pprint import pprint
from pyproj import Proj, transform
import rasterio as rio


def image_latlon_pxpy(latitude, longitude):
    dataset = rio.open('/Users/leonid/Downloads/MAY_2021_part13_3857.tif', crs='epsg:3857')
    coords = transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), longitude, latitude)
    px, py = coords[0], coords[1]
    px_pc = (px - dataset.bounds.left) / (dataset.bounds.right - dataset.bounds.left)
    py_pc = (dataset.bounds.top - py) / (dataset.bounds.top - dataset.bounds.bottom)
    print(px, py, dataset.bounds)
    return int(px_pc * dataset.width), int(py_pc * dataset.height)


pprint(image_latlon_pxpy(56.8415, 56.9017))
