"""decoder.py module."""

from os.path import sep as os_path_sep
from typing import Tuple


class CDSRDecoderException(Exception):
    """CDSRDecoderException."""


def decode_scene_dir(scene_dir: str) -> Tuple[str, str, str, str, str]:
    """Decodes a scene directory, returning its data."""

    scene_dir_first, scene_dir_second = scene_dir.split('.')

    if scene_dir_first.startswith('AMAZONIA_1') or scene_dir_first.startswith('CBERS_4'):
        # examples:
        # - AMAZONIA_1_WFI_DRD_2021_04_01.13_22_45_CP5_COROT
        # - AMAZONIA_1_WFI_DRD_2021_03_03.12_57_40_CB11
        # - AMAZONIA_1_WFI_DRD_2021_03_03.14_35_23_CB11_SIR18
        # - CBERS_4_MUX_DRD_2020_07_31.13_07_00_CB11
        # - CBERS_4A_MUX_RAW_2019_12_27.13_53_00_ETC2
        # - CBERS_4A_MUX_RAW_2020_04_06.00_56_20_CP5
        # - CBERS_4A_MUX_RAW_2019_12_28.14_15_00

        # get the data from the first part of scene dir
        satellite, number, sensor, _, *reception_date = scene_dir_first.split('_')
        # create satellite name with its number
        satellite = satellite + number
        reception_date = '-'.join(reception_date)

        # second part of scene dir, it can be: `13_53_00`,
        # `13_53_00_ETC2`, `14_35_23_CB11_SIR18`, etc.
        second_part = scene_dir_second.split('_')

        # I need at least three elements to create the time datum
        if len(second_part) < 3:
            raise CDSRDecoderException(f'Invalid second part of scene dir: `{scene_dir_second}`.')

        # join the time parts from the list of parts
        reception_time = ':'.join(second_part[0:3])

        # get the antenna and server part from the list of parts
        antenna_and_server = second_part[3:]

        # if there is not at least one element (i.e. antenna), then raise an exception
        if not antenna_and_server:
            raise CDSRDecoderException(f'`{scene_dir}` scene_dir does not contain antenna datum.')

        # get antenna datum from the list of parts
        antenna = antenna_and_server[0]

    elif scene_dir_first.startswith('CBERS2B') or scene_dir_first.startswith('LANDSAT'):
        # examples:
        # - CBERS2B_CCD_20070925.145654
        # - LANDSAT1_MSS_19750907.130000

        satellite, sensor, reception_date = scene_dir_first.split('_')
        reception_time = scene_dir_second

        if len(reception_date) != 8:
            # example: a date should be something like this: '20070925'
            raise CDSRDecoderException(f'Size of `{reception_date}` reception date is not 8.')

        # I build the date string based on the old one (e.g. from '20070925' to '2007-09-25')
        reception_date = f'{reception_date[0:4]}-{reception_date[4:6]}-{reception_date[6:8]}'

        if len(reception_time) != 6:
            # example: a time should be something like this: '145654'
            raise CDSRDecoderException(f'Size of `{reception_time}` reception time is not 6.')

        # I build the time string based on the old one (e.g. from '145654' to '14:56:54')
        reception_time = f'{reception_time[0:2]}:{reception_time[2:4]}:{reception_time[4:6]}'

        # default value to antenna, because these satellites do
        # not have antenna datum on their scene directory
        # `ND` stands for `não determinado`
        antenna = 'ND'

    else:
        raise CDSRDecoderException(f'Invalid scene directory: `{scene_dir}`.')

    return satellite, sensor, reception_date, reception_time, antenna


def decode_path_row_dir(path_row_dir: str) -> Tuple[str, str]:
    """Decodes a path/row directory, returning its information."""

    splitted_path_row = path_row_dir.split('_')

    if len(splitted_path_row) == 3:
        # example: `151_098_0`
        path, row, _ = splitted_path_row
    elif len(splitted_path_row) == 5:
        # example: `151_B_141_5_0`
        path, _, row, *_ = splitted_path_row
    else:
        raise CDSRDecoderException(f'Path/row directory cannot be decoded: `{path_row_dir}`.')

    return path, row


def decode_geo_processing_dir(geo_processing_dir: str) -> str:
    """Decodes a geo. processing directory, returning its information."""

    geo_processing = geo_processing_dir.split('_')[0]

    if geo_processing in ('2', '2B', '3', '4'):
        return geo_processing

    raise CDSRDecoderException('Geo. processing directory cannot '
                              f'be decoded: `{geo_processing_dir}`.')


def decode_asset(asset: str) -> Tuple[str, str]:
    """Decodes a asset file, returning if this file is DN or SR.
    Asset example: `AMAZONIA_1_WFI_20210321_037_016_L2_BAND4.tif`"""

    # asset example: AMAZONIA_1_WFI_20210321_037_016_L2_BAND4.tif

    if "." not in asset:
        raise CDSRDecoderException('An asset must have an extension.')

    # get date from asset
    date = asset.split('_')[3]

    if len(date) != 8:
        raise CDSRDecoderException(f'Invalid date inside asset: `{date}`.')

    # fix date format
    date = f'{date[:4]}-{date[4:6]}-{date[6:8]}'

    if 'GRID_SURFACE' in asset or 'EVI' in asset or 'NDVI' in asset:
        return date, 'SR'

    return date, 'DN'


def decode_path(path: str) -> dict:
    """Decodes a path, returning its metadata."""

    # check type
    if not isinstance(path, str):
        raise CDSRDecoderException(f'Path must be a str, not a `{type(path)}`.')

    # if path ends with slash, then remove it
    if path.endswith('/'):
        path = path[:-1]

    # get dir path index starting at `/TIFF`
    index = path.find('TIFF')

    # `splitted_dir_path` examples:
    # - ['TIFF', 'CBERS4A', '2020_11', 'CBERS_4A_WFI_RAW_2020_11_10.13_41_00_ETC2',
    #       '207_148_0', '2_BC_UTM_WGS84']
    # - ['TIFF', 'CBERS4A', '2020_11', 'CBERS_4A_WFI_RAW_2020_11_10.13_41_00_ETC2',
    #       '207_148_0', '2_BC_UTM_WGS84', 'AMAZONIA_1_WFI_20210321_037_016_L2_BAND4.tif']
    splitted_path = path[index:].split(os_path_sep)

    # get directory level
    level = len(splitted_path)

    # if this path is not level 6 or 7, then raise an exception
    if level not in (6, 7):
        raise CDSRDecoderException(f'Invalid `{level}` level to path: `{path}`.')

    # add the metadata based on the directory decode
    metadata = {
        # default values
        'date': None,
        'radio_processing': None
    }

    # if path is 7 level, then the last position is the file and I can get radio. processing
    if level == 7:
        metadata['date'], metadata['radio_processing'] = decode_asset(splitted_path[-1])

    # extract metadata
    _, metadata['satellite'], _, scene_dir, path_row_dir, geo_processing_dir, *_ = splitted_path
    _, metadata['sensor'], *_, metadata['antenna'] = decode_scene_dir(scene_dir)
    metadata['path'], metadata['row'] = decode_path_row_dir(path_row_dir)
    metadata['geo_processing'] = decode_geo_processing_dir(geo_processing_dir)

    return metadata
