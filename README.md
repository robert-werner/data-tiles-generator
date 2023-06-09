Как запускать:

python datatile_generator.py URN --out-crs EPSG:3857 --zooms 3,4,5 --tilesize 256 --resolution 1  

На выходе папка с дататайлами *.json.

Описание параметров:
– out-crs: выходная СК
– zooms: уровни увеличения
– tilesize: размер тайла 
– resolution: размер ячейки (чем меньше, тем точнее расположение пиксела)