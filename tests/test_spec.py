"""Ассемблер генерирует поля и значения из тестов спецификации."""

import unittest

from isa import format_fields
from source import parse_program
from spec_cases import SPEC_CASES


class SpecFieldsTest(unittest.TestCase):
    """Проверка промежуточного представления для тестов спецификации."""

    def test_each_command(self):
        """Каждая команда даёт ожидаемые поля A и B."""
        for mnemonic, expected, _ in SPEC_CASES:
            with self.subTest(command=mnemonic):
                text = f"- {mnemonic}: {expected.b}\n"
                self.assertEqual(parse_program(text, "t"), [expected])

    def test_whole_program(self):
        """Программа из всех команд сохраняет порядок команд."""
        text = "\n".join(f"- {m}: {i.b}" for m, i, _ in SPEC_CASES)
        expected = [instruction for _, instruction, _ in SPEC_CASES]
        self.assertEqual(parse_program(text, "t"), expected)

    def test_format_fields(self):
        """Поля печатаются в формате спецификации."""
        _, instruction, _ = SPEC_CASES[0]
        self.assertEqual(format_fields(instruction), "A=81, B=50")


if __name__ == "__main__":
    unittest.main()
