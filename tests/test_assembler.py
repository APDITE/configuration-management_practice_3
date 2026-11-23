"""Интерфейс командной строки ассемблера."""

import os
import unittest

import assembler
from helpers import TempDirTestCase, run_main
from spec_cases import SPEC_CASES

SOURCE = "".join(f"- {m}: {i.b}\n" for m, i, _ in SPEC_CASES)
SPEC_BYTES = b"".join(code for _, _, code in SPEC_CASES)
SPEC_PROGRAM = os.path.join(
    os.path.dirname(__file__), "..", "programs", "spec.yaml")
USAGE_ERROR = 2


class AssemblerCliTest(TempDirTestCase):
    """Проверка параметров, двоичного файла и режима тестирования."""

    def test_test_mode_prints_bytes(self):
        """Режим тестирования печатает байты команд и размер файла."""
        source = self.write("spec.yaml", SOURCE)
        argv = ["-i", source, "-o", self.path("out.bin"), "--test"]
        code, out, _ = run_main(assembler.main, argv)
        self.assertEqual(code, 0)
        self.assertEqual(out.splitlines(), [
            "0x51, 0x19, 0x00",
            "0x31, 0x3C, 0x00",
            "0xFF, 0xAF, 0x00, 0x00, 0x00",
            "0xA8, 0x5C, 0x00, 0x00, 0x00",
            "Binary size: 16 bytes"])

    def test_normal_mode_prints_size_only(self):
        """Без режима тестирования выводится только размер файла."""
        source = self.write("spec.yaml", SOURCE)
        argv = ["-i", source, "-o", self.path("out.bin")]
        code, out, _ = run_main(assembler.main, argv)
        self.assertEqual(code, 0)
        self.assertEqual(out, "Binary size: 16 bytes\n")

    def test_binary_file_content(self):
        """Двоичный файл содержит машинный код программы."""
        source = self.write("spec.yaml", SOURCE)
        output = self.path("out.bin")
        run_main(assembler.main, ["-i", source, "-o", output])
        with open(output, "rb") as stream:
            self.assertEqual(stream.read(), SPEC_BYTES)

    def test_spec_program_file(self):
        """programs/spec.yaml даёт все байты из спецификации."""
        output = self.path("spec.bin")
        argv = ["-i", SPEC_PROGRAM, "-o", output]
        code, _, _ = run_main(assembler.main, argv)
        self.assertEqual(code, 0)
        with open(output, "rb") as stream:
            self.assertEqual(stream.read(), SPEC_BYTES)

    def test_empty_program_size(self):
        """Пустая программа - пустой файл размером 0 байт."""
        source = self.write("empty.yaml", "[]\n")
        argv = ["-i", source, "-o", self.path("out.bin")]
        _, out, _ = run_main(assembler.main, argv)
        self.assertEqual(out, "Binary size: 0 bytes\n")

    def test_bad_source_reports_error(self):
        """Ошибка в программе: сообщение в stderr и код 1."""
        source = self.write("bad.yaml", "- jump: 1\n")
        argv = ["-i", source, "-o", self.path("out.bin")]
        code, _, err = run_main(assembler.main, argv)
        self.assertEqual(code, 1)
        self.assertIn("assembler: error:", err)
        self.assertIn("unknown command", err)
        self.assertFalse(os.path.exists(self.path("out.bin")))

    def test_unwritable_output(self):
        """Выходной файл нельзя создать."""
        source = self.write("spec.yaml", SOURCE)
        argv = ["-i", source, "-o", self.path("no_dir/out.bin")]
        code, _, err = run_main(assembler.main, argv)
        self.assertEqual(code, 1)
        self.assertIn("cannot write output", err)

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
