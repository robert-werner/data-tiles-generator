import rasterio
from affine import Affine
from pyproj import transform

with rasterio.open('/Users/leonid/Downloads/MAY_2021_part13.tif') as src:
    print(src.bounds)