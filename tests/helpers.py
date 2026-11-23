"""Общие вспомогательные средства тестов."""

import contextlib
import io
import os
import tempfile
import unittest


class TempDirTestCase(unittest.TestCase):
    """Тест с временным каталогом для файлов."""

    def setUp(self):
        """Создать временный каталог."""
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = self._tmp.name

    def path(self, name):
        """Путь к файлу во временном каталоге."""
        return os.path.join(self.tmp, name)

    def write(self, name, text):
        """Записать текстовый файл и вернуть его путь."""
        path = self.path(name)
        with open(path, "w", encoding="utf-8") as stream:
            stream.write(text)
        return path


def run_main(main, argv):
    """Запустить main(argv), вернув код, stdout и stderr."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(argv)
        except SystemExit as exit_error:
            code = exit_error.code
    return code, out.getvalue(), err.getvalue()
