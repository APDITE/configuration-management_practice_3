"""Интерфейс командной строки ассемблера."""

import unittest

import assembler
from helpers import TempDirTestCase, run_main
from spec_cases import SPEC_CASES

SOURCE = "".join(f"- {m}: {i.b}\n" for m, i, _ in SPEC_CASES)
USAGE_ERROR = 2


class AssemblerCliTest(TempDirTestCase):
    """Проверка параметров и режима тестирования."""

    def test_test_mode_prints_fields(self):
        """Режим тестирования печатает поля и значения команд."""
        source = self.write("spec.yaml", SOURCE)
        argv = ["-i", source, "-o", self.path("out.bin"), "--test"]
        code, out, _ = run_main(assembler.main, argv)
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), [
            "A=81, B=50", "A=49, B=120", "A=127, B=351", "A=40, B=185"])

    def test_bad_source_reports_error(self):
        """Ошибка в программе: сообщение в stderr и код 1."""
        source = self.write("bad.yaml", "- jump: 1\n")
        argv = ["-i", source, "-o", self.path("out.bin")]
        code, _, err = run_main(assembler.main, argv)
        self.assertEqual(code, 1)
        self.assertIn("assembler: error:", err)
        self.assertIn("unknown command", err)

    def test_missing_arguments(self):
        """Без обязательных параметров - ошибка использования."""
        code, _, err = run_main(assembler.main, ["--test"])
        self.assertEqual(code, USAGE_ERROR)
        self.assertIn("-i/--input", err)

    def test_abbreviations_rejected(self):
        """Сокращённые имена параметров не принимаются."""
        code, _, _ = run_main(assembler.main, ["--inp", "a", "-o", "b"])
        self.assertEqual(code, USAGE_ERROR)


if __name__ == "__main__":
    unittest.main()
