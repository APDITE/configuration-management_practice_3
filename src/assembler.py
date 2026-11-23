"""Ассемблер УВМ: программа на языке YAML -> промежуточное представление.

Использование:
    python3 src/assembler.py -i program.yaml -o program.bin [-t]
"""

import argparse
import sys

from errors import UvmError
from isa import format_fields
from source import load_program

PROG = "assembler"


def build_parser():
    """Создать разборщик параметров командной строки."""
    parser = argparse.ArgumentParser(
        prog=PROG, allow_abbrev=False,
        description="Assembler for the educational virtual machine (UVM).")
    parser.add_argument("-i", "--input", required=True, metavar="PATH",
                        help="path to the source file (YAML)")
    parser.add_argument("-o", "--output", required=True, metavar="PATH",
                        help="path to the binary output file")
    parser.add_argument("-t", "--test", action="store_true",
                        help="test mode: print the assembled program")
    return parser


def run(args):
    """Выполнить ассемблирование по разобранным параметрам."""
    instructions = load_program(args.input)
    if args.test:
        for instruction in instructions:
            print(format_fields(instruction))
    return 0


def main(argv=None):
    """Точка входа: вернуть код завершения."""
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except UvmError as error:
        print(f"{PROG}: error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
