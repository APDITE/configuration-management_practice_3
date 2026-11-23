"""Тесты из спецификации УВМ (вариант 17): поля и байты."""

from isa import Instruction

SPEC_CASES = (
    ("load_const", Instruction(81, 50), bytes([0x51, 0x19, 0x00])),
    ("read", Instruction(49, 120), bytes([0x31, 0x3C, 0x00])),
    ("write", Instruction(127, 351),
     bytes([0xFF, 0xAF, 0x00, 0x00, 0x00])),
    ("eq", Instruction(40, 185), bytes([0xA8, 0x5C, 0x00, 0x00, 0x00])),
)
