import json
from os import path, getcwd
from .util import app_file


file = open(app_file('uomcodes.json'))
codes = json.load(file)
file.close()


def get_uom_code(code):
    if not codes.get(code):
        return 'C62'

    return codes[code]
