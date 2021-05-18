import json
from os import path, getcwd


directory = path.dirname(path.realpath(__file__))
file = open(path.join(directory, 'uomcodes.json'))

codes = json.load(file)

file.close()


def get_uom_code(code):
    if not codes.get(code):
        return 'C62'

    return codes[code]
