"""Разбор исходного текста: допустимые и ошибочные программы."""

import unittest

from errors import UvmError
from isa import Instruction
from source import load_program, parse_program


class ParseProgramTest(unittest.TestCase):
    """Проверка разбора YAML и сообщений об ошибках."""

    def assert_error(self, text, fragment):
        """Разбор текста должен завершаться ошибкой с фрагментом."""
        with self.assertRaises(UvmError) as context:
            parse_program(text, "prog")
        self.assertIn(fragment, str(context.exception))

    def test_empty_list(self):
        """Пустой список - пустая программа."""
        self.assertEqual(parse_program("[]", "prog"), [])

    def test_hex_operand(self):
        """YAML позволяет задавать операнд в шестнадцатеричном виде."""
        result = parse_program("- load_const: 0x10", "prog")
        self.assertEqual(result, [Instruction(81, 16)])

    def test_operand_bounds(self):
        """Граничные значения операндов допустимы."""
        text = "- load_const: 65535\n- read: 2047\n- eq: 1073741823"
        self.assertEqual(len(parse_program(text, "prog")), 3)

    def test_not_a_list(self):
        """Корень документа должен быть списком."""
        self.assert_error("load_const: 1", "expected a list")
        self.assert_error("", "expected a list")

    def test_bad_item(self):
        """Команда - словарь из одного ключа."""
        self.assert_error("- load_const", "command #1")
        self.assert_error("- {read: 1, eq: 2}", "expected 'mnemonic")

    def test_unknown_command(self):
        """Неизвестная мнемоника."""
        self.assert_error("- load_const: 1\n- jump: 2",
                          "command #2: unknown command 'jump'")

    def test_bad_operand_type(self):
        """Операнд должен быть целым числом."""
        self.assert_error("- read: abc", "must be an integer")
        self.assert_error("- read: 1.5", "must be an integer")
        self.assert_error("- read: true", "must be an integer")

    def test_operand_out_of_range(self):
        """Операнд должен помещаться в поле B."""
        self.assert_error("- load_const: 65536", "range 0..65535")
        self.assert_error("- read: 2048", "range 0..2047")
        self.assert_error("- write: -1", "got -1")
        self.assert_error("- eq: 1073741824", "range 0..1073741823")

    def test_invalid_yaml(self):
        """Синтаксическая ошибка YAML."""
        self.assert_error("- load_const: [", "invalid YAML")

    def test_missing_file(self):
        """Файл программы не найден."""
        with self.assertRaises(UvmError) as context:
            load_program("no_such_file.yaml")
        self.assertIn("cannot read source", str(context.exception))


if __name__ == "__main__":
    unittest.main()
