from click import argument, Path, option

from options_handlers import crs_handler, zoom_handler

urn_opt = argument(
    'urn',
    type=str,
    nargs=1,
    required=True,
    metavar='Uniform Resource Name'
)

output_dir_arg = argument(
    'output_dir',
    metavar='OUTPUT',
    required=True,
    type=Path(resolve_path=True, file_okay=False))

output_crs_opt = option('--out-crs',
                        'dest_crs',
                        default='EPSG:4326',
                        callback=crs_handler,
                        help="Выходная система координат тайлов.")

zoom_opt = option(
    '--zooms',
    'zoom_list',
    type=str,
    default='3',
    callback=zoom_handler,
    help='Значение (значения) увеличения (zoom) для генерации тайлов.'
)

tilesize_opt = option(
    '--tilesize',
    "tilesize",
    nargs=1,
    type=int,
    default=256,
    help='Разрешение тайла (на выходе квадрат стороной указанного размера).')
