"""Ассемблер УВМ: программа на языке YAML -> машинный код.

Использование:
    python3 src/assembler.py -i program.yaml -o program.bin [-t]
"""

import argparse
import sys

from binfile import write_binary
from codec import encode, encode_program, format_bytes
from errors import UvmError
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
                        help="test mode: print the bytes of every command")
    return parser


def run(args):
    """Выполнить ассемблирование по разобранным параметрам."""
    instructions = load_program(args.input)
    code = encode_program(instructions)
    write_binary(args.output, code)
    if args.test:
        for instruction in instructions:
            print(format_bytes(encode(instruction)))
    print(f"Binary size: {len(code)} bytes")
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
