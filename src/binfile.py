"""Чтение и запись двоичных файлов с машинным кодом."""

from errors import UvmError


def write_binary(path, code):
    """Записать машинный код в двоичный файл."""
    try:
        with open(path, "wb") as stream:
            stream.write(code)
    except OSError as error:
        reason = error.strerror or str(error)
        raise UvmError(f"{path}: cannot write output: {reason}") from error
