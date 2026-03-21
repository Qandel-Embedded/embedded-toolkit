from embedded_toolkit import crc8, crc16_modbus, crc32


def test_crc8_known_value():
    assert crc8(b'\x01\x02\x03') == crc8(b'\x01\x02\x03')  # deterministic


def test_crc16_modbus_known():
    # Modbus RTU standard test vector
    data = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x02])
    crc = crc16_modbus(data)
    assert crc == 0xC40B


def test_crc32_empty():
    assert crc32(b'') is not None


def test_crc_detects_corruption():
    data = b'hello embedded world'
    good = crc16_modbus(data)
    bad  = crc16_modbus(data[:-1] + bytes([data[-1] ^ 0xFF]))
    assert good != bad
