#!/bin/sh
# Запуск ассемблера и тестов УВМ.

cd "$(dirname "$0")" || exit 1
export PYTHONPATH=src

usage() {
    echo "usage: ./run.sh asm|test [options]" >&2
    exit 2
}

case "$1" in
    asm)
        shift
        exec python3 src/assembler.py "$@"
        ;;
    test)
        exec python3 -m unittest discover -s tests -v
        ;;
    *)
        usage
        ;;
esac
