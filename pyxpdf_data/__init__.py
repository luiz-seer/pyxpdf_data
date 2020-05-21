import os
import time
import site
from pathlib import Path

__version__ = 1.0


ROOT = Path(__file__).parent
POPPLER_DATA_DIR = Path(ROOT, 'poppler_data')

def _get_root_files(path):
    return [x for x in Path(path).iterdir() if x.is_file()]

def _get_root_dirs(path):
    return [x for x in Path(path).iterdir() if x.is_dir()]

def _process_poppler_data(entry):
    lines = [
        "# {0}".format(entry),
    ]

    if entry == 'nameToUnicode':
        for file in _get_root_files(Path(POPPLER_DATA_DIR, entry)):
            lines.append('nameToUnicode "{0}"'.format(file.absolute()))
    elif entry == 'cidToUnicode':
        for file in  _get_root_files(Path(POPPLER_DATA_DIR, entry)):
            lines.append('cidToUnicode {0} "{1}"'.format(file.name, file.absolute()))
    elif entry == 'unicodeMap':
        for file in  _get_root_files(Path(POPPLER_DATA_DIR, entry)):
            lines.append('unicodeMap {0} "{1}"'.format(file.name, file.absolute()))
    elif entry == 'cMap':
        for directory in _get_root_dirs(Path(POPPLER_DATA_DIR, entry)):
                lines.append('cMapDir {0} "{1}"'.format(directory.name, directory.absolute()))

    lines.append(os.linesep)
    return lines


def _xpdfrc_header():
    return [
        '# {0}'.format(time.ctime()),
        '# Generated by pyxpdf_poppler_data python module',
        '# THIS FILE WILL NOT WORK ON OTHER SYSTEM, ',
        '# AS IT USES ABSOLUTE PATHs',
        '',
    ]

def pyxpdf_defaults():
    return [
        '# Default Settings for pyxpdf',
        'textEncoding UTF-8'
    ]

def generate_xpdfrc():
    xpdfrc = _xpdfrc_header()

    for entry in ['nameToUnicode', 'cidToUnicode', 'unicodeMap', 'cMap']:
        xpdfrc += _process_poppler_data(entry)

    # add defaults
    xpdfrc += pyxpdf_defaults()

    # add trailing newline
    xpdfrc.append('')

    return os.linesep.join(xpdfrc)


def get_poppler_dir():
    return str(POPPLER_DATA_DIR)

def get_xpdfrc():
    # TODO: add cache support
    xpdfrc_path = Path(site.getsitepackages()[0], 'default.xpdfrc')
    xpdfrc = generate_xpdfrc()
    with open(xpdfrc_path, 'w') as fp:
        fp.write(xpdfrc)
    return str(xpdfrc_path.absolute())


if __name__ == "__main__":
    print(get_xpdfrc())