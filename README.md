Как запускать:

python -m pip install requirements.txt (выполнить только один раз в папке репозитория, Python 3.9)

python datatile_generator.py URN --out-crs EPSG:3857 --zooms 3,4,5 --tilesize 256 OUTPUT_FOLDER  

На выходе папка с дататайлами *.json.

Описание параметров:
– out-crs: выходная СК
– zooms: уровни увеличения
– tilesize: размер тайла 
– OUTPUT_FOLDER: выходная папка