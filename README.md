# Data Tiles generator

Утилита генерирует JSON-тайлы из координат исходных точек как то так

![image](http://dev.modext.ru:8929/dcc5/data-tiles-generator/-/blob/main/DOC/photo_2023-07-18_17-56-19.jpg)

Утилита получает по REST API информацию по точкам с координатами lat/lon и расчитывает позицию каждой точки в тайле проекции (в примере показан Меркатор) и вычисляет X/Y координаты точек (координаты пикселей) в координатной плоскости тайла
