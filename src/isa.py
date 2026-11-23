"""Спецификация команд УВМ (вариант 17).

Каждая команда состоит из поля A (код операции, биты 0-6) и поля B
(операнд, начинается с бита 7). Команда записывается в память
младшими байтами вперёд (little-endian).
"""

from dataclasses import dataclass

OPCODE_BITS = 7
OPCODE_MASK = (1 << OPCODE_BITS) - 1
BYTE_BITS = 8
BYTE_MASK = (1 << BYTE_BITS) - 1


@dataclass(frozen=True)
class CommandSpec:
    """Описание формата одной команды УВМ."""

    mnemonic: str
    opcode: int
    operand_bits: int
    size: int

    @property
    def operand_max(self):
        """Наибольшее значение, помещающееся в поле B."""
        return (1 << self.operand_bits) - 1


@dataclass(frozen=True)
class Instruction:
    """Команда в промежуточном представлении: поля A и B."""

    a: int
    b: int


LOAD_CONST = CommandSpec("load_const", 81, 16, 3)
READ = CommandSpec("read", 49, 11, 3)
WRITE = CommandSpec("write", 127, 30, 5)
EQ = CommandSpec("eq", 40, 30, 5)

SPECS = (LOAD_CONST, READ, WRITE, EQ)
BY_MNEMONIC = {spec.mnemonic: spec for spec in SPECS}
BY_OPCODE = {spec.opcode: spec for spec in SPECS}

