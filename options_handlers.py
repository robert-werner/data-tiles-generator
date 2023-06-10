import click
from pyproj import CRS


def crs_handler(ctx, param, value):
    crs_def = None  # PureC-style костыль, на стороне PyPROJ
    crs_def = CRS.from_user_input(
        value)  # TODO: пулл-реквест в pyproj для возвращения None-значения при отсутствии определения СК
    if not crs_def:
        raise click.BadParameter('Поддерживаются системы координат только из EPSG-базы данных (см. https://epsg.org/)')
    else:
        epsg_auth = crs_def.to_epsg()
        if not epsg_auth:
            raise click.BadParameter(
                'Поддерживаются системы координат только из EPSG-базы данных (см. https://epsg.org/)')
    return ":".join(crs_def.to_authority(auth_name='EPSG'))


def zoom_handler(ctx, param, value):
    zooms = []
    if '..' in value:
        start, stop = map(
            lambda x: int(x) if x else None, value.split('..'))
        if start is None:
            start = 1
        zooms.extend(list(map(str,
                              list(range(start, stop + 1)))))
    elif '-' in value:
        start, stop = map(
            lambda x: int(x) if x else None, value.split('-'))
        if start is None:
            start = 1
        zooms.extend(list(map(str,
                              list(range(start, stop + 1)))))
    elif ',' in value:
        zooms.extend(list(map(
            lambda x: x if x else None, value.split(','))))
    else:
        try:
            int(value)
        except ValueError:
            raise click.BadParameter('''
                            Допустимые форматы ввода уровней увеличения:

                            1) 0..4
                            2) 0-4
                            3) 0,1,2,3,4
                            4) 0

                            Остальные форматы недопустимы.
                            ''')
        else:
            _value = int(value)
            if _value < 0 or _value > 24:
                raise click.BadParameter('Поддерживаются только уровни увеличения с 0 по 24 (включительно).')
            zooms.append(str(_value))
    return zooms
