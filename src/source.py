"""Разбор исходного текста программы на языке ассемблера (YAML).

Программа - список команд. Каждая команда - словарь из одного ключа:
мнемоника команды, значение - целочисленный операнд (поле B).
"""

import yaml

from errors import UvmError
from isa import BY_MNEMONIC, Instruction

ITEM_SIZE = 1
OPERAND_MIN = 0


def read_source(path):
    """Прочитать текстовый файл программы."""
    try:
        with open(path, encoding="utf-8") as stream:
            return stream.read()
    except OSError as error:
        reason = error.strerror or str(error)
        raise UvmError(f"{path}: cannot read source: {reason}") from error
    except UnicodeDecodeError as error:
        raise UvmError(f"{path}: source is not UTF-8 text") from error


def parse_program(text, name):
    """Разобрать YAML-текст в список команд (промежуточное представление)."""
    try:
        items = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise UvmError(f"{name}: invalid YAML: {_first_line(error)}") from error
    if not isinstance(items, list):
        raise UvmError(f"{name}: expected a list of commands")
    return [_parse_item(item, name, index)
            for index, item in enumerate(items, start=1)]


def load_program(path):
    """Прочитать файл и разобрать его в список команд."""
    return parse_program(read_source(path), path)


def _first_line(error):
    """Первая строка сообщения об ошибке YAML вместе с позицией."""
    mark = getattr(error, "problem_mark", None)
    problem = getattr(error, "problem", None) or str(error)
    if mark is None:
        return problem.splitlines()[0]
    return f"line {mark.line + 1}: {problem}"


def _parse_item(item, name, index):
    """Разобрать одну команду списка."""
    where = f"{name}: command #{index}"
    if not isinstance(item, dict) or len(item) != ITEM_SIZE:
        raise UvmError(f"{where}: expected 'mnemonic: operand'")
    (mnemonic, operand), = item.items()
    spec = BY_MNEMONIC.get(mnemonic)
    if spec is None:
        raise UvmError(f"{where}: unknown command {mnemonic!r}")
    if isinstance(operand, bool) or not isinstance(operand, int):
        raise UvmError(f"{where}: operand of {mnemonic} must be an integer")
    if not OPERAND_MIN <= operand <= spec.operand_max:
        raise UvmError(
            f"{where}: operand of {mnemonic} must be in range "
            f"{OPERAND_MIN}..{spec.operand_max}, got {operand}")
    return Instruction(spec.opcode, operand)
