import json
from os import path, getcwd

file = open(path.join(getcwd(), 'uomcodes.json'))

codes = json.load(file)

file.close()


def get_uom_code(code):
    if not codes.get(code):
        return 'C62'

    return codes[code]
