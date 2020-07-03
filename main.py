import json

import converter


def main():
    file = json.load(open('input.json'))
    converter.convert(file['sigma'], file['s0'], file['F'], file['delta'])


if __name__ == '__main__':
    main()
