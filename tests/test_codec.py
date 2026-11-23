"""Кодирование команд в машинный код."""

import unittest

from codec import encode, encode_program, format_bytes
from errors import UvmError
from isa import Instruction
from spec_cases import SPEC_CASES

UNKNOWN_OPCODE = 0
OPERAND_TOO_BIG = 1 << 16


class EncodeTest(unittest.TestCase):
    """Проверка байтовых последовательностей из спецификации."""

    def test_spec_bytes(self):
        """Каждая команда даёт байты из тестов спецификации."""
        for mnemonic, instruction, expected in SPEC_CASES:
            with self.subTest(command=mnemonic):
                self.assertEqual(encode(instruction), expected)

    def test_sizes(self):
        """Размеры команд: 3, 3, 5 и 5 байт."""
        sizes = [len(encode(item)) for _, item, _ in SPEC_CASES]
        self.assertEqual(sizes, [3, 3, 5, 5])

    def test_program_is_concatenation(self):
        """Программа - конкатенация байтов команд."""
        instructions = [item for _, item, _ in SPEC_CASES]
        expected = b"".join(code for _, _, code in SPEC_CASES)
        self.assertEqual(encode_program(instructions), expected)

    def test_empty_program(self):
        """Пустая программа - пустой машинный код."""
        self.assertEqual(encode_program([]), b"")

    def test_unknown_opcode(self):
        """Неизвестный код операции."""
        with self.assertRaises(UvmError):
            encode(Instruction(UNKNOWN_OPCODE, 1))

    def test_operand_does_not_fit(self):
        """Операнд не помещается в поле B."""
        with self.assertRaises(UvmError) as context:
            encode(Instruction(81, OPERAND_TOO_BIG))
        self.assertIn("16 bits", str(context.exception))

    def test_format_bytes(self):
        """Байты печатаются как в спецификации."""
        self.assertEqual(format_bytes(bytes([0x51, 0x19, 0x00])),
                         "0x51, 0x19, 0x00")


if __name__ == "__main__":
    unittest.main()
