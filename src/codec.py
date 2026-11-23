"""Преобразование команд: промежуточное представление -> машинный код."""

from errors import UvmError
from isa import BY_OPCODE, OPCODE_BITS

BYTE_ORDER = "little"
OPERAND_MIN = 0


def encode(instruction):
    """Перевести одну команду в байты (младший байт первым)."""
    spec = BY_OPCODE.get(instruction.a)
    if spec is None:
        raise UvmError(f"unknown operation code A={instruction.a}")
    if not OPERAND_MIN <= instruction.b <= spec.operand_max:
        raise UvmError(f"operand B={instruction.b} of {spec.mnemonic} "
                       f"does not fit into {spec.operand_bits} bits")
    value = instruction.a | (instruction.b << OPCODE_BITS)
    return value.to_bytes(spec.size, BYTE_ORDER)


def encode_program(instructions):
    """Перевести список команд в машинный код программы."""
    return b"".join(encode(instruction) for instruction in instructions)


def format_bytes(code):
    """Строка с байтами в формате спецификации: 0x51, 0x19, 0x00."""
    return ", ".join(f"0x{byte:02X}" for byte in code)
