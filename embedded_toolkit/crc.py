"""CRC checksum implementations for serial protocol validation."""


def crc8(data: bytes, polynomial: int = 0x07, init: int = 0x00) -> int:
    """CRC-8 (Dallas/Maxim 1-Wire compatible by default).

    Example::

        check = crc8(b'\x01\x02\x03')
        frame = data + bytes([check])
    """
    crc = init
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc << 1) ^ polynomial) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
    return crc


def crc16_modbus(data: bytes) -> int:
    """CRC-16/MODBUS used in Modbus RTU framing.

    Example::

        frame = address + function + payload
        crc   = crc16_modbus(frame)
        packet = frame + crc.to_bytes(2, 'little')
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = ((crc >> 1) ^ 0xA001) if crc & 1 else crc >> 1
    return crc


def crc32(data: bytes, init: int = 0xFFFFFFFF) -> int:
    """CRC-32 (Ethernet/ZIP polynomial)."""
    import zlib
    return zlib.crc32(data, init) & 0xFFFFFFFF
